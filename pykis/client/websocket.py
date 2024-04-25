import base64
import json
import threading
import time
from multiprocessing import Event, Lock
from multiprocessing.synchronize import Event as EventType
from multiprocessing.synchronize import Lock as LockType
from typing import TYPE_CHECKING

from websocket import WebSocketApp

from pykis import logging
from pykis.__env__ import (
    WEBSOCKET_MAX_SUBSCRIPTIONS,
    WEBSOCKET_REAL_DOMAIN,
    WEBSOCKET_VIRTUAL_DOMAIN,
)
from pykis.api.websocket import WEBSOCKET_RESPONSES_MAP
from pykis.client.messaging import (
    TR_SUBSCRIBE_TYPE,
    TR_UNSUBSCRIBE_TYPE,
    KisWebsocketEncryptionKey,
    KisWebsocketForm,
    KisWebsocketRequest,
    KisWebsocketTR,
)
from pykis.event.eventhandler import KisEventHandler
from pykis.event.websocket.subscription import (
    KisSubscribedEventArgs,
    KisSubscriptionEventArgs,
)
from pykis.responses.websocket import KisWebsocketResponse
from pykis.utils.thread_safe import thread_safe

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisWebsocketClient:
    """한국투자증권 실시간 클라이언트"""

    kis: "PyKis"
    """한국투자증권 API"""

    websocket: WebSocketApp | None = None
    """웹소켓"""
    thread: threading.Thread | None = None
    """웹소켓 스레드"""

    subscribed_event: KisEventHandler["KisWebsocketClient", KisSubscribedEventArgs]
    """구독 추가 이벤트"""
    unsubscribed_event: KisEventHandler["KisWebsocketClient", KisSubscribedEventArgs]
    """구독 해제 이벤트"""

    event: KisEventHandler["KisWebsocketClient", KisSubscriptionEventArgs]
    """구독 이벤트"""

    reconnect: bool = True
    """자동 재접속 여부"""
    reconnect_interval: float = 5
    """재접속 간격 (초)"""

    _connect_lock: LockType
    """접속 락"""
    _connect_event: EventType
    """즉시 접속 이벤트"""
    _connected_event: EventType
    """접속됨 이벤트"""

    _subscriptions: set[KisWebsocketTR]
    """TR 구독 목록"""
    _registered_subscriptions: set[KisWebsocketTR]
    """TR 등록된 구독 목록"""

    _keychain: dict[KisWebsocketTR, KisWebsocketEncryptionKey]
    """암호화 키체인"""

    def __init__(self, kis: "PyKis"):
        self.kis = kis
        self.subscribed_event = KisEventHandler()
        self.unsubscribed_event = KisEventHandler()
        self.event = KisEventHandler()
        self._connect_lock = Lock()
        self._connect_event = Event()
        self._connected_event = Event()
        self._subscriptions = set()
        self._registered_subscriptions = set()
        self._keychain = {}

    def is_subscribed(self, id: str, key: str = "") -> bool:
        """
        TR 구독 여부를 확인합니다.

        Args:
            id (str): TR ID
            key (str): TR Key Default is "".

        Returns:
            bool: 구독 여부
        """
        return KisWebsocketTR(id, key) in self._subscriptions

    @property
    def connected(self) -> bool:
        return self.websocket is not None and self._connected_event.is_set()

    @thread_safe("connect")
    def connect(self):
        """한국투자증권 웹소켓 서버에 접속합니다. (비동기)"""
        if self.connected:
            return

        if self.thread is not None and self.thread.is_alive():
            # 즉시 재접속
            self._connect_event.set()
            return

        self.thread = threading.Thread(target=self._run_forever)
        self.thread.start()

    def _ensure_connection(self):
        """접속을 보장합니다."""
        if not self.connected:
            self.connect()

    def ensure_connected(self, timeout: float | None = None):
        """
        접속 상태를 동기적으로 보장합니다.

        Args:
            timeout (float | None): 타임아웃 (초)

        Raises:
            TimeoutError: 접속 시간 초과
        """
        self._ensure_connection()
        self._connected_event.wait(timeout=timeout)

    @thread_safe("connect")
    def disconnect(self):
        """한국투자증권 웹소켓 서버와 연결을 해제합니다."""
        thread = self.thread

        if thread is not None and thread.is_alive():
            self.thread = None

            if self.websocket:
                logging.logger.info("RTC: Disconnecting from server")
                self.websocket.close()

    def _request(self, type: str, body: KisWebsocketForm | None = None) -> bool:
        """
        요청을 보냅니다.

        Args:
            type (str): 요청 타입
            body (KisWebsocketForm | None): 요청 본문

        Returns:
            bool: 요청 성공 여부
        """
        if not self.websocket or not self.connected:
            return False

        logging.logger.debug("RTC: Sending request: %s %s", type, body)
        self.websocket.send(
            json.dumps(
                KisWebsocketRequest(
                    kis=self.kis,
                    type=type,
                    body=body,
                ).build()
            )
        )

        return True

    @thread_safe("subscriptions")
    def subscribe(self, id: str, key: str):
        """
        TR을 구독합니다.

        Args:
            id (str): TR ID
            key (str): TR Key

        Raises:
            ValueError: 최대 구독 수를 초과했습니다.
        """
        self._ensure_connection()
        tr = KisWebsocketTR(id, key)

        if tr in self._subscriptions:
            return

        if len(self._subscriptions) >= WEBSOCKET_MAX_SUBSCRIPTIONS:
            logging.logger.warning("RTC: Maximum number of subscriptions reached")
            raise ValueError("Maximum number of subscriptions reached")

        self._subscriptions.add(tr)
        self._request(TR_SUBSCRIBE_TYPE, tr)
        logging.logger.info("RTC: Subscribed to %s", tr)

    @thread_safe("subscriptions")
    def unsubscribe(self, id: str, key: str):
        """
        TR 구독을 취소합니다.

        Args:
            id (str): TR ID
            key (str): TR Key
        """
        tr = KisWebsocketTR(id, key)

        if tr not in self._subscriptions:
            return

        self._subscriptions.remove(tr)
        self._request(TR_UNSUBSCRIBE_TYPE, tr)

    def unsubscribe_all(self):
        """모든 TR 구독을 취소합니다."""
        for tr in self._subscriptions.copy():
            self.unsubscribe(tr.id, tr.key)

    @thread_safe("subscriptions")
    def _reset_session_state(self):
        """세션 상태를 초기화합니다."""
        # 등록된 구독 초기화
        self._registered_subscriptions.clear()
        # 암호화 키 초기화
        self._keychain.clear()

    def _restore_subscriptions(self):
        """구독 목록을 복원합니다."""
        subscriptions = self._subscriptions - self._registered_subscriptions

        if not subscriptions:
            return

        logging.logger.info("RTC: Restoring subscriptions...")

        for tr in subscriptions:
            self._request(TR_SUBSCRIBE_TYPE, tr)

    def _run_forever(self) -> bool:
        SLEEP_INTERVAL = 0.1

        if not self._connect_lock.acquire(block=False):
            return False

        try:
            while self.reconnect or not self.thread != threading.current_thread():
                try:
                    self._connected_event.clear()
                    self.websocket = WebSocketApp(
                        f"{WEBSOCKET_VIRTUAL_DOMAIN if self.kis.virtual else WEBSOCKET_REAL_DOMAIN}/tryitout",
                        on_open=self._on_open,
                        on_error=self._on_error,
                        on_close=self._on_close,
                        on_message=self._on_message,
                    )
                    self.websocket.run_forever()
                except Exception as e:
                    logging.logger.error("RTC: Unexpected error: %s", e)

                # 종료 확인
                if self.thread != threading.current_thread():
                    break

                # 재접속 간격
                self.websocket = None
                logging.logger.info("RTC: Reconnecting in %s seconds...", self.reconnect_interval)

                self._connect_event.clear()

                for _ in range(int(self.reconnect_interval / SLEEP_INTERVAL)):
                    time.sleep(SLEEP_INTERVAL)

                    if self.thread != threading.current_thread():
                        break

                    # 즉시 재접속
                    if self._connect_event.is_set():
                        self._connect_event.clear()
                        break

        finally:
            self.websocket = None
            self._connected_event.clear()
            self._connect_lock.release()

        return True

    def _on_open(self, websocket: WebSocketApp):
        if websocket is not self.websocket:
            return

        logging.logger.info("RTC: Connected to server")
        self._reset_session_state()
        self._connected_event.set()

        self._restore_subscriptions()

    def _on_error(self, websocket: WebSocketApp, error: Exception):
        if websocket is not self.websocket:
            return

        logging.logger.error("RTC: WebSocket error: %s", error)

    def _on_close(self, websocket: WebSocketApp, code: int, reason: str):
        if websocket is not self.websocket:
            return

        logging.logger.info("RTC: Disconnected from server: %s", reason)

    def _on_message(self, websocket: WebSocketApp, message: str):
        if websocket is not self.websocket:
            return

        try:
            match message[0]:
                case "0" | "1":  # 이벤트 데이터 (암호화여부)
                    self._handle_event(message)
                case "{" | _:  # 제어 데이터
                    self._handle_control(json.loads(message))
        except Exception as e:
            logging.logger.error("RTC: failed to handle message: %s", e)

    def _handle_control(self, data: dict):
        if not self.websocket:
            return False

        header = data["header"]
        body = data.get("body")

        id: str = header["tr_id"]
        key: str | None = header.get("tr_key")
        encrypted: bool = header.get("encrypt") == "Y"

        if id == "PINGPONG":
            logging.logger.debug("RTC: Received PINGPONG")
            self.websocket.send(json.dumps(data))
            return

        if not body:
            logging.logger.warning("RTC: Unhandled control data: %s", id)
            return

        tr = KisWebsocketTR(id, key or "")
        code = data["body"]["msg_cd"]
        message = data["body"]["msg1"]

        if encrypted:
            self._set_encryption_key(tr, body["output"])

        match code:
            case "OPSP0000":  # subscribed
                logging.logger.info("RTC: Subscribed to %s", tr)
                self._registered_subscriptions.add(tr)
                self.subscribed_event.invoke(self, KisSubscribedEventArgs(tr))

            case "OPSP0002":  # already subscribed
                logging.logger.info("RTC: Already subscribed to %s", tr)
                self._registered_subscriptions.add(tr)

            case "OPSP0001":  # unsubscribed
                logging.logger.info("RTC: Unsubscribed from %s", tr)
                self._registered_subscriptions.remove(tr)
                self._keychain.pop(tr, None)
                self.unsubscribed_event.invoke(self, KisSubscribedEventArgs(tr))

            case "OPSP0003":  # not subscribed
                logging.logger.info("RTC: Already unsubscribed from %s", tr)
                self._registered_subscriptions.remove(tr)
                self._keychain.pop(tr, None)

            case "OPSP0007":  # internal error
                logging.logger.error("RTC: Internal server error: %s %s", tr, message)

            case _:
                logging.logger.warning("RTC: Unhandled control message: %s(%s) %s", tr, code, message)

    def _set_encryption_key(self, tr: KisWebsocketTR, body: dict):
        """암호화 키를 설정합니다."""
        self._keychain[tr] = KisWebsocketEncryptionKey(
            key=body["key"].encode("utf-8"),
            iv=body["iv"].encode("utf-8"),
        )

    def _handle_event(self, message: str):
        (
            encrypted,
            id,
            count,
            body,
        ) = message.split("|", 3)
        encrypted = encrypted == "1"
        count = int(count)
        tr = KisWebsocketTR(id, "")

        if encrypted:
            try:
                key = self._keychain.get(tr)

                if not key:
                    logging.logger.error("RTC: No encryption key for %s", tr)
                    return

                body = key.decrypt(base64.b64decode(body)).decode("utf-8")
            except Exception as e:
                logging.logger.exception("RTC: Failed to decrypt message: %s %s", id, e)
                return

        if not (response_type := WEBSOCKET_RESPONSES_MAP.get(id)):
            logging.logger.warning("RTC: No response type for %s", id)
            return

        try:
            for response in KisWebsocketResponse.parse(
                data=body,
                count=count,
                response_type=response_type,
            ):
                try:
                    self.event.invoke(
                        self,
                        KisSubscriptionEventArgs(
                            tr=tr,
                            response=response,
                        ),
                    )
                except Exception as e:
                    logging.logger.exception("RTC: Failed to emit event: %s %s", tr, e)
        except Exception as e:
            logging.logger.exception("RTC: Failed to parse message: %s %s", tr, e)
            return
