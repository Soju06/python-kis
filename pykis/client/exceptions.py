from collections import namedtuple
from typing import Any
from urllib.parse import parse_qs, urlparse

from requests import Response

from pykis.__env__ import TRACE_DETAIL_ERROR

__all__ = [
    "KisException",
    "KisHTTPError",
    "KisAPIError",
]


def safe_request_data(response: Response):
    header = dict(response.request.headers)

    if "appkey" in header:
        header["appkey"] = "***"
    if "appsecret" in header:
        header["appsecret"] = "***"
    if "Authorization" in header:
        header["Authorization"] = f'{header["Authorization"].split()[0]} ***'

    if response.request.body:
        body = response.request.body

        if isinstance(body, memoryview):
            body = body.tobytes()

        if isinstance(body, (bytes, bytearray)):
            try:
                body = body.decode("utf-8")
            except UnicodeDecodeError:
                body = body.reason.decode("iso-8859-1")  # type: ignore

        if not TRACE_DETAIL_ERROR and ("appkey" in body or "appsecret" in body or "secretkey" in body):
            body = "[PROTECTED BODY]"
    else:
        body = "[EMPTY BODY]"

    url = urlparse(response.request.url)
    params = str(parse_qs(url.query)) or "[EMPTY PARAMS]"  # type: ignore
    url = url._replace(query="")

    return namedtuple("SafeRequestData", ["url", "header", "params", "body"])(
        url=url,
        header=header,
        params=params,
        body=body,
    )


class KisException(Exception):
    """PyKis 예외 베이스 클래스"""

    status_code: int
    """HTTP 상태 코드"""
    response: Response
    """응답 객체"""

    def __init__(self, message: str, response: Response):
        super().__init__(message)
        self.status_code = response.status_code
        self.response = response


class KisHTTPError(KisException):
    """HTTP 예외 베이스 클래스"""

    reason: str
    """응답 메시지"""
    text: str
    """응답 본문"""

    def __init__(self, response: Response):
        req = safe_request_data(response)
        text = response.text

        super().__init__(
            "HTTP 요청에 실패했습니다.\n"
            f"({response.status_code}) {response.reason}\n"
            f"{text}\n\n"
            f"[  Request  ]: {response.request.method} {req.url.geturl()}\n"
            f"Headers: {req.header}\n"
            f"Params: {req.params}\n"
            f"Body: {req.body}",
            response=response,
        )
        self.reason = response.reason
        self.text = text


class KisAPIError(KisException):
    """API 예외 베이스 클래스"""

    data: dict[str, Any]
    """응답 데이터"""
    rt_cd: int | None
    """응답 코드"""
    tr_id: str | None
    """거래 ID"""
    gt_uid: str | None
    """거래고유번호"""
    msg_cd: str | None
    """응답 메시지 코드"""
    msg1: str | None
    """응답 메시지"""

    @property
    def message(self) -> str:
        """응답 메시지"""
        return self.msg1 or self.response.reason

    @property
    def code(self) -> int:
        """응답 코드"""
        return self.rt_cd or 0

    @property
    def error_code(self) -> str:
        """응답 메시지 코드"""
        return self.msg_cd or "UNKNOWN"

    @property
    def transaction_id(self) -> str:
        """거래 ID"""
        return self.tr_id or "UNKNOWN"

    @property
    def transaction_unique_id(self) -> str:
        """거래고유번호"""
        return self.gt_uid or "UNKNOWN"

    def __init__(self, data: dict, response: Response):
        rt_cd = data.get("rt_cd")
        rt_cd = int(rt_cd) if rt_cd else None
        tr_id = response.headers.get("tr_id")
        gt_uid = response.headers.get("gt_uid")
        msg_cd = data.get("msg_cd")
        msg1 = data.get("msg1", "").strip()
        req = safe_request_data(response)

        super().__init__(
            f"KIS API 요청에 실패했습니다.\n"
            f"(RT_CD: {rt_cd}, MSG_CD: {msg_cd}) {tr_id}\n"
            f"{msg1}\n\n"
            f"[  Request  ]: {response.request.method} {req.url.geturl()}\n"
            f"Headers: {req.header}\n"
            f"Params: {req.params}\n"
            f"Body: {req.body}",
            response=response,
        )

        self.data = data
        self.rt_cd = rt_cd
        self.tr_id = tr_id
        self.gt_uid = gt_uid
        self.msg_cd = msg_cd
        self.msg1 = msg1
