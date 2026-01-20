from __future__ import annotations

import asyncio
import importlib
import json
from dataclasses import dataclass
from types import ModuleType
from typing import AsyncIterator, Callable, Protocol


class WebSocketConnection(Protocol):
    async def send(self, data: str) -> None: ...
    async def close(self) -> None: ...
    def __aiter__(self) -> AsyncIterator[str | bytes]: ...


@dataclass(slots=True)
class WebSocketTransport:
    url: str
    connect_timeout: float
    ping_interval: float | None
    _ws: WebSocketConnection | None = None

    def __init__(
        self,
        url: str,
        *,
        connect_timeout: float = 10.0,
        ping_interval: float | None = 20.0,
    ) -> None:
        self.url = url
        self.connect_timeout = connect_timeout
        self.ping_interval = ping_interval
        self._ws = None

    async def connect(self) -> None:
        websockets = _load_websockets()
        self._ws = await asyncio.wait_for(
            websockets.connect(self.url, ping_interval=self.ping_interval),
            timeout=self.connect_timeout,
        )

    async def close(self) -> None:
        if self._ws is None:
            return
        await self._ws.close()
        self._ws = None

    async def send_json(self, payload: dict[str, object]) -> None:
        if self._ws is None:
            raise RuntimeError("WebSocket not connected")
        await self._ws.send(json.dumps(payload, ensure_ascii=False))

    async def messages(self) -> AsyncIterator[str]:
        if self._ws is None:
            raise RuntimeError("WebSocket not connected")
        async for message in self._ws:
            if isinstance(message, bytes):
                yield message.decode("utf-8", errors="replace")
            else:
                yield str(message)


@dataclass(slots=True)
class WebSocketRunner:
    transport: WebSocketTransport
    on_message: Callable[[str], None]

    async def run(self) -> None:
        async for message in self.transport.messages():
            self.on_message(message)


def _load_websockets() -> ModuleType:
    try:
        return importlib.import_module("websockets")
    except Exception as exc:
        raise RuntimeError("websockets is required for streaming transport") from exc
