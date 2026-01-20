from __future__ import annotations

import importlib
import json
from dataclasses import dataclass
from types import ModuleType
from typing import Iterator, Callable, Protocol


class WebSocketConnection(Protocol):
    def send(self, data: str) -> None: ...
    def close(self) -> None: ...
    def __iter__(self) -> Iterator[str | bytes]: ...


@dataclass(slots=True)
class SyncWebSocketTransport:
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

    def connect(self) -> None:
        websockets = _load_websockets()
        self._ws = websockets.sync.client.connect(
            self.url,
            ping_interval=self.ping_interval,
            open_timeout=self.connect_timeout,
        )

    def close(self) -> None:
        if self._ws is None:
            return
        self._ws.close()
        self._ws = None

    def send_json(self, payload: dict[str, object]) -> None:
        if self._ws is None:
            raise RuntimeError("WebSocket not connected")
        self._ws.send(json.dumps(payload, ensure_ascii=False))

    def messages(self) -> Iterator[str]:
        if self._ws is None:
            raise RuntimeError("WebSocket not connected")
        for message in self._ws:
            if isinstance(message, bytes):
                yield message.decode("utf-8", errors="replace")
            else:
                yield str(message)


@dataclass(slots=True)
class SyncWebSocketRunner:
    transport: SyncWebSocketTransport
    on_message: Callable[[str], None]

    def run(self) -> None:
        for message in self.transport.messages():
            self.on_message(message)


def _load_websockets() -> ModuleType:
    try:
        return importlib.import_module("websockets")
    except Exception as exc:
        raise RuntimeError("websockets is required for streaming transport") from exc
