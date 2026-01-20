from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Callable, cast

from pykis.streaming.crypto import AesCbcDecryptor, StreamingKeyStore
from pykis.streaming.raw.adapter import StreamingFrameHandler
from pykis.streaming.transport import WebSocketRunner, WebSocketTransport

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

    def __init__(
        self,
        *,
        url: str,
        frame_handler: StreamingFrameHandler,
        on_control: Callable[[ControlMessage], None] | None = None,
    ) -> None:
        self.url = url
        self.frame_handler = frame_handler
        self.key_store = StreamingKeyStore()
        self.transport = WebSocketTransport(url)
        self._runner = None
        self._task = None
        self.on_control = on_control

        if self.frame_handler.decryptor is None:
            self.frame_handler.decryptor = AesCbcDecryptor(self.key_store)

    async def connect(self) -> None:
        await self.transport.connect()
        self._runner = WebSocketRunner(self.transport, self._handle_message)
        self._task = asyncio.create_task(self._runner.run())

    async def close(self) -> None:
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
