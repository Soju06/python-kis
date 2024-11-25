import hashlib
from datetime import timedelta
from os import PathLike
from pathlib import Path
from time import sleep
from typing import Callable, Iterable, Literal, overload
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
from pykis.client.exceptions import KisHTTPError
from pykis.client.form import KisForm
from pykis.client.object import KisObjectBase, kis_object_init
from pykis.client.websocket import KisWebsocketClient
from pykis.responses.dynamic import KisObject, TDynamic
from pykis.responses.types import KisDynamicDict
from pykis.utils.rate_limit import RateLimiter
from pykis.utils.thread_safe import thread_safe
from pykis.utils.workspace import get_cache_path


class PyKis:
    """한국투자증권 API"""

    appkey: KisKey
    """한국투자증권 실전도메인 API AppKey"""
    virtual_appkey: KisKey | None
    """한국투자증권 API AppKey"""
    primary_account: KisAccountNumber | None
    """한국투자증권 기본 계좌 정보"""

    @property
    def virtual(self) -> bool:
        """모의도메인 여부"""
        return self.virtual_appkey is not None

    cache: KisCacheStorage
    """캐시 저장소"""

    _rate_limiters: dict[str, RateLimiter]
    """API 호출 제한"""
    _token: KisAccessToken | None
    """실전투자 API 접속 토큰"""
    _virtual_token: KisAccessToken | None
    """API 접속 토큰"""
    _websocket: KisWebsocketClient | None
    """웹소켓 클라이언트"""
    _keep_token: Path | None
    """API 접속 토큰 자동 저장 경로"""
    _sessions: dict[Literal["real", "virtual"], requests.Session]
    """API 세션"""

    @property
    def keep_token(self) -> bool:
        """API 접속 토큰 자동 저장 여부"""
        return self._keep_token is not None

    @overload
    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 실전투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.pykis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            파일로 저장된 인증 정보를 불러와 PyKis 객체를 생성합니다.

            먼저, 인증 정보를 저장합니다.

            >>> auth = KisAuth(
            ...     id="soju06",                # HTS 로그인 ID
            ...     account="00000000-01",      # 계좌번호
            ...     appkey="PSED321z...",       # AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # SecretKey 180자리
            ... )
            >>> auth.save("pykis_auth.json")

            그 후, 저장된 인증 정보를 불러와 PyKis 객체를 생성합니다.

            >>> kis = PyKis(
            ...     "pykis_auth.json",          # 인증 정보 파일 경로
            ...     keep_token=True             # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    @overload
    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        virtual_auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        token: KisAccessToken | str | PathLike[str] | None = None,
        virtual_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 모의투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            virtual_auth (str | PathLike[str] | KisAuth | None, optional): 모의도메인 인증 정보.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            virtual_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.pykis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            먼저, 실전투자 인증 정보를 저장합니다.

            >>> real_auth = KisAuth(
            ...     id="soju06",                # HTS 로그인 ID
            ...     account="00000000-01",      # 계좌번호
            ...     appkey="PSED321z...",       # AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # SecretKey 180자리
            ... )
            >>> real_auth.save("pykis_real_auth.json")

            그 다음, 모의투자 인증 정보를 저장합니다.

            >>> virtual_auth = KisAuth(
            ...     id="soju06",                # 모의투자 HTS 로그인 ID
            ...     account="00000000-01",      # 모의투자 계좌번호
            ...     appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
            ...     virtual=True,               # 모의투자 여부
            ... )
            >>> virtual_auth.save("pykis_virtual_auth.json")

            그 후, 저장된 인증 정보를 불러와 PyKis 객체를 생성합니다.

            >>> kis = PyKis(
            ...     "pykis_real_auth.json",     # 실전투자 인증 정보 파일 경로
            ...     "pykis_virtual_auth.json",  # 모의투자 인증 정보 파일 경로
            ...     keep_token=True             # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    @overload
    def __init__(
        self,
        /,
        *,
        id: str | None = None,
        account: str | KisAccountNumber | None = None,
        appkey: str | KisKey | None = None,
        secretkey: str | None = None,
        token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
    ):
        """
        실전투자용 한국투자증권 API를 생성합니다.

        Args:
            id (str | None, optional): API ID.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            appkey (str | KisKey | None, optional): API 실전도메인 AppKey.
            secretkey (str | None, optional): API 실전도메인 SecretKey.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.pykis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            인증 정보를 입력하여 PyKis 객체를 생성합니다.

            >>> kis = PyKis(
            ...     id="soju06",                        # HTS 로그인 ID
            ...     account="00000000-01",              # 계좌번호
            ...     appkey="PSED321z...",               # AppKey 36자리
            ...     secretkey="RR0sFMVB...",            # SecretKey 180자리
            ...     keep_token=True,                    # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    @overload
    def __init__(
        self,
        /,
        *,
        id: str | None = None,
        account: str | KisAccountNumber | None = None,
        appkey: str | KisKey | None = None,
        secretkey: str | None = None,
        token: KisAccessToken | str | PathLike[str] | None = None,
        virtual_id: str | None = None,
        virtual_appkey: str | KisKey | None = None,
        virtual_secretkey: str | None = None,
        virtual_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
    ):
        """
        모의투자용 한국투자증권 API를 생성합니다.

        Args:
            id (str | None, optional): API ID.
            appkey (str | KisKey | None, optional): API 실전도메인 AppKey.
            secretkey (str | None, optional): API 실전도메인 SecretKey.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            virtual_id (str | None, optional): 모의도메인 API ID.
            virtual_appkey (str | KisKey | None, optional): 모의도메인 API AppKey.
            virtual_secretkey (str | None, optional): 모의도메인 API SecretKey.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            virtual_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.pykis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            인증 정보를 입력하여 모의 투자용 PyKis 객체를 생성합니다.

            >>> kis = PyKis(
            ...     id="soju06",                        # HTS 로그인 ID
            ...     account="00000000-01",              # 모의투자 계좌번호
            ...     appkey="PSED321z...",               # 실전투자 AppKey 36자리
            ...     secretkey="RR0sFMVB...",            # 실전투자 SecretKey 180자리
            ...     virtual_id="soju06",                # 모의투자 HTS 로그인 ID
            ...     virtual_appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     virtual_secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
            ...     keep_token=True,                    # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    @overload
    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        account: str | KisAccountNumber | None = None,
        token: KisAccessToken | str | PathLike[str] | None = None,
        virtual_id: str | None = None,
        virtual_appkey: str | KisKey | None = None,
        virtual_secretkey: str | None = None,
        virtual_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 모의투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            virtual_id (str | None, optional): 모의도메인 API ID.
            virtual_appkey (str | KisKey | None, optional): 모의도메인 API AppKey.
            virtual_secretkey (str | None, optional): 모의도메인 API SecretKey.
            virtual_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.pykis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            파일로 저장된 인증 정보를 불러와 모의투자용 PyKis 객체를 생성합니다.

            먼저, 실전투자 인증 정보를 저장합니다.

            >>> real_auth = KisAuth(
            ...     id="soju06",                        # HTS 로그인 ID
            ...     account="00000000-01",              # 모의투자 계좌번호
            ...     appkey="PSED321z...",               # AppKey 36자리
            ...     secretkey="RR0sFMVB...",            # SecretKey 180자리
            ... )
            >>> real_auth.save("pykis_real_auth.json")

            그 후, 저장된 인증 정보를 불러와 모의투자용 PyKis 객체를 생성합니다.

            >>> kis = PyKis(
            ...     "pykis_real_auth.json",             # 실전투자 인증 정보 파일 경로
            ...     virtual_id="soju06",                # 모의투자 HTS 로그인 ID
            ...     virtual_appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     virtual_secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
            ...     keep_token=True,                    # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        virtual_auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        account: str | KisAccountNumber | None = None,
        id: str | None = None,
        appkey: str | KisKey | None = None,
        secretkey: str | None = None,
        token: KisAccessToken | str | PathLike[str] | None = None,
        virtual_id: str | None = None,
        virtual_appkey: str | KisKey | None = None,
        virtual_secretkey: str | None = None,
        virtual_token: KisAccessToken | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        keep_token: bool | str | PathLike[str] | None = None,
    ):
        if auth is not None:
            if not isinstance(auth, KisAuth):
                auth = KisAuth.load(auth)

            if auth.virtual:
                raise ValueError("auth에는 실전도메인 인증 정보를 입력해야 합니다.")

            id = auth.id
            appkey = auth.key
            account = auth.account_number

        if virtual_auth is not None:
            if not isinstance(virtual_auth, KisAuth):
                virtual_auth = KisAuth.load(virtual_auth)

            if not virtual_auth.virtual:
                raise ValueError("virtual_auth에는 모의도메인 인증 정보를 입력해야 합니다.")

            virtual_id = virtual_auth.id
            virtual_appkey = virtual_auth.key
            account = virtual_auth.account_number

        virtual = virtual_appkey is not None and virtual_auth is not None

        if id is None:
            raise ValueError("id를 입력해야 합니다.")

        if appkey is None:
            raise ValueError("appkey를 입력해야 합니다.")

        if virtual and virtual_id is None:
            raise ValueError("virtual_id를 입력해야 합니다.")

        if virtual and virtual_appkey is None:
            raise ValueError("virtual_appkey를 입력해야 합니다.")

        if isinstance(appkey, str):
            if secretkey is None:
                raise ValueError("secretkey를 입력해야 합니다.")

            appkey = KisKey(
                id=id,
                appkey=appkey,
                secretkey=secretkey,
            )

        self.appkey = appkey

        if isinstance(virtual_appkey, str):
            if virtual_secretkey is None:
                raise ValueError("primary_secretkey를 입력해야 합니다.")

            virtual_appkey = KisKey(
                id=id,
                appkey=virtual_appkey,
                secretkey=virtual_secretkey,
            )

        self.virtual_appkey = virtual_appkey

        if isinstance(account, str):
            account = KisAccountNumber(account)

        self.primary_account = account

        self._websocket = KisWebsocketClient(self) if use_websocket else None
        self.cache = KisCacheStorage()

        self._rate_limiters = {
            "real": RateLimiter(REAL_API_REQUEST_PER_SECOND, 1),
            "virtual": RateLimiter(VIRTUAL_API_REQUEST_PER_SECOND, 1),
        }
        self._token = token if isinstance(token, KisAccessToken) else KisAccessToken.load(token) if token else None
        self._virtual_token = (
            virtual_token
            if isinstance(virtual_token, KisAccessToken)
            else KisAccessToken.load(virtual_token) if self.virtual and virtual_token else None
        )
        self._sessions = {
            "real": requests.Session(),
            "virtual": requests.Session(),
        }

        for session in self._sessions.values():
            session.headers.update({"User-Agent": USER_AGENT})

        if keep_token:
            if keep_token is True:
                keep_token = get_cache_path()

            self._keep_token = Path(keep_token).resolve()
            self._load_cached_token(self._keep_token)
        else:
            self._keep_token = None

    def _get_hashed_token_name(self, domain: Literal["real", "virtual"]) -> str:
        appkey = self.appkey if domain == "real" else self.virtual_appkey

        if appkey is None:
            raise ValueError("모의도메인 AppKey가 없습니다.")

        hash = hashlib.sha1(f"pykis{appkey.id}{appkey.appkey}{appkey.secretkey}token".encode()).hexdigest()

        return f"token_{domain}_{self.appkey.id}_{hash}.json"

    def _load_cached_token(self, token_dir: str | PathLike[str] | Path) -> None:
        if not isinstance(token_dir, Path):
            token_dir = Path(token_dir)

        token_dir = token_dir.resolve()
        virtual_token_path = token_dir / self._get_hashed_token_name("real")

        if virtual_token_path.exists():
            try:
                self.token = KisAccessToken.load(virtual_token_path)
                logging.logger.debug(f"실전도메인 API 접속 토큰을 불러왔습니다.")
            except:
                pass

        if self.virtual:
            virtual_token_path = token_dir / self._get_hashed_token_name("virtual")

            if virtual_token_path.exists():
                try:
                    self.primary_token = KisAccessToken.load(virtual_token_path)
                    logging.logger.debug(f"모의도메인 API 접속 토큰을 불러왔습니다.")
                except:
                    pass

    def _save_cached_token(
        self,
        token_dir: str | PathLike[str] | Path,
        domain: Literal["real", "virtual"] | None = None,
        force: bool = False,
    ):
        if not isinstance(token_dir, Path):
            token_dir = Path(token_dir)

        token_dir = token_dir.resolve()
        token_dir.mkdir(parents=True, exist_ok=True)

        if domain is None or domain == "real":
            token = self.token if force else self._token

            if token is not None:
                token.save(token_dir / self._get_hashed_token_name("real"))
                logging.logger.debug(f"실전도메인 API 접속 토큰을 저장했습니다.")

        if self.virtual and (domain is None or domain == "virtual"):
            virtual_token = self.primary_token if force else self._virtual_token

            if virtual_token is not None:
                virtual_token.save(token_dir / self._get_hashed_token_name("virtual"))
                logging.logger.debug(f"모의도메인 API 접속 토큰을 저장했습니다.")

    def _rate_limit_exceeded(self) -> None:
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

        request_headers = headers.copy() if headers else {}

        if domain is None:
            domain = "virtual" if self.virtual else "real"

        session = self._sessions[domain]

        if appkey_location:
            appkey = self.appkey if domain == "real" else self.virtual_appkey

            if appkey is None:
                raise ValueError("모의도메인 AppKey가 없습니다.")

            appkey.build(request_headers if appkey_location == "header" else body)

        if form is not None:
            if form_location is None:
                form_location = "params" if method == "GET" else "body"

            dist = request_headers if form_location == "header" else params if form_location == "params" else body

            for f in form:
                if f is not None:
                    f.build(dist)

        rate_limit = self._rate_limiters[domain]

        while True:
            rate_limit.acquire(blocking_callback=self._rate_limit_exceeded)

            if auth:
                (self.token if domain == "real" else self.primary_token).build(request_headers)

            resp = session.request(
                method=method,
                url=urljoin(REAL_DOMAIN if domain == "real" else VIRTUAL_DOMAIN, path),
                headers=request_headers,
                params=params,
                json=body,
            )

            if resp.ok:
                return resp

            try:
                data = resp.json()
            except Exception:
                data = None

            error_code = data.get("msg_cd") if data is not None else None

            match error_code:
                case "EGW00201":
                    # Rate limit exceeded
                    logging.logger.warning("API 호출 횟수를 초과하였습니다.")
                    sleep(0.1)
                    continue

                case "EGW00123":
                    # Token expired
                    if domain == "real":
                        self._token = None
                    else:
                        self._virtual_token = None

                case _:
                    raise KisHTTPError(response=resp)

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
            kis_object_init(self, response_object)

        return response_object  # type: ignore

    @property
    @thread_safe("token")
    def token(self) -> KisAccessToken:
        """실전도메인 API 접속 토큰을 반환합니다."""
        if self._token is None or self._token.remaining < timedelta(minutes=10):
            from pykis.api.auth.token import token_issue

            self._token = token_issue(self, domain="real")
            logging.logger.debug(f"실전도메인 API 접속 토큰을 발급했습니다.")

            if self._keep_token:
                self._save_cached_token(self._keep_token, domain="real", force=False)

        return self._token

    @token.setter
    @thread_safe("token")
    def token(self, token: KisAccessToken) -> None:
        """API 접속 토큰을 설정합니다."""
        self._token = token

    @property
    @thread_safe("primary_token")
    def primary_token(self) -> KisAccessToken:
        """API 접속 토큰을 반환합니다."""
        if not self.virtual:
            return self.token

        if self._virtual_token is None or self._virtual_token.remaining < timedelta(minutes=10):
            from pykis.api.auth.token import token_issue

            self._virtual_token = token_issue(self, domain="virtual")
            logging.logger.debug(f"모의도메인 API 접속 토큰을 발급했습니다.")

            if self._keep_token:
                self._save_cached_token(self._keep_token, domain="virtual", force=False)

        return self._virtual_token

    @primary_token.setter
    @thread_safe("primary_token")
    def primary_token(self, token: KisAccessToken) -> None:
        """API 접속 토큰을 설정합니다."""
        self._virtual_token = token

    def discard(self, domain: Literal["real", "virtual"] | None = None) -> None:
        """API 접속 토큰을 폐기합니다."""
        from pykis.api.auth.token import token_revoke

        if self._token is not None and (domain is None or domain == "real"):
            token_revoke(self, self._token.token)
            self._token = None

        if self._virtual_token is not None and (domain is None or (domain == "virtual" and self.virtual)):
            token_revoke(self, self._virtual_token.token)
            self._virtual_token = None

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

    @property
    def websocket(self) -> KisWebsocketClient:
        """웹소켓 클라이언트를 반환합니다."""
        if self._websocket is None:
            raise ValueError("웹소켓 클라이언트가 초기화되지 않았습니다.")

        return self._websocket

    def close(self) -> None:
        """API 세션을 종료합니다."""
        for session in self._sessions.values():
            session.close()

    def __del__(self) -> None:
        """API 세션을 종료합니다."""
        self.close()

    from pykis.api.stock.trading_hours import trading_hours
    from pykis.scope.account import account
    from pykis.scope.stock import stock
