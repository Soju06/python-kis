from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Awaitable, Callable, cast

from pykis.streaming._async.crypto import AesCbcDecryptor, StreamingKeyStore
from pykis.streaming._async.router import StreamingEventRouter
from pykis.streaming._async.transport import WebSocketRunner, WebSocketTransport
from pykis.streaming.raw.adapter import StreamingFrameHandler

ControlMessage = dict[str, object]


@dataclass(slots=True)
class StreamingSession:
    url: str
    frame_handler: StreamingFrameHandler
    key_store: StreamingKeyStore
    transport: WebSocketTransport
    _runner: WebSocketRunner | None
    _task: asyncio.Task[None] | None
    on_control: Callable[[ControlMessage], None] | None
    on_reconnect: Callable[[], Awaitable[None] | None] | None
    router: StreamingEventRouter | None
    reconnect: bool
    reconnect_backoff: float
    reconnect_max_backoff: float

    def __init__(
        self,
        *,
        url: str,
        frame_handler: StreamingFrameHandler,
        router: StreamingEventRouter | None = None,
        on_control: Callable[[ControlMessage], None] | None = None,
        on_reconnect: Callable[[], Awaitable[None] | None] | None = None,
        reconnect: bool = True,
        reconnect_backoff: float = 1.0,
        reconnect_max_backoff: float = 30.0,
    ) -> None:
        self.url = url
        self.frame_handler = frame_handler
        self.key_store = StreamingKeyStore()
        self.transport = WebSocketTransport(url)
        self._runner = None
        self._task = None
        self.on_control = on_control
        self.on_reconnect = on_reconnect
        self.router = router
        self.reconnect = reconnect
        self.reconnect_backoff = reconnect_backoff
        self.reconnect_max_backoff = reconnect_max_backoff

        if self.frame_handler.decryptor is None:
            self.frame_handler.decryptor = AesCbcDecryptor(self.key_store)

    async def connect(self) -> None:
        if self._task is not None:
            return
        self._task = asyncio.create_task(self._run_loop())

    async def close(self) -> None:
        self.reconnect = False
        if self._task is not None:
            self._task.cancel()
            self._task = None
        await self.transport.close()

    async def subscribe(
        self,
        *,
        approval_key: str,
        tr_id: str,
        tr_key: str,
        custtype: str = "P",
        tr_type: str = "1",
        content_type: str = "utf-8",
    ) -> None:
        message = _build_subscription_message(
            approval_key=approval_key,
            tr_id=tr_id,
            tr_key=tr_key,
            custtype=custtype,
            tr_type=tr_type,
            content_type=content_type,
        )
        await self.transport.send_json(message)

    async def unsubscribe(
        self,
        *,
        approval_key: str,
        tr_id: str,
        tr_key: str,
        custtype: str = "P",
        content_type: str = "utf-8",
    ) -> None:
        await self.subscribe(
            approval_key=approval_key,
            tr_id=tr_id,
            tr_key=tr_key,
            custtype=custtype,
            tr_type="2",
            content_type=content_type,
        )

    def _handle_message(self, message: str) -> None:
        message = message.strip()
        if not message:
            return
        if message.startswith("{"):
            data = _safe_json(message)
            if data:
                self._handle_control(data)
            return
        if message.startswith("["):
            return
        if self.router is not None:
            self.router.handle_frame(message)
        else:
            self.frame_handler.handle_frame(message)

    def _handle_control(self, data: ControlMessage) -> None:
        body = _get_dict(data.get("body"))
        output = _get_dict(body.get("output")) if body else None
        if output and "key" in output and "iv" in output:
            key = str(output.get("key", ""))
            iv = str(output.get("iv", ""))
            self.key_store.update(key, iv)
        if self.on_control is not None:
            self.on_control(data)

    async def _run_loop(self) -> None:
        backoff = self.reconnect_backoff
        while True:
            try:
                await self.transport.connect()
                self._runner = WebSocketRunner(self.transport, self._handle_message)
                await self._runner.run()
            except asyncio.CancelledError:
                return
            except Exception:
                await self.transport.close()
            if not self.reconnect:
                await self.transport.close()
                return
            self.key_store.clear()
            if self.on_reconnect is not None:
                result = self.on_reconnect()
                if result is not None:
                    await result
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2.0, self.reconnect_max_backoff)


def _build_subscription_message(
    *,
    approval_key: str,
    tr_id: str,
    tr_key: str,
    custtype: str,
    tr_type: str,
    content_type: str,
) -> dict[str, object]:
    return {
        "header": {
            "approval_key": approval_key,
            "custtype": custtype,
            "tr_type": tr_type,
            "content-type": content_type,
        },
        "body": {"input": {"tr_id": tr_id, "tr_key": tr_key}},
    }


def _safe_json(message: str) -> ControlMessage | None:
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict):
        return data
    return None


def _get_dict(value: object) -> dict[str, object] | None:
    if isinstance(value, dict):
        return cast(dict[str, object], value)
    return None
