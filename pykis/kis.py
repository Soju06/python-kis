from datetime import timedelta
from os import PathLike
from typing import Callable, Iterable, Literal
from urllib.parse import urljoin

import requests
from requests import Response

from pykis import logging
from pykis.__env__ import (
    REAL_API_REQUEST_PER_SECOND,
    REAL_DOMAIN,
    USER_AGENT,
    VIRTUAL_API_REQUEST_PER_SECOND,
    VIRTUAL_DOMAIN,
)
from pykis.api.auth.token import KisAccessToken
from pykis.client.account import KisAccountNumber
from pykis.client.appkey import KisKey
from pykis.client.auth import KisAuth
from pykis.client.cache import KisCacheStorage
from pykis.client.exception import KisHTTPError
from pykis.client.form import KisForm
from pykis.client.object import KisObjectBase
from pykis.responses.dynamic import KisObject, TDynamic
from pykis.responses.types import KisDynamicDict
from pykis.utils.rate_limit import RateLimiter
from pykis.utils.thread_safe import thread_safe


class PyKis:
    """한국투자증권 API"""

    appkey: KisKey
    """한국투자증권 API AppKey"""
    primary_account: KisAccountNumber | None
    """한국투자증권 기본 계좌 정보"""
    virtual: bool
    """모의투자 여부"""

    cache: KisCacheStorage
    """캐시 저장소"""

    _rate_limiters: dict[str, RateLimiter]
    _token: KisAccessToken | None

    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        *,
        account: str | KisAccountNumber | None = None,
        appkey: str | KisKey | None = None,
        secretkey: str | None = None,
        virtual: bool = False,
        token: KisAccessToken | str | PathLike[str] | None = None,
    ):
        """한국투자증권 API를 생성합니다.

        Args:
            auth: 한국투자증권 계좌 및 인증 정보
            appkey: 한국투자증권 API AppKey
            secretkey: 한국투자증권 API AppSecret
            account: 한국투자증권 기본 계좌 정보
            virtual: 모의투자 여부

            token: 한국투자증권 API 접속 토큰
        """
        if auth is not None:
            if not isinstance(auth, KisAuth):
                auth = KisAuth.load(auth)

            appkey = auth.key
            account = auth.account_
            virtual = auth.virtual

        if appkey is None:
            raise ValueError("appkey를 입력해야 합니다.")

        if isinstance(appkey, str):
            if secretkey is None:
                raise ValueError("secretkey를 입력해야 합니다.")

            appkey = KisKey(appkey=appkey, secretkey=secretkey)

        self.appkey = appkey

        if isinstance(account, str):
            account = KisAccountNumber(account)

        self.primary_account = account
        self.virtual = virtual

        self.cache = KisCacheStorage()

        self._rate_limiters = {
            "real": RateLimiter(REAL_API_REQUEST_PER_SECOND, 1),
            "virtual": RateLimiter(VIRTUAL_API_REQUEST_PER_SECOND, 1),
        }
        self._token = (
            token if isinstance(token, KisAccessToken) else KisAccessToken.load(token) if token else None
        )

    def _rate_limit_exceeded(self):
        logging.logger.warning("API 호출 횟수를 초과하여 호출 유량 획득까지 대기합니다.")

    def request(
        self,
        path: str,
        *,
        method: Literal["GET", "POST"] = "GET",
        params: dict[str, str] | None = None,
        body: dict[str, str] | None = None,
        form: Iterable[KisForm | None] | None = None,
        headers: dict[str, str] | None = None,
        domain: Literal["real", "virtual"] | None = None,
        appkey_location: Literal["header", "body"] | None = "header",
        form_location: Literal["header", "params", "body"] | None = None,
        auth: bool = True,
    ) -> Response:
        if method == "GET":
            if body is not None:
                raise ValueError("GET 요청에는 body를 입력할 수 없습니다.")

            if appkey_location == "body":
                raise ValueError("GET 요청에는 appkey_location을 header로 설정해야 합니다.")
        elif body is None:
            body = {}

        if headers is None:
            headers = {}

        if domain is None:
            domain = "virtual" if self.virtual else "real"

        if appkey_location:
            self.appkey.build(headers if appkey_location == "header" else body)

        if auth:
            self.token.build(headers)

        if form is not None:
            if form_location is None:
                form_location = "params" if method == "GET" else "body"

            dist = headers if form_location == "header" else params if form_location == "params" else body

            for f in form:
                if f is not None:
                    f.build(dist)

        headers["User-Agent"] = USER_AGENT

        rate_limit = self._rate_limiters[domain]

        while True:
            rate_limit.acquire(blocking_callback=self._rate_limit_exceeded)

            resp = requests.request(
                method=method,
                url=urljoin(REAL_DOMAIN if domain == "real" else VIRTUAL_DOMAIN, path),
                headers=headers,
                params=params,
                json=body,
            )

            if resp.ok:
                return resp

            try:
                data = resp.json()
            except:
                data = None

            # Rate limit exceeded
            if resp.status_code != 500 or not data or data.get("msg_cd") != "EGW00201":
                raise KisHTTPError(response=resp)

            logging.logger.warning("API 호출 횟수를 초과하였습니다.")

    def fetch(
        self,
        path: str,
        *,
        method: Literal["GET", "POST"] = "GET",
        params: dict[str, str] | None = None,
        body: dict[str, str] | None = None,
        form: Iterable[KisForm | None] | None = None,
        headers: dict[str, str] | None = None,
        domain: Literal["real", "virtual"] | None = None,
        appkey_location: Literal["header", "body"] | None = "header",
        form_location: Literal["header", "params", "body"] | None = None,
        auth: bool = True,
        api: str | None = None,
        continuous: bool = False,
        response_type: TDynamic | type[TDynamic] | Callable[[], TDynamic] = KisDynamicDict,
        verbose: bool = True,
    ) -> TDynamic:
        if api is not None:
            if headers is None:
                headers = {}

            headers["tr_id"] = api

        if continuous:
            if headers is None:
                headers = {}

            headers["tr_cont"] = "N"

        response = self.request(
            path,
            method=method,
            params=params,
            body=body,
            form=form,
            headers=headers,
            domain=domain,
            appkey_location=appkey_location,
            form_location=form_location,
            auth=auth,
        )

        data = response.json()
        data["__response__"] = response

        if verbose:
            logging.logger.debug(
                f"API [%s]: %s, %s -> %s:%s (%s)",
                api or path,
                params or ".",
                body or ".",
                data.get("rt_cd", "."),
                data.get("msg_cd", "."),
                data.get("msg1", ".").strip(),
            )

        response_object = KisObject.transform_(
            data=data,
            transform_type=response_type,
            ignore_missing_fields={"__response__"},
        )

        if isinstance(response_object, KisObjectBase):
            response_object.__kis_init__(self)
            response_object.__kis_post_init__()

        return response_object  # type: ignore

    @property
    @thread_safe("token")
    def token(self) -> KisAccessToken:
        """API 접속 토큰을 반환합니다."""
        if self._token is None or self._token.remaining < timedelta(minutes=10):
            from pykis.api.auth.token import token_issue

            self._token = token_issue(self)
            logging.logger.debug(f"API 접속 토큰을 발급했습니다.")

        return self._token

    @token.setter
    @thread_safe("token")
    def token(self, token: KisAccessToken):
        """API 접속 토큰을 설정합니다."""
        self._token = token

    def discard(self):
        """API 접속 토큰을 폐기합니다."""
        if self._token is not None:
            from pykis.api.auth.token import token_revoke

            token_revoke(self, self._token.token)
            self._token = None

    @property
    def primary(self) -> KisAccountNumber:
        """
        기본 계좌 정보를 반환합니다.

        Raises:
            ValueError: 기본 계좌 정보가 없을 경우
        """
        if self.primary_account is None:
            raise ValueError("기본 계좌 정보가 없습니다.")

        return self.primary_account

    from pykis.scope.account.account import account
    from pykis.scope.stock.info_stock import info_stock as stock
