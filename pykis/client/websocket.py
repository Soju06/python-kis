import base64
import json
import threading
import time
from multiprocessing import Event, Lock
from multiprocessing.synchronize import Event as EventType
from multiprocessing.synchronize import Lock as LockType
from typing import TYPE_CHECKING, Callable

from websocket import WebSocketApp, WebSocketConnectionClosedException

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
from pykis.client.object import KisObjectBase, kis_object_init
from pykis.event.filters.subscription import KisSubscriptionEventFilter
from pykis.event.handler import (
    KisEventFilter,
    KisEventHandler,
    KisEventTicket,
    KisMultiEventFilter,
)
from pykis.event.subscription import KisSubscribedEventArgs, KisSubscriptionEventArgs
from pykis.responses.websocket import KisWebsocketResponse, TWebsocketResponse
from pykis.utils.reference import ReferenceStore, ReferenceTicket, package_mathod
from pykis.utils.thread_safe import thread_safe

if TYPE_CHECKING:
    from pykis.kis import PyKis

__all__ = [
    "KisWebsocketClient",
]


class KisWebsocketClient:
    """한국투자증권 실시간 클라이언트"""

    kis: "PyKis"
    """한국투자증권 API"""

    virtual: bool
    """모의투자 서버 여부"""

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
    _reference_store: ReferenceStore
    """이벤트 참조 카운터"""

    _primary_client: "KisWebsocketClient | None" = None
    """계좌 조회가 가능한 서버의 클라이언트 (모의투자에서만 사용)"""

    def __init__(self, kis: "PyKis", virtual: bool = False):
        self.kis = kis
        self.virtual = virtual
        self.subscribed_event = KisEventHandler()
        self.unsubscribed_event = KisEventHandler()
        self.event = KisEventHandler()
        self._connect_lock = Lock()
        self._connect_event = Event()
        self._connected_event = Event()
        self._subscriptions = set()
        self._registered_subscriptions = set()
        self._keychain = dict()
        self._reference_store = ReferenceStore(callback=self._release_reference)

    def is_subscribed(self, id: str, key: str = "") -> bool:
        """
        TR 구독 여부를 확인합니다.

        Args:
            id (str): TR ID
            key (str): TR Key Default is "".

        Returns:
            bool: 구독 여부
        """
        return (KisWebsocketTR(id, key) in self._subscriptions) or (
            self._primary_client is not None and self._primary_client.is_subscribed(id, key)
        )

    @property
    def subscriptions(self) -> set[KisWebsocketTR]:
        return self._subscriptions | (self._primary_client.subscriptions if self._primary_client else set())

    @property
    def connected(self) -> bool:
        return (
            self.websocket is not None
            and self._connected_event.is_set()
            and (self._primary_client is None or self._primary_client.connected)
        )

    @thread_safe("connect")
    def connect(self):
        """한국투자증권 웹소켓 서버에 접속합니다. (비동기)"""
        if self._primary_client:
            self._primary_client.connect()

        if self.connected:
            return

        if self.thread is not None and self.thread.is_alive():
            # 즉시 재접속
            self._connect_event.set()
            return

        self.thread = threading.Thread(target=self._run_forever, daemon=True)
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
        if self._primary_client:
            return self._primary_client.ensure_connected(timeout=timeout)

        self._ensure_connection()
        self._connected_event.wait(timeout=timeout)

    @thread_safe("connect")
    def disconnect(self):
        """한국투자증권 웹소켓 서버와 연결을 해제합니다."""
        if self._primary_client:
            self._primary_client.disconnect()

        thread = self.thread

        if thread is not None and thread.is_alive():
            self.thread = None

            if self.websocket:
                logging.logger.info("RTC Disconnecting from server")
                self.websocket.close()

    def _request(self, type: str, body: KisWebsocketForm | None = None, force: bool = False) -> bool:
        """
        요청을 보냅니다.

        Args:
            type (str): 요청 타입
            body (KisWebsocketForm | None): 요청 본문
            force (bool): 접속 상태와 상관없이 요청을 보낼지 여부

        Returns:
            bool: 요청 성공 여부
        """
        if not self.websocket or (not force and not self._connected_event.is_set()):
            return False

        logging.logger.debug("RTC Sending request: %s %s", type, body)
        self.websocket.send(
            json.dumps(
                KisWebsocketRequest(
                    kis=self.kis,
                    type=type,
                    body=body,
                    domain="virtual" if self.virtual else "real",
                ).build()
            )
        )

        return True

    @thread_safe("subscriptions")
    def subscribe(self, id: str, key: str, primary: bool = False):
        """
        TR을 구독합니다.

        Args:
            id (str): TR ID
            key (str): TR Key
            primary (bool): 주 서버에 구독할지 여부

        Raises:
            ValueError: 최대 구독 수를 초과했습니다.
        """
        if primary and (client := self._ensure_primary_client()) is not self:
            client.subscribe(
                id=id,
                key=key,
                primary=False,
            )
            return

        self._ensure_connection()
        tr = KisWebsocketTR(id, key)

        if tr in self._subscriptions:
            return

        if len(self._subscriptions) >= WEBSOCKET_MAX_SUBSCRIPTIONS:
            logging.logger.warning("RTC Maximum number of subscriptions reached")
            raise ValueError("Maximum number of subscriptions reached")

        self._subscriptions.add(tr)
        self._request(TR_SUBSCRIBE_TYPE, tr)

    @thread_safe("subscriptions")
    def unsubscribe(self, id: str, key: str, primary: bool = False):
        """
        TR 구독을 취소합니다.

        Args:
            id (str): TR ID
            key (str): TR Key
            primary (bool): 주 서버에 구독을 취소할지 여부
        """
        if primary and (client := self._ensure_primary_client()) is not self:
            client.unsubscribe(
                id=id,
                key=key,
                primary=False,
            )
            return

        tr = KisWebsocketTR(id, key)

        if tr not in self._subscriptions:
            return

        self._subscriptions.remove(tr)
        self._request(TR_UNSUBSCRIBE_TYPE, tr)

    def unsubscribe_all(self):
        """모든 TR 구독을 취소합니다."""
        if self._primary_client:
            self._primary_client.unsubscribe_all()

        for tr in self._subscriptions.copy():
            self.unsubscribe(tr.id, tr.key)

    def referenced_subscribe(self, id: str, key: str, primary: bool = False) -> ReferenceTicket:
        """
        래퍼런스 카운터를 사용하여 TR을 구독합니다.
        카운터가 0일 때 구독을 취소합니다.

        Args:
            id (str): TR ID
            key (str): TR Key
            primary (bool): 주 서버에 구독할지 여부
        """
        self.subscribe(id, key, primary)
        return self._reference_store.ticket(f"{id}:{key}")

    def on(
        self,
        id: str,
        key: str,
        callback: Callable[["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]], None],
        where: KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]] | None = None,
        once: bool = False,
        primary: bool = False,
    ) -> KisEventTicket["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]]:
        """
        TR을 구독합니다.

        Args:
            id (str): TR ID
            key (str): TR Key
            callback (Callable[[TSender, TEventArgs], None]): 콜백 함수
            where (KisEventFilter["KisWebsocketClient", KisSubscriptionEventArgs[TWebsocketResponse]], optional): 이벤트 필터. Defaults to None.
            primary (bool): 주 서버에 구독할지 여부
        """
        subscription_filter = KisSubscriptionEventFilter(id)

        return self.event.on(
            handler=package_mathod(
                callback,
                ticket=self.referenced_subscribe(
                    id=id,
                    key=key,
                    primary=primary,
                ),
            ),
            where=KisMultiEventFilter(subscription_filter, where) if where else subscription_filter,
            once=once,
        )

    def _release_reference(self, key: str, value: int):
        if value == 0:
            id, key = key.split(":", 1)
            self.unsubscribe(id, key)

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

        logging.logger.info("RTC Restoring subscriptions... %s", ", ".join(map(str, subscriptions)))

        for tr in subscriptions:
            self._request(TR_SUBSCRIBE_TYPE, tr, force=True)

    def _run_forever(self) -> bool:
        SLEEP_INTERVAL = 0.1

        if not self._connect_lock.acquire(block=False):
            return False

        try:
            while self.reconnect or not self.thread != threading.current_thread():
                try:
                    self._connected_event.clear()
                    self.websocket = WebSocketApp(
                        f"{WEBSOCKET_VIRTUAL_DOMAIN if self.virtual else WEBSOCKET_REAL_DOMAIN}/tryitout",
                        on_open=self._on_open,  # type: ignore
                        on_error=self._on_error,  # type: ignore
                        on_close=self._on_close,  # type: ignore
                        on_message=self._on_message,  # type: ignore
                    )
                    self.websocket.run_forever()
                except Exception as e:
                    logging.logger.error("RTC Unexpected error: %s", e, exc_info=True)

                # 종료 확인
                if self.thread != threading.current_thread():
                    break

                # 재접속 간격
                self.websocket = None
                logging.logger.info("RTC Reconnecting in %s seconds...", self.reconnect_interval)

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

        logging.logger.info("RTC Connected to %s server", "virtual" if self.virtual else "real")
        self._reset_session_state()
        self._restore_subscriptions()
        self._connected_event.set()

    def _on_error(self, websocket: WebSocketApp, error: Exception):
        if websocket is not self.websocket:
            return

        if isinstance(error, WebSocketConnectionClosedException):
            logging.logger.error("RTC Websocket error: Connection closed")
        elif isinstance(error, KeyboardInterrupt):
            logging.logger.error("RTC Websocket error: Keyboard interrupt")
        else:
            logging.logger.error("RTC Websocket error: %s", error, exc_info=True)

    def _on_close(self, websocket: WebSocketApp, code: int, reason: str):
        if websocket is not self.websocket:
            return

        logging.logger.info("RTC Disconnected from server: %s", reason)

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
            logging.logger.error("RTC failed to handle message: %s", e, exc_info=True)

    def _handle_control(self, data: dict):
        if not self.websocket:
            return False

        header = data["header"]
        body = data.get("body")

        id: str = header["tr_id"]
        key: str | None = header.get("tr_key")

        if id == "PINGPONG":
            # logging.logger.debug("RTC Received PINGPONG")
            self.websocket.send(json.dumps(data))
            return

        if not body:
            logging.logger.warning("RTC Unhandled control data: %s", id)
            return

        tr = KisWebsocketTR(id, key or "")
        code = body["msg_cd"]
        message = body["msg1"]
        output = body.get("output")

        if output:
            self._set_encryption_key(tr, output)

        match code:
            case "OPSP0000":  # subscribed
                logging.logger.info("RTC Subscribed to %s", tr)
                self._registered_subscriptions.add(tr)
                self.subscribed_event.invoke(self, KisSubscribedEventArgs(tr))

            case "OPSP0002":  # already subscribed
                logging.logger.info("RTC Already subscribed to %s", tr)
                self._registered_subscriptions.add(tr)

            case "OPSP0001":  # unsubscribed
                logging.logger.info("RTC Unsubscribed from %s", tr)
                try:
                    self._registered_subscriptions.remove(tr)
                except KeyError:
                    pass
                self._keychain.pop(tr, None)
                self.unsubscribed_event.invoke(self, KisSubscribedEventArgs(tr))

            case "OPSP0003":  # not subscribed
                logging.logger.info("RTC Already unsubscribed from %s", tr)
                try:
                    self._registered_subscriptions.remove(tr)
                except KeyError:
                    pass
                self._keychain.pop(tr, None)

            case "OPSP8996":  # already in use
                logging.logger.error("RTC Session already in use")

            case "OPSP0007":  # internal error
                logging.logger.error("RTC Internal server error: %s %s", tr, message)

            case _:
                logging.logger.warning("RTC Unhandled control message: %s(%s) %s", tr, code, message)

    def _set_encryption_key(self, tr: KisWebsocketTR, body: dict):
        """암호화 키를 설정합니다."""
        # 국내주식 실시간체결통보 실전, 모의 해외주식 실시간체결통보 실전, 모의
        if tr.id in ("H0STCNI0", "H0STCNI9", "H0GSCNI0", "H0GSCNI9"):
            # 체결통보의 경우 tr key를 사용하지 않음
            tr = KisWebsocketTR(tr.id, "")

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
                    logging.logger.error("RTC No encryption key for %s", tr)
                    return

                body = key.decrypt(base64.b64decode(body)).decode("utf-8")
            except Exception as e:
                logging.logger.exception("RTC Failed to decrypt message: %s %s", id, e)
                return

        if not (response_type := WEBSOCKET_RESPONSES_MAP.get(id)):
            logging.logger.warning("RTC No response type for %s", id)
            return

        try:
            for response in KisWebsocketResponse.parse(
                body,
                count=count,
                response_type=response_type,
            ):
                if isinstance(response, KisObjectBase):
                    kis_object_init(self.kis, response)

                try:
                    self.event.invoke(
                        self,
                        KisSubscriptionEventArgs(
                            tr=tr,
                            response=response,
                        ),
                    )
                except Exception as e:
                    logging.logger.exception("RTC Failed to emit event: %s %s", tr, e)
        except Exception as e:
            logging.logger.exception("RTC Failed to parse message: %s %s", tr, e)
            return

    @thread_safe("primary_client")
    def _ensure_primary_client(self) -> "KisWebsocketClient":
        if self.kis.virtual and not self.virtual and not self._primary_client:
            self._primary_client = KisWebsocketClient(self.kis, virtual=True)

            self._primary_client.subscribed_event += self._primary_client_subscribed_event
            self._primary_client.unsubscribed_event += self._primary_client_unsubscribed_event
            self._primary_client.event += self._primary_client_event

            return self._primary_client
        else:
            return self

    def _primary_client_subscribed_event(self, sender: "KisWebsocketClient", args: KisSubscribedEventArgs):
        self.subscribed_event.invoke(self, args)

    def _primary_client_unsubscribed_event(self, sender: "KisWebsocketClient", args: KisSubscribedEventArgs):
        self.unsubscribed_event.invoke(self, args)

    def _primary_client_event(self, sender: "KisWebsocketClient", args: KisSubscriptionEventArgs):
        self.event.invoke(self, args)
