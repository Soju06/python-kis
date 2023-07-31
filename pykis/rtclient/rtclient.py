import json
import logging
from concurrent.futures import Future, as_completed
from multiprocessing import Lock
from multiprocessing.synchronize import Lock as LockType
from threading import Thread
from time import sleep

from websocket import WebSocketApp

from ..__env__ import REAL_TIME_PRICE_MAX_SUBSCRIPTIONS, WEBSOCKET_REAL_DOMAIN, WEBSOCKET_VIRTUAL_DOMAIN
from ..client.appkey import KisKey
from ..client.client import KisClient
from ..logging import KisLoggable
from .encrypt import KisRTEncrypt
from .event import KisRTEvent
from .messaging import KisRTRequest, KisRTResponse, KisRTSysResponse
from .responses import RT_CODE_TYPE, RT_RESPONSES, _rtcd


class KisRTClient(KisLoggable):
    """한국투자증권 실시간 클라이언트"""

    key: KisKey
    """한국투자증권 API Key"""
    client: KisClient
    """한국투자증권 API Key"""
    ws: WebSocketApp
    """웹소켓 연결"""
    reconnect: bool = True
    """재접속 여부"""
    reconnect_delay: int = 5
    """재접속 시도 간격"""
    subscribed: set[str]
    """구독 목록"""
    event: KisRTEvent
    """실시간 이벤트"""
    thread: Thread | None = None

    _close: bool = False
    _response_handlers: dict[str, Future | None]
    _encrypts: dict[str, KisRTEncrypt]
    _lock: LockType
    _isreconnect: bool = False

    def __init__(self, client: KisClient, logger: logging.Logger):
        self.key = client.key
        self.client = client
        self._response_handlers = {}
        self._encrypts = {}
        self.subscribed = set()
        self.event = KisRTEvent(self)
        self._lock = Lock()
        self.logger = logger
        self._run()
        self._emit_logger(logger)

    @property
    def connected(self):
        return self.ws and self.ws.sock and self.ws.sock.connected

    def _onmessage(self, ws, data):
        if self.ws != ws:
            return

        if data[0] in ["0", "1"]:
            self._receive_response(data)
        else:
            self._receive_sys_msg(data)

    def _onerror(self, ws, error):
        if self.ws != ws:
            return

        self.logger.info("RTC websocket error: %s", error)
        self._try_reconnect()

    def _onclose(self, ws, close_status_code, close_msg):
        if self.ws != ws:
            return

        self._release_lock()
        self.logger.info("RTC websocket disconnected")
        self._try_reconnect()

    def _onopen(self, ws):
        if self.ws != ws:
            return

        subs = list(self.subscribed)

        self._encrypts.clear()
        self.subscribed.clear()
        self._response_handlers.clear()
        self._release_lock()
        self.logger.info("RTC websocket connected")

        if self._isreconnect:
            self._restore_subscriptions(subs)

    def close(self):
        self._release_lock()
        self._close = True
        self.ws.close()

    def _build_url(self, path: str):
        domain = WEBSOCKET_VIRTUAL_DOMAIN if self.key.virtual_account else WEBSOCKET_REAL_DOMAIN
        return f"{domain}{path}"

    def _run(self):
        if self.thread and self.thread.is_alive():
            if self.connected:
                self.ws.close()

        self.ws = WebSocketApp(
            self._build_url("/tryitout/H0STCNI0"),
            on_message=self._onmessage,
            on_error=self._onerror,
            on_close=self._onclose,
            on_open=self._onopen,
        )

        self._lock.acquire(block=False)
        self.thread = Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def _release_lock(self):
        self._lock.acquire(block=False)
        self._lock.release()

    def _reconnect(self):
        self.logger.info(f"RTC websocket reconnect after {self.reconnect_delay} seconds")
        sleep(self.reconnect_delay)

        if not self._close and not self.connected:
            self._isreconnect = True
            self.logger.info(f"RTC websocket reconnecting...")
            self._run()

    def _try_reconnect(self):
        if self.reconnect and not self._close and not self.connected:
            Thread(target=self._reconnect, daemon=True).start()

    def _restore_subscriptions(self, subs: list[str]):
        for sub in subs:
            tr_id, tr_key = self._dcid(sub)
            self.logger.info("RTC restoring subscription: %s.%s", tr_id, tr_key)
            Thread(
                target=self._send_request,
                args=(tr_id, tr_key, True),
                kwargs={"verbose": True},
                daemon=True,
            ).start()

    def _mkid(self, tr_id: str, tr_key: str):
        return f"{tr_id}.{tr_key}"

    def _dcid(self, sub: str) -> tuple[str, str]:
        return tuple(sub.split("."))

    def _rctst(self):
        self.ws.close()

    def _receive_sys_msg(self, data: str):
        try:
            res = KisRTSysResponse(json.loads(data))

            if res.tr_id == "PINGPONG":
                self.logger.debug("RTC received PINGPONG")
                self.ws.send(data)
                return

            id = self._mkid(res.tr_id, res.tr_key)  # type: ignore
            hh = id in self._response_handlers
            future = self._response_handlers.get(id, None)

            if not future and hh:
                self.logger.warning("RTC received unhandled sysMsg: %s %s", res.msg_cd, res.rt_cd)
                return

            if res.rt_cd == "9":
                self.logger.error("RTC received request error: %s %s", res.msg_cd, res.msg1)
                if future:
                    future.set_exception(Exception(f"{res.msg_cd} {res.msg1}"))
            else:
                self._subman(res)
                if future:
                    future.set_result(res)
        except Exception as e:
            self.logger.error("RTC failed to parse sysMsg: %s, exc: %s", data, e)

    def _subman(self, res: KisRTSysResponse):
        if res.msg_cd or res.tr_key:
            id = self._mkid(res.tr_id, res.tr_key)  # type: ignore
            self._encman(res)
            if res.msg_cd == "OPSP0000":  # subscribed
                self.logger.info("RTC received sysMag: %s.%s subscribed", res.tr_id, res.tr_key)

                if len(self.subscribed) >= REAL_TIME_PRICE_MAX_SUBSCRIPTIONS:
                    self.logger.warning("RTC subscription limit reached.")

                self.subscribed.add(id)
                return
            elif res.msg_cd == "OPSP0001":  # unsubscribed
                self.logger.info("RTC received sysMag: %s.%s unsubscribed", res.tr_id, res.tr_key)
                return
            elif res.msg_cd == "OPSP0002":  # already subscribed
                self.logger.warning(
                    "RTC received sysMag: %s.%s already subscribed", res.tr_id, res.tr_key
                )
                self.subscribed.add(id)
                return
            elif res.msg_cd == "OPSP0003":  # already unsubscribed
                self.logger.warning(
                    "RTC received sysMag: %s.%s already unsubscribed", res.tr_id, res.tr_key
                )
                try:
                    self.subscribed.remove(id)
                except:
                    pass
            elif res.msg_cd == "OPSP0007":  # internal error
                self.logger.critical(
                    "RTC received sysMag: %s.%s INTERNAL ERROR!!", res.tr_id, res.tr_key
                )

        self.logger.warning(
            "RTC received sysMag: unknown response status: %s.%s %s %s",
            res.tr_id,
            res.tr_key,
            res.msg_cd,
            res.msg1,
        )

    def _encman(self, res: KisRTSysResponse):
        if res.tr_id not in ("H0STCNI0", "H0STCNI9") or res.tr_id in self._encrypts:
            return

        if res.msg_cd == "OPSP0002":
            self.logger.critical(
                "RTC received sysMag: %s.%s already subscribed but not have decrypt key.",
                res.tr_id,
                res.tr_key,
            )
            return

        if res.msg_cd == "OPSP0000":
            self._encrypts[res.tr_id] = KisRTEncrypt(res)

    def _receive_response(self, data: str):
        try:
            res = KisRTResponse(data, parse=False)
            res_type = RT_RESPONSES.get(res.tr_id, None)

            if not res_type:
                self.logger.warning("RTC received unhandled response: %s", res.tr_id)
                return

            if res.encrypt:
                enc = self._encrypts.get(res.tr_id, None)

                if not enc:
                    self.logger.warning(
                        "RTC received encrypted response: %s but not have decrypt key.", res.tr_id
                    )
                    return

                res = res_type(data, encrypt=enc)
            else:
                res = res_type(data)

            self.logger.debug("RTC received response: %s %s", res.tr_id, res_type.__name__)
            self.event._emit(res)
        except Exception as e:
            self.logger.error("RTC failed to parse response: %s, exc: %s", data, e)

    def wait_connected(self, timeout: int = 10):
        if self._close:
            raise Exception("RTC websocket closed")

        if self._lock.acquire(block=True, timeout=timeout):
            self._lock.release()

        if not self.connected:
            raise Exception("RTC websocket not connected")

    def _wait_response(self, id: str, timeout: int = 10):
        future = self._response_handlers.get(id, None)
        if not future:
            self._response_handlers[id] = future = Future()
        try:
            (future,) = as_completed([future], timeout=timeout)
            return future.result(timeout=timeout)
        finally:
            if id in self._response_handlers:
                del self._response_handlers[id]

    def _send_request(
        self, tr_id: str, tr_key: str, tr_type: bool, timeout: int = 10, verbose: bool = True
    ) -> KisRTSysResponse | None:
        id = self._mkid(tr_id, tr_key)

        if tr_type:
            if id in self.subscribed:
                return None

            if len(self.subscribed) >= REAL_TIME_PRICE_MAX_SUBSCRIPTIONS:
                raise Exception(f"RTC max subscriptions reached: {REAL_TIME_PRICE_MAX_SUBSCRIPTIONS}")
        else:
            if id not in self.subscribed:
                return None

        self.wait_connected()
        if verbose:
            self.logger.info("RTC sending request: %s %s", "REG" if tr_type else "UNREG", id)
        #  웹소켓 보안강화 대응.
        # self.ws.send(json.dumps(KisRTRequest(self.key, tr_id=tr_id, tr_key=tr_key, tr_type=tr_type).dict()))
        self.ws.send(
            json.dumps(
                KisRTRequest(
                    self.client.ws_approvalkey(), tr_id=tr_id, tr_key=tr_key, tr_type=tr_type
                ).dict()
            )
        )
        return self._wait_response(id, timeout)  # type: ignore

    def register(self, tr_id: str, tr_key: str, timeout: int = 10) -> KisRTSysResponse | None:
        return self._send_request(tr_id, tr_key, True, timeout=timeout)

    def unregister(self, tr_id: str, tr_key: str, timeout: int = 10) -> KisRTSysResponse | None:
        return self._send_request(tr_id, tr_key, False, timeout=timeout)

    def add(self, id: RT_CODE_TYPE, tr_key: str, timeout: int = 10) -> KisRTSysResponse | None:
        """실시간 응답을 등록합니다.

        Args:
            id (Literal['체결가', '호가', '체결']): 등록할 실시간 코드.
            tr_key (str): 체결가, 호가의 경우 종목코드. 체결의 경우 KIS 아이디 (ex: 000660 or kth****)
            timeout (int, optional): 응답 대기 시간. Defaults to 10.

        Raises:
            KeyError: 등록할 실시간 코드가 잘못되었습니다.

        Examples:
            >>> kis.rtclient.add('체결가', '000660')
            >>> kis.rtclient.add('호가', '000660')
            >>> kis.rtclient.add('체결', 'kth****')

        Returns:
            KisRTSysResponse: 등록 응답.
            None: 이미 등록되어 있습니다.
        """
        return self.register(_rtcd(id, self.key.virtual_account), tr_key, timeout=timeout)

    def remove(
        self, id: RT_CODE_TYPE, tr_key: str | None = None, timeout: int = 10
    ) -> KisRTSysResponse | None:
        """실시간 응답을 해제합니다.

        Args:
            id (Literal['체결가', '호가', '체결']): 해제할 실시간 코드
            tr_key (str | None): 체결가, 호가의 경우 종목코드. 체결의 경우 KIS 아이디 (ex: 000660 or kth****) None일 경우 모든 종목 해제. Defaults to None.
            timeout (int, optional): 응답 대기 시간. Defaults to 10.

        Examples:
            >>> kis.rtclient.remove('체결가', '000660')
            >>> kis.rtclient.remove('호가', '000660')
            >>> kis.rtclient.remove('체결')

        Returns:
            KisRTSysResponse: 등록 해제 응답.
            None: 만약 tr_key가 None이 아니라면 해당 종목이 등록되어 있지 않습니다.
        """
        tr_id = _rtcd(id, self.key.virtual_account)

        if tr_key is None:
            for key in self.subscribed:
                tid, tr_key = self._dcid(key)

                if tid != tr_id:
                    continue

                self.unregister(tr_id, tr_key, timeout=timeout)
        else:
            return self.unregister(tr_id, tr_key, timeout=timeout)

    def remove_all(self, timeout: int = 10) -> list[KisRTSysResponse]:
        """모든 실시간 응답을 해제합니다.

        Args:
            timeout (int, optional): 응답 대기 시간. Defaults to 10.
        """
        res = []

        for id in self.subscribed:
            r = self.unregister(*self._dcid(id), timeout=timeout)
            if r:
                res.append(r)

        return res
