import hashlib
from collections.abc import Callable, Iterable
from datetime import timedelta
from os import PathLike
from pathlib import Path
from time import sleep
from typing import Literal, TypeVar, overload
from urllib.parse import urljoin

import requests
from requests import Response

from vmkis import logging
from vmkis.__env__ import (
    API_RETRY_INITIAL_DELAY,
    API_RETRY_MAX_ATTEMPTS,
    API_RETRY_MAX_DELAY,
    API_TOKEN_REISSUE_LIMIT,
    LIVE_API_REQUEST_PER_SECOND,
    LIVE_DOMAIN,
    PAPER_API_REQUEST_PER_SECOND,
    PAPER_DOMAIN,
    USER_AGENT,
    WEBSOCKET_LIVE_DOMAIN,
    WEBSOCKET_PAPER_DOMAIN,
)
from vmkis.api.auth.token import KisAccessToken
from vmkis.client.account import KisAccountNumber
from vmkis.client.appkey import KisKey
from vmkis.client.auth import KisAuth
from vmkis.client.cache import KisCacheStorage
from vmkis.client.endpoint import KisEndpoint
from vmkis.client.exceptions import KisAuthenticationError, KisHTTPError, KisRateLimitError
from vmkis.client.form import KisForm
from vmkis.client.object import KisObjectBase, kis_object_init
from vmkis.client.page import KisPage
from vmkis.client.websocket import KisWebsocketClient
from vmkis.config import Endpoint
from vmkis.responses.dynamic import KisDynamic, KisObject, TDynamic
from vmkis.responses.response import KisPaginationAPIResponseProtocol
from vmkis.responses.types import KisDynamicDict
from vmkis.utils.rate_limit import RateLimiter
from vmkis.utils.retry import RetryConfig
from vmkis.utils.thread_safe import thread_safe
from vmkis.utils.workspace import get_cache_path

# 전역 `retry_config` 싱글턴을 쓰지 않고 전용 인스턴스를 둡니다.
# `with_retry` 데코레이터가 그 싱글턴을 제자리에서 변형하므로, 공유하면
# 데코레이터를 한 번 쓰는 순간 이쪽 정책까지 바뀝니다.
_REQUEST_RETRY_POLICY = RetryConfig(
    max_retries=API_RETRY_MAX_ATTEMPTS,
    initial_delay=API_RETRY_INITIAL_DELAY,
    max_delay=API_RETRY_MAX_DELAY,
    exponential_base=2.0,
    jitter=True,
)


TPagination = TypeVar("TPagination", bound=KisPaginationAPIResponseProtocol)

MAX_PAGES = 100
"""연속조회 상한.

서버가 `is_last` 를 끝내 주지 않거나 커서가 진행하지 않으면 루프가 끝나지
않습니다. 조용히 도는 것보다 명시적으로 실패하는 편이 낫습니다.
"""


class VmKis:
    """한국투자증권 API"""

    appkey: KisKey
    """한국투자증권 실전도메인 API AppKey"""
    paper_appkey: KisKey | None
    """한국투자증권 API AppKey"""
    primary_account: KisAccountNumber | None
    """한국투자증권 기본 계좌 정보"""

    @property
    def paper(self) -> bool:
        """모의도메인 여부"""
        return self.paper_appkey is not None

    cache: KisCacheStorage
    """캐시 저장소"""

    _rate_limiters: dict[str, RateLimiter]
    """API 호출 제한"""
    _token: KisAccessToken | None
    """실전투자 API 접속 토큰"""
    _paper_token: KisAccessToken | None
    """API 접속 토큰"""
    _websocket: KisWebsocketClient | None
    """웹소켓 클라이언트"""
    _keep_token: Path | None
    """API 접속 토큰 자동 저장 경로"""
    _sessions: dict[Literal["live", "paper"], requests.Session]
    """API 세션"""

    @property
    def keep_token(self) -> bool:
        """API 접속 토큰 자동 저장 여부"""
        return self._keep_token is not None

    def base_url(self, domain: Literal["live", "paper"]) -> str:
        """REST 서버 주소. 설정에 재정의가 있으면 그것을, 없으면 기본값을 씁니다.

        벤더가 주소를 바꿔도 사용자가 설정만 고쳐 복구할 수 있게 하는 것이 목적입니다.
        상수를 `from ... import` 로 가져오면 값이 복사되므로, 사용자가 `__env__` 를
        고쳐도 이 모듈은 옛 값을 봅니다 — 그래서 재정의 경로가 필요합니다.
        """
        override = self._endpoints.get(domain)

        if override is not None and override.base_url:
            return override.base_url

        return LIVE_DOMAIN if domain == "live" else PAPER_DOMAIN

    def ws_url(self, domain: Literal["live", "paper"]) -> str:
        """웹소켓 서버 주소. `base_url` 과 같은 규칙입니다."""
        override = self._endpoints.get(domain)

        if override is not None and override.ws_url:
            return override.ws_url

        return WEBSOCKET_LIVE_DOMAIN if domain == "live" else WEBSOCKET_PAPER_DOMAIN

    @overload
    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 실전투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.vmkis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            파일로 저장된 인증 정보를 불러와 VmKis 객체를 생성합니다.

            먼저, 인증 정보를 저장합니다.

            >>> auth = KisAuth(
            ...     id="soju06",                # HTS 로그인 ID
            ...     account="00000000-01",      # 계좌번호
            ...     appkey="PSED321z...",       # AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # SecretKey 180자리
            ... )
            >>> auth.save("vmkis_auth.json")

            그 후, 저장된 인증 정보를 불러와 VmKis 객체를 생성합니다.

            >>> kis = VmKis(
            ...     "vmkis_auth.json",          # 인증 정보 파일 경로
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
        paper_auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        token: KisAccessToken | str | PathLike[str] | None = None,
        paper_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 모의투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            paper_auth (str | PathLike[str] | KisAuth | None, optional): 모의도메인 인증 정보.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            paper_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.vmkis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            먼저, 실전투자 인증 정보를 저장합니다.

            >>> live_auth = KisAuth(
            ...     id="soju06",                # HTS 로그인 ID
            ...     account="00000000-01",      # 계좌번호
            ...     appkey="PSED321z...",       # AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # SecretKey 180자리
            ... )
            >>> live_auth.save("vmkis_live_auth.json")

            그 다음, 모의투자 인증 정보를 저장합니다.

            >>> paper_auth = KisAuth(
            ...     id="soju06",                # 모의투자 HTS 로그인 ID
            ...     account="00000000-01",      # 모의투자 계좌번호
            ...     appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
            ...     paper=True,               # 모의투자 여부
            ... )
            >>> paper_auth.save("vmkis_paper_auth.json")

            그 후, 저장된 인증 정보를 불러와 VmKis 객체를 생성합니다.

            >>> kis = VmKis(
            ...     "vmkis_live_auth.json",     # 실전투자 인증 정보 파일 경로
            ...     "vmkis_paper_auth.json",  # 모의투자 인증 정보 파일 경로
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
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
    ):
        """
        실전투자용 한국투자증권 API를 생성합니다.

        Args:
            id (str | None, optional): API ID.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            appkey (str | KisKey | None, optional): API 실전도메인 AppKey.
            secretkey (str | None, optional): API 실전도메인 SecretKey.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.vmkis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            인증 정보를 입력하여 VmKis 객체를 생성합니다.

            >>> kis = VmKis(
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
        paper_id: str | None = None,
        paper_appkey: str | KisKey | None = None,
        paper_secretkey: str | None = None,
        paper_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
    ):
        """
        모의투자용 한국투자증권 API를 생성합니다.

        Args:
            id (str | None, optional): API ID.
            appkey (str | KisKey | None, optional): API 실전도메인 AppKey.
            secretkey (str | None, optional): API 실전도메인 SecretKey.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            paper_id (str | None, optional): 모의도메인 API ID.
            paper_appkey (str | KisKey | None, optional): 모의도메인 API AppKey.
            paper_secretkey (str | None, optional): 모의도메인 API SecretKey.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            paper_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.vmkis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            인증 정보를 입력하여 모의 투자용 VmKis 객체를 생성합니다.

            >>> kis = VmKis(
            ...     id="soju06",                        # HTS 로그인 ID
            ...     account="00000000-01",              # 모의투자 계좌번호
            ...     appkey="PSED321z...",               # 실전투자 AppKey 36자리
            ...     secretkey="RR0sFMVB...",            # 실전투자 SecretKey 180자리
            ...     paper_id="soju06",                # 모의투자 HTS 로그인 ID
            ...     paper_appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     paper_secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
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
        paper_id: str | None = None,
        paper_appkey: str | KisKey | None = None,
        paper_secretkey: str | None = None,
        paper_token: KisAccessToken | str | PathLike[str] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
    ):
        """
        `KisAuth` 인증 정보를 이용하여 모의투자용 한국투자증권 API를 생성합니다.

        Args:
            auth (str | PathLike[str] | KisAuth | None, optional): 실전도메인 인증 정보.
            account (str | KisAccountNumber | None, optional): 계좌번호.
            token (KisAccessToken | str | PathLike[str] | None, optional): 실전도메인 API 접속 토큰.
            paper_id (str | None, optional): 모의도메인 API ID.
            paper_appkey (str | KisKey | None, optional): 모의도메인 API AppKey.
            paper_secretkey (str | None, optional): 모의도메인 API SecretKey.
            paper_token (KisAccessToken | str | PathLike[str] | None, optional): 모의도메인 API 접속 토큰.
            keep_token (bool | str | PathLike[str] | None, optional): API 접속 토큰을 저장할지 여부. 기본 저장 폴더: `~/.vmkis/` (신뢰할 수 없는 환경에서 사용하지 마세요)
            use_websocket (bool, optional): 웹소켓 사용 여부.

        Examples:

            파일로 저장된 인증 정보를 불러와 모의투자용 VmKis 객체를 생성합니다.

            먼저, 실전투자 인증 정보를 저장합니다.

            >>> live_auth = KisAuth(
            ...     id="soju06",                        # HTS 로그인 ID
            ...     account="00000000-01",              # 모의투자 계좌번호
            ...     appkey="PSED321z...",               # AppKey 36자리
            ...     secretkey="RR0sFMVB...",            # SecretKey 180자리
            ... )
            >>> live_auth.save("vmkis_live_auth.json")

            그 후, 저장된 인증 정보를 불러와 모의투자용 VmKis 객체를 생성합니다.

            >>> kis = VmKis(
            ...     "vmkis_live_auth.json",             # 실전투자 인증 정보 파일 경로
            ...     paper_id="soju06",                # 모의투자 HTS 로그인 ID
            ...     paper_appkey="PSED321z...",       # 모의투자 AppKey 36자리
            ...     paper_secretkey="RR0sFMVB...",    # 모의투자 SecretKey 180자리
            ...     keep_token=True,                    # API 접속 토큰 자동 저장
            ... )

        Raises:
            ValueError: 인증 정보가 올바르지 않을 경우
        """
        ...

    def __init__(
        self,
        auth: str | PathLike[str] | KisAuth | None = None,
        paper_auth: str | PathLike[str] | KisAuth | None = None,
        /,
        *,
        account: str | KisAccountNumber | None = None,
        id: str | None = None,
        appkey: str | KisKey | None = None,
        secretkey: str | None = None,
        token: KisAccessToken | str | PathLike[str] | None = None,
        paper_id: str | None = None,
        paper_appkey: str | KisKey | None = None,
        paper_secretkey: str | None = None,
        paper_token: KisAccessToken | str | PathLike[str] | None = None,
        use_websocket: bool = True,
        user_agent: str | None = None,
        endpoints: dict[str, Endpoint] | None = None,
        keep_token: bool | str | PathLike[str] | None = None,
    ):
        if auth is not None:
            if not isinstance(auth, KisAuth):
                auth = KisAuth.load(auth)

            if auth.paper:
                raise ValueError("auth에는 실전도메인 인증 정보를 입력해야 합니다.")

            id = auth.id
            appkey = auth.key
            account = auth.account_number

        if paper_auth is not None:
            if not isinstance(paper_auth, KisAuth):
                paper_auth = KisAuth.load(paper_auth)

            if not paper_auth.paper:
                raise ValueError("paper_auth에는 모의도메인 인증 정보를 입력해야 합니다.")

            paper_id = paper_auth.id
            paper_appkey = paper_auth.key
            account = paper_auth.account_number

        paper = paper_appkey is not None and paper_auth is not None

        # 모의 인증만 주는 것은 **지원되지 않습니다.** 이 검사가 없으면 아래
        # `id is None` 에 걸려 "id를 입력해야 합니다" 가 나오는데, 그 메시지는
        # 원인을 가립니다 — 사용자는 id 를 주지 않은 적이 없고 모의 인증을
        # 통째로 넘겼기 때문입니다. (이슈 #87)
        #
        # 왜 실전 인증이 필요한가: **시세 TR 은 모의도메인에 없습니다.**
        # `KisEndpoint.tr_paper` 가 `None` 인 엔드포인트는 모의 계좌로 호출해도
        # 실전 도메인으로 나가고, 그때 `self.appkey` 와 실전 토큰을 씁니다.
        # 지금 21개 중 13개가 그렇습니다(시세·차트·상품정보 계열).
        if auth is None and paper_auth is not None:
            raise ValueError(
                "모의 인증만으로는 클라이언트를 만들 수 없습니다. 실전 인증을 첫 번째 "
                "인자로 함께 주세요 — VmKis(live_auth, paper_auth). "
                "시세 TR 은 모의도메인에 없어서 모의 계좌도 실전 도메인으로 나가고, "
                "그때 실전 앱키와 실전 토큰이 필요합니다."
            )

        if id is None:
            raise ValueError("id를 입력해야 합니다.")

        if appkey is None:
            raise ValueError("appkey를 입력해야 합니다.")

        if paper and paper_id is None:
            raise ValueError("paper_id를 입력해야 합니다.")

        if paper and paper_appkey is None:
            raise ValueError("paper_appkey를 입력해야 합니다.")

        if isinstance(appkey, str):
            if secretkey is None:
                raise ValueError("secretkey를 입력해야 합니다.")

            appkey = KisKey(
                id=id,
                appkey=appkey,
                secretkey=secretkey,
            )

        self.appkey = appkey

        if isinstance(paper_appkey, str):
            if paper_secretkey is None:
                raise ValueError("primary_secretkey를 입력해야 합니다.")

            paper_appkey = KisKey(
                id=id,
                appkey=paper_appkey,
                secretkey=paper_secretkey,
            )

        self.paper_appkey = paper_appkey

        if isinstance(account, str):
            account = KisAccountNumber(account)

        self.primary_account = account

        self._websocket = KisWebsocketClient(self) if use_websocket else None
        self.cache = KisCacheStorage()

        self._rate_limiters = {
            "live": RateLimiter(LIVE_API_REQUEST_PER_SECOND, 1),
            "paper": RateLimiter(PAPER_API_REQUEST_PER_SECOND, 1),
        }
        self._token = token if isinstance(token, KisAccessToken) else KisAccessToken.load(token) if token else None
        self._paper_token = (
            paper_token
            if isinstance(paper_token, KisAccessToken)
            else KisAccessToken.load(paper_token)
            if self.paper and paper_token
            else None
        )
        self._sessions = {
            "live": requests.Session(),
            "paper": requests.Session(),
        }

        # 설정에서 온 재정의. 키는 이 모듈의 어휘("live"/"paper")이며,
        # 설정 파일의 live/paper 는 호출부(`vmkis.helpers`)가 번역합니다.
        self._endpoints = endpoints or {}

        for session in self._sessions.values():
            session.headers.update({"User-Agent": user_agent or USER_AGENT})

        if keep_token:
            if keep_token is True:
                keep_token = get_cache_path()

            self._keep_token = Path(keep_token).resolve()
            self._load_cached_token(self._keep_token)
        else:
            self._keep_token = None

    def _get_hashed_token_name(self, domain: Literal["live", "paper"]) -> str:
        appkey = self.appkey if domain == "live" else self.paper_appkey

        if appkey is None:
            raise ValueError("모의도메인 AppKey가 없습니다.")

        hash = hashlib.sha1(f"vmkis{appkey.id}{appkey.appkey}{appkey.secretkey}token".encode()).hexdigest()

        return f"token_{domain}_{self.appkey.id}_{hash}.json"

    def _token_cache_dir(self, token_dir: str | PathLike[str] | Path) -> Path:
        """토큰을 두는 디렉터리.

        `create_client` 는 앱 이름 파일(`configs/token/app_paper_1.json`)을
        `keep_token` 으로 넘깁니다. 예전 코드는 그걸 디렉터리로 `mkdir` 해서
        파일이 이미 있으면 `FileExistsError` 가 났습니다 (#157).
        """
        if not isinstance(token_dir, Path):
            token_dir = Path(token_dir)
        token_dir = token_dir.resolve()
        if token_dir.suffix == ".json" or token_dir.is_file():
            token_dir = token_dir.parent
        token_dir.mkdir(parents=True, exist_ok=True)
        return token_dir

    def _load_cached_token(self, token_dir: str | PathLike[str] | Path) -> None:
        token_dir = self._token_cache_dir(token_dir)
        paper_token_path = token_dir / self._get_hashed_token_name("live")

        if paper_token_path.exists():
            try:
                self.token = KisAccessToken.load(paper_token_path)
                logging.logger.debug("실전도메인 API 접속 토큰을 불러왔습니다.")
            except Exception:
                # 캐시된 토큰이 손상되었거나 형식이 바뀐 경우. 새로 발급받으면 된다.
                pass

        if self.paper:
            paper_token_path = token_dir / self._get_hashed_token_name("paper")

            if paper_token_path.exists():
                try:
                    self.primary_token = KisAccessToken.load(paper_token_path)
                    logging.logger.debug("모의도메인 API 접속 토큰을 불러왔습니다.")
                except Exception:
                    # 캐시된 토큰이 손상되었거나 형식이 바뀐 경우. 새로 발급받으면 된다.
                    pass

    def _save_cached_token(
        self,
        token_dir: str | PathLike[str] | Path,
        domain: Literal["live", "paper"] | None = None,
        force: bool = False,
    ):
        token_dir = self._token_cache_dir(token_dir)

        if domain is None or domain == "live":
            token = self.token if force else self._token

            if token is not None:
                token.save(token_dir / self._get_hashed_token_name("live"))
                logging.logger.debug("실전도메인 API 접속 토큰을 저장했습니다.")

        if self.paper and (domain is None or domain == "paper"):
            paper_token = self.primary_token if force else self._paper_token

            if paper_token is not None:
                paper_token.save(token_dir / self._get_hashed_token_name("paper"))
                logging.logger.debug("모의도메인 API 접속 토큰을 저장했습니다.")

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
        domain: Literal["live", "paper"] | None = None,
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
            domain = "paper" if self.paper else "live"

        session = self._sessions[domain]

        if appkey_location:
            appkey = self.appkey if domain == "live" else self.paper_appkey

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

        # 재시도는 반드시 끝나야 합니다. 예전에는 상한이 없어, 서버가 유량 초과를
        # 계속 반환하면 이 호출이 영원히 반환되지 않았습니다.
        rate_limit_retries = 0
        token_reissues = 0

        while True:
            rate_limit.acquire(blocking_callback=self._rate_limit_exceeded)

            if auth:
                (self.token if domain == "live" else self.primary_token).build(request_headers)

            resp = session.request(
                method=method,
                url=urljoin(self.base_url(domain), path),
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
                    #
                    # 로컬 유량 제한기를 통과했는데도 서버가 초과라고 답하는
                    # 상황입니다(같은 계정을 쓰는 다른 프로세스 등). 고정 간격으로
                    # 되받아치면 상황을 악화시키므로 지수 백오프 + 지터로 물러납니다.
                    if rate_limit_retries >= API_RETRY_MAX_ATTEMPTS:
                        logging.logger.error(
                            f"API 호출 유량 초과가 계속되어 중단합니다. ({API_RETRY_MAX_ATTEMPTS}회 재시도)"
                        )
                        raise KisRateLimitError(response=resp)

                    delay = _REQUEST_RETRY_POLICY.calculate_delay(rate_limit_retries)
                    rate_limit_retries += 1
                    logging.logger.warning(
                        f"API 호출 횟수를 초과하였습니다. "
                        f"{delay:.2f}초 후 재시도 ({rate_limit_retries}/{API_RETRY_MAX_ATTEMPTS})"
                    )
                    sleep(delay)
                    continue

                case "EGW00123":
                    # Token expired
                    #
                    # 재발급 후에도 같은 오류가 나면 만료가 아니라 인증 문제입니다.
                    # 반복해도 결과가 달라지지 않으므로 즉시 실패합니다.
                    if token_reissues >= API_TOKEN_REISSUE_LIMIT:
                        logging.logger.error("토큰을 재발급했는데도 만료 오류가 반복됩니다. 인증 정보를 확인하세요.")
                        raise KisAuthenticationError(response=resp)

                    token_reissues += 1

                    if domain == "live":
                        self._token = None
                    else:
                        self._paper_token = None

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
        domain: Literal["live", "paper"] | None = None,
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
                "API [%s]: %s, %s -> %s:%s (%s)",
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

    def call(
        self,
        endpoint: KisEndpoint,
        *,
        params: dict[str, str] | None = None,
        body: dict[str, str] | None = None,
        form: Iterable[KisForm | None] | None = None,
        page: KisPage | None = None,
        response_type: TDynamic | type[TDynamic] | Callable[[], TDynamic] = KisDynamicDict,
        **kwargs,
    ) -> TDynamic:
        """엔드포인트 스펙으로 API 를 호출합니다.

        `fetch()` 위에 얹은 얇은 층입니다. 흩어져 있던 세 가지 규칙을 여기서만
        처리합니다.

        1. **실전/모의 TR ID 선택** — 예전에는 호출부마다
           `api="VTTC8434R" if self.paper else "TTTC8434R"` 를 적었습니다
        2. **도메인 라우팅** — 모의 미지원 TR 은 실전으로 보냅니다.
           예전에는 `domain="live"` 을 손으로 붙였고, **빠뜨리면 모의 계정에서만
           터지는 버그**가 됐습니다
        3. **커서 길이와 연속조회** — `page.to(100)` / `continuous=not page.is_first`

        Args:
            endpoint: 엔드포인트 스펙
            page: 연속조회 커서. 주면 `endpoint.page_size` 로 길이를 맞추고
                `form` 뒤에 붙입니다. 첫 페이지가 아니면 `continuous=True`.

        `fetch()` 의 나머지 인자는 `**kwargs` 로 그대로 넘어갑니다.
        """
        tr_id, domain = endpoint.resolve(self.paper)

        forms = list(form) if form is not None else []
        continuous = False

        if page is not None:
            if endpoint.page_size is not None:
                page = page.to(endpoint.page_size)

            forms.append(page)
            continuous = not page.is_first

        return self.fetch(
            endpoint.path,
            method=endpoint.method,
            api=tr_id,
            domain=domain,
            params=params,
            body=body,
            form=forms or None,
            continuous=continuous,
            response_type=response_type,
            **kwargs,
        )

    def fetch_pages(
        self,
        endpoint: KisEndpoint,
        *,
        response_type: Callable[[], TPagination],
        merge: Callable[[TPagination, TPagination], None],
        page: KisPage | None = None,
        continuous: bool = True,
        max_pages: int = MAX_PAGES,
        params: dict[str, str] | None = None,
        body: dict[str, str] | None = None,
        form: Iterable[KisForm | None] | None = None,
        **kwargs,
    ) -> TPagination:
        """연속조회를 끝까지 따라가며 결과를 하나로 합칩니다.

        예전에는 이 루프를 엔드포인트마다 각자 복사했습니다(이슈 #44 착수 시점
        8곳). 골격이 전부 같고 **다른 것은 "어느 필드에 누적하는가" 한 줄뿐**
        이었습니다. `continuous` / `is_last` / `next_page` 를 잘못 다루면
        **무한 루프이거나 첫 페이지만 반환**하는데, 둘 다 조용히 틀립니다.

        Args:
            response_type: 응답 객체를 만드는 **팩토리**. 인스턴스가 아닙니다
                (아래 참고).
            merge: `merge(첫_페이지, 다음_페이지)` — 첫 페이지에 누적합니다.
                예: `lambda first, more: first.stocks.extend(more.stocks)`
            continuous: `False` 면 첫 페이지만 가져옵니다.
            max_pages: 상한. 서버가 `is_last` 를 끝내 주지 않아도 여기서 멈춥니다.

        Raises:
            TypeError: `response_type` 에 팩토리가 아니라 인스턴스를 준 경우
            RuntimeError: `max_pages` 를 넘긴 경우

        **왜 팩토리인가.** `KisObject.transform_` 은 인스턴스를 받으면 **그
        인스턴스에 그대로 파싱**합니다. 하나를 돌려 쓰면 모든 페이지가 같은
        객체가 되고, `merge(first, result)` 가 자기 자신을 이어붙여 결과가
        불어납니다. 예전 루프들이 매 반복마다 응답 객체를 새로 만든 이유가
        이것입니다.
        """
        if isinstance(response_type, KisDynamic):
            raise TypeError(
                "response_type 에는 인스턴스가 아니라 팩토리를 주세요. "
                "인스턴스를 주면 모든 페이지가 같은 객체에 파싱되어 결과가 불어납니다. "
                "예: response_type=lambda: KisDomesticBalance(account_number=account)"
            )

        page = page or KisPage.first()
        first: TPagination | None = None

        for _ in range(max_pages):
            result = self.call(
                endpoint,
                params=params,
                body=body,
                form=form,
                page=page,
                response_type=response_type,
                **kwargs,
            )

            if first is None:
                first = result
            else:
                merge(first, result)

            if not continuous or result.is_last:
                return first

            page = result.next_page

        # `KisInternalError` 를 쓰지 않는 이유: 그 예외의 베이스가 `Response` 를
        # 요구하는데 여기에는 건넬 응답이 없습니다.
        raise RuntimeError(
            f"연속조회가 {max_pages}페이지를 넘겼습니다. 서버가 마지막 페이지를 알리지 않았거나 "
            f"커서가 진행하지 않고 있습니다. ({endpoint.path})"
        )

    @property
    @thread_safe("token")
    def token(self) -> KisAccessToken:
        """실전도메인 API 접속 토큰을 반환합니다."""
        if self._token is None or self._token.remaining < timedelta(minutes=10):
            from vmkis.api.auth.token import token_issue

            self._token = token_issue(self, domain="live")
            logging.logger.debug("실전도메인 API 접속 토큰을 발급했습니다.")

            if self._keep_token:
                self._save_cached_token(self._keep_token, domain="live", force=False)

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
        if not self.paper:
            return self.token

        if self._paper_token is None or self._paper_token.remaining < timedelta(minutes=10):
            from vmkis.api.auth.token import token_issue

            self._paper_token = token_issue(self, domain="paper")
            logging.logger.debug("모의도메인 API 접속 토큰을 발급했습니다.")

            if self._keep_token:
                self._save_cached_token(self._keep_token, domain="paper", force=False)

        return self._paper_token

    @primary_token.setter
    @thread_safe("primary_token")
    def primary_token(self, token: KisAccessToken) -> None:
        """API 접속 토큰을 설정합니다."""
        self._paper_token = token

    def discard(self, domain: Literal["live", "paper"] | None = None) -> None:
        """API 접속 토큰을 폐기합니다."""
        from vmkis.api.auth.token import token_revoke

        if self._token is not None and (domain is None or domain == "live"):
            token_revoke(self, self._token.token)
            self._token = None

        if self._paper_token is not None and (domain is None or (domain == "paper" and self.paper)):
            token_revoke(self, self._paper_token.token)
            self._paper_token = None

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
        # `getattr` 로 방어하는 이유: 생성자가 중간에 실패하면(잘못된 인증 정보로
        # `ValueError`) `_sessions` 가 설정되기 전에 객체가 소멸합니다. 그때
        # `__del__` -> `close()` 가 없는 속성을 참조해 AttributeError 를 냅니다.
        # 파이썬이 `__del__` 의 예외를 삼키므로 치명적이지는 않지만, 실행할 때마다
        # PytestUnraisableExceptionWarning 노이즈가 쌓입니다.
        #
        # 이 가드를 걷어내면 `tests/unit/test_kis.py` 의 초기화 실패 테스트 3건이
        # 실패합니다. 예전에는 그 테스트들이 `__del__` 을 무력화해 우회하고 있어서
        # 아무 일도 일어나지 않았습니다(이슈 #42). 지금은 `pyproject.toml` 의
        # `filterwarnings` 가 그 경고를 오류로 올립니다.
        for session in getattr(self, "_sessions", {}).values():
            session.close()

    def __del__(self) -> None:
        """API 세션을 종료합니다."""
        self.close()

    from vmkis.api.stock.trading_hours import trading_hours
    from vmkis.scope.account import account
    from vmkis.scope.stock import stock
