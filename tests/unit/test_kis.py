from unittest.mock import MagicMock, mock_open, patch

import pytest

from vmkis.__env__ import API_RETRY_MAX_ATTEMPTS, API_TOKEN_REISSUE_LIMIT
from vmkis.api.auth.token import KisAccessToken
from vmkis.client.auth import KisAuth
from vmkis.client.exceptions import KisAuthenticationError, KisHTTPError, KisRateLimitError
from vmkis.client.form import KisForm
from vmkis.kis import VmKis
from vmkis.responses.dynamic import KisObject


@pytest.fixture
def mock_kis_auth():
    """KisAuth 객체를 모킹합니다."""
    auth = MagicMock(spec=KisAuth)
    auth.paper = False
    auth.id = "test_id"
    auth.key = MagicMock()
    auth.key.id = "test_id"
    auth.key.appkey = "test_appkey_36chars_long_1234567890"
    auth.key.secretkey = "test_secretkey"
    auth.account_number = "12345678-01"
    return auth


@pytest.fixture
def mock_virtual_kis_auth():
    """가상 KisAuth 객체를 모킹합니다."""
    auth = MagicMock(spec=KisAuth)
    auth.paper = True
    auth.id = "v_test_id"
    auth.key = MagicMock()
    auth.key.id = "v_test_id"
    auth.key.appkey = "v_test_appkey"
    auth.key.secretkey = "v_test_secretkey"
    auth.account_number = "V12345678-01"
    return auth


# Valid key lengths required by `KisKey` (APPKEY_LENGTH=36, SECRETKEY_LENGTH=180)
VALID_APPKEY = "A" * 36
VALID_SECRETKEY = "S" * 180


@patch("vmkis.kis.KisAuth.load")
def test_init_with_auth_path(mock_load_auth, mock_kis_auth):
    """auth 파일 경로로 VmKis 초기화 테스트"""
    mock_load_auth.return_value = mock_kis_auth
    kis = VmKis("fake/path/auth.json", use_websocket=False)
    mock_load_auth.assert_called_once_with("fake/path/auth.json")
    assert kis.appkey == mock_kis_auth.key
    assert str(kis.primary_account) == mock_kis_auth.account_number
    assert not kis.paper


def test_init_with_kwargs():
    """키워드 인자로 VmKis 초기화 테스트"""
    kis = VmKis(
        id="test_id",
        appkey="test_appkey_36chars_1234567890_abcde",
        secretkey="test_secretkey_180chars_long_aa72vEu5ejiqRwpPRetP2fPdMVeTswa2oitr48MiH1Orje0W8sflP9s9cOfottRWfGsxetpntEpxNo+6zNSZsKUo7G7f8COnXdouYtdUsi34nMVMzDoPrbN5Uu2podrHD8Bhh0zWVHW8nCXu2kEojo=",
        account="12345678-01",
        use_websocket=False,
    )
    assert kis.appkey.id == "test_id"
    assert kis.appkey.appkey == "test_appkey_36chars_1234567890_abcde"
    assert str(kis.primary_account) == "12345678-01"
    assert not kis.paper


def test_init_with_virtual_kwargs():
    """가상 계좌 키워드 인자로 VmKis 초기화 테스트"""
    kis = VmKis(
        id="test_id",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_id="v_test_id",
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        account="12345678-01",
        use_websocket=False,
    )
    # The implementation builds the paper KisKey using the main `id`,
    # so `paper_appkey.id` will match the provided `id` argument.
    assert kis.paper_appkey is not None
    assert kis.paper_appkey.id == "test_id"
    assert kis.paper_appkey.appkey == VALID_APPKEY
    assert str(kis.primary_account) == "12345678-01"
    # Providing `paper_appkey` sets the `paper` property in current
    # implementation because `paper_appkey` is not None.
    assert kis.paper


def test_init_value_errors():
    """초기화 시 발생하는 ValueError 테스트

    소멸자를 무력화하지 않습니다. 부분 초기화된 객체가 GC 될 때
    `__del__` -> `close()` 가 조용히 끝나는 것까지 이 테스트가 함께 봅니다
    (이슈 #38 · #42). `close()` 의 `getattr` 가드가 사라지면
    `PytestUnraisableExceptionWarning` 이 오류로 올라옵니다.
    """
    with pytest.raises(ValueError, match="id를 입력해야 합니다."):
        VmKis(use_websocket=False)
    with pytest.raises(ValueError, match="appkey를 입력해야 합니다."):
        VmKis(id="test", use_websocket=False)
    with pytest.raises(ValueError, match="secretkey를 입력해야 합니다."):
        VmKis(id="test", appkey="key", use_websocket=False)
    # Note: the library requires a separate `paper_auth` object (or
    # explicit paper authentication input) to treat the client as a
    # paper client. Passing only paper key strings does not raise
    # `paper_id` errors in the current implementation, so we do not
    # assert that behavior here.


@patch("vmkis.kis.requests.Session")
@patch("vmkis.api.auth.token.token_issue")
def test_token_property(mock_token_issue, mock_session):
    """token 속성 테스트 (만료 및 재발급)"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    # 토큰이 없을 때 발급
    mock_token_issue.return_value = KisObject.transform_(
        {
            "access_token": "new_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    assert kis.token.token == "new_token"
    mock_token_issue.assert_called_once_with(kis, domain="live")

    # 토큰이 유효할 때 재사용
    mock_token_issue.reset_mock()
    assert kis.token.token == "new_token"
    mock_token_issue.assert_not_called()

    # 토큰이 만료되었을 때 재발급: 교체된 만료된 토큰을 할당
    kis._token = KisObject.transform_(
        {
            "access_token": "old_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2000-01-01 00:00:00",
            "expires_in": 0,
        },
        KisAccessToken,
    )
    mock_token_issue.return_value = KisObject.transform_(
        {
            "access_token": "refreshed_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    assert kis.token.token == "refreshed_token"
    mock_token_issue.assert_called_once_with(kis, domain="live")


@patch("vmkis.kis.requests.Session")
def test_request_rate_limit_and_token_expiry(mock_session):
    """API 요청 시 Rate Limit 및 토큰 만료 처리 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis.token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_request = mock_session.return_value.request
    # 1. Rate limit, 2. Token expired, 3. Success
    mock_request.side_effect = [
        MagicMock(ok=False, json=lambda: {"msg_cd": "EGW00201"}),
        MagicMock(ok=False, json=lambda: {"msg_cd": "EGW00123"}),
        MagicMock(ok=True, json=lambda: {"rt_cd": "0"}),
    ]

    with patch("vmkis.api.auth.token.token_issue") as mock_token_issue:
        mock_token_issue.return_value = KisObject.transform_(
            {
                "access_token": "new_token",
                "token_type": "Bearer",
                "access_token_token_expired": "2099-01-01 00:00:00",
                "expires_in": 86400,
            },
            KisAccessToken,
        )

        with patch("vmkis.kis.sleep") as mock_sleep:
            response = kis.request("/")

            assert response.json()["rt_cd"] == "0"
            assert mock_request.call_count == 3

            # 첫 재시도는 API_RETRY_INITIAL_DELAY 근처. 지터가 ±10% 흔듭니다.
            mock_sleep.assert_called_once()
            (delay,) = mock_sleep.call_args.args
            assert 0.09 <= delay <= 0.11

            mock_token_issue.assert_called_once()  # 토큰 재발급
            assert kis.token.token == "new_token"


# ---------------------------------------------------------------------------
# 재시도 상한 (이슈 #14)
#
# 예전에는 `while True` 안에서 상한 없이 재시도했다. 서버가 EGW00201(유량 초과)
# 이나 EGW00123(토큰 만료)을 계속 반환하면 호출이 영원히 반환되지 않았다.
# 자동매매에서는 "느리다"가 아니라 "멈춘다"이므로, 아래 테스트들은 실패보다
# **끝난다는 것** 자체를 검증한다.
# ---------------------------------------------------------------------------


def _error_response(msg_cd: str) -> MagicMock:
    resp = MagicMock(ok=False, status_code=429)
    resp.json.return_value = {"msg_cd": msg_cd}
    resp.request = MagicMock()
    resp.request.url = "https://example.local/test"
    resp.request.method = "GET"
    resp.request.headers = {}
    resp.request.body = None
    resp.reason = "Too Many Requests"
    resp.text = "rate limited"
    return resp


def _bounded_side_effect(resp: MagicMock, limit: int) -> list[MagicMock]:
    """같은 응답을 `limit` 번만 돌려주는 side_effect.

    `return_value` 로 두면 상한이 회귀했을 때 테스트가 **실패가 아니라 무한
    정지**한다. CI를 멈추게 하는 것은 빨간 줄보다 나쁘다. 목록으로 주면
    소진되는 순간 StopIteration 으로 즉시 터진다.
    """
    return [resp] * limit


def _authed_kis() -> VmKis:
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis.token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    return kis


@patch("vmkis.kis.requests.Session")
def test_rate_limit_retries_are_bounded(mock_session):
    """유량 초과가 계속돼도 무한 루프에 빠지지 않고 예외로 끝난다."""
    kis = _authed_kis()
    mock_session.return_value.request.side_effect = _bounded_side_effect(
        _error_response("EGW00201"), API_RETRY_MAX_ATTEMPTS + 1
    )

    with patch("vmkis.kis.sleep") as mock_sleep, pytest.raises(KisRateLimitError):
        kis.request("/")

    # 최초 1회 + 재시도 N회
    assert mock_session.return_value.request.call_count == API_RETRY_MAX_ATTEMPTS + 1
    assert mock_sleep.call_count == API_RETRY_MAX_ATTEMPTS


@patch("vmkis.kis.requests.Session")
def test_rate_limit_backoff_is_exponential(mock_session):
    """고정 간격이 아니라 지수적으로 물러난다. 고정 간격은 유량 제한을 악화시킨다."""
    kis = _authed_kis()
    mock_session.return_value.request.side_effect = _bounded_side_effect(
        _error_response("EGW00201"), API_RETRY_MAX_ATTEMPTS + 1
    )

    with patch("vmkis.kis.sleep") as mock_sleep, pytest.raises(KisRateLimitError):
        kis.request("/")

    delays = [call.args[0] for call in mock_sleep.call_args_list]

    assert delays == sorted(delays), f"대기가 단조 증가하지 않습니다: {delays}"
    assert delays[-1] > delays[0] * 2, f"백오프가 적용되지 않았습니다: {delays}"
    # 지터가 붙으므로 값이 서로 정확히 같지 않아야 한다.
    assert len(set(delays)) > 1


@patch("vmkis.kis.requests.Session")
def test_token_reissue_is_limited(mock_session):
    """재발급 후에도 만료 오류가 반복되면 인증 문제이므로 즉시 실패한다."""
    kis = _authed_kis()
    mock_session.return_value.request.side_effect = _bounded_side_effect(
        _error_response("EGW00123"), API_TOKEN_REISSUE_LIMIT + 1
    )

    with patch("vmkis.api.auth.token.token_issue") as mock_token_issue:
        mock_token_issue.return_value = KisObject.transform_(
            {
                "access_token": "new_token",
                "token_type": "Bearer",
                "access_token_token_expired": "2099-01-01 00:00:00",
                "expires_in": 86400,
            },
            KisAccessToken,
        )

        with pytest.raises(KisAuthenticationError):
            kis.request("/")

    assert mock_token_issue.call_count == API_TOKEN_REISSUE_LIMIT
    assert mock_session.return_value.request.call_count == API_TOKEN_REISSUE_LIMIT + 1


@patch("vmkis.kis.requests.Session")
def test_request_http_error(mock_session):
    """HTTP 에러 발생 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis.token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=False, status_code=500)
    mock_response.json.return_value = {"msg_cd": "SOME_ERROR", "msg1": "Error message"}
    # Provide a realistic `request` attribute expected by safe_request_data
    mock_response.request = MagicMock()
    mock_response.request.url = "https://example.local/test"
    mock_response.request.method = "GET"
    mock_response.request.headers = {}
    mock_response.request.body = None
    mock_response.reason = "Internal Server Error"
    mock_response.text = "Error message"
    mock_session.return_value.request.return_value = mock_response

    with pytest.raises(KisHTTPError):
        kis.request("/")


@patch("vmkis.kis.Path.exists", return_value=True)
@patch("vmkis.kis.KisAccessToken.load")
@patch("builtins.open", new_callable=mock_open)
def test_load_cached_token(mock_file, mock_load_token, mock_exists):
    """캐시된 토큰 로딩 테스트"""
    mock_token = KisObject.transform_(
        {
            "access_token": "cached_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    mock_load_token.return_value = mock_token

    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=True, use_websocket=False)

    assert kis._token == mock_token
    assert mock_load_token.call_count == 1


@patch("vmkis.kis.Path.mkdir")
@patch("vmkis.kis.KisAccessToken.save")
def test_save_cached_token(mock_save, mock_mkdir):
    """토큰 캐시 저장 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=True, use_websocket=False)
    token = KisObject.transform_(
        {
            "access_token": "new_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    kis._token = token

    with patch("vmkis.kis.VmKis._get_hashed_token_name") as mock_hash_name:
        mock_hash_name.return_value = "hashed_token_name.json"
        kis._save_cached_token(kis._keep_token, domain="live")

        mock_save.assert_called_once()
        # `token.save`가 올바른 경로와 함께 호출되었는지 확인
        saved_path = mock_save.call_args[0][0]
        assert saved_path.name == "hashed_token_name.json"

    def test_primary_and_websocket_errors():
        """`primary` and `websocket` accessors raise when uninitialized"""
        kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

        # primary should raise when no account
        kis.primary_account = None
        with pytest.raises(ValueError, match="기본 계좌 정보가 없습니다."):
            _ = kis.primary

        # websocket should raise when not initialized
        kis._websocket = None
        with pytest.raises(ValueError, match="웹소켓 클라이언트가 초기화되지 않았습니다."):
            _ = kis.websocket

    @patch("vmkis.api.auth.token.token_revoke")
    def test_discard_calls_token_revoke(mock_revoke):
        """discard() should call token_revoke for both tokens when present"""
        kis = VmKis(
            id="t",
            appkey=VALID_APPKEY,
            secretkey=VALID_SECRETKEY,
            paper_appkey=VALID_APPKEY,
            paper_secretkey=VALID_SECRETKEY,
            use_websocket=False,
        )

        kis._token = KisObject.transform_(
            {
                "access_token": "realtok",
                "token_type": "Bearer",
                "access_token_token_expired": "2099-01-01 00:00:00",
                "expires_in": 86400,
            },
            KisAccessToken,
        )

        kis._paper_token = KisObject.transform_(
            {
                "access_token": "vtoken",
                "token_type": "Bearer",
                "access_token_token_expired": "2099-01-01 00:00:00",
                "expires_in": 86400,
            },
            KisAccessToken,
        )

        kis.discard()

        # two calls (live + paper)
        assert mock_revoke.call_count == 2
        # first arg should be the VmKis instance, second is token string
        assert mock_revoke.call_args_list[0][0][0] is kis
        assert mock_revoke.call_args_list[0][0][1] == "realtok"

    def test_get_hashed_token_name_missing_virtual_appkey():
        """_get_hashed_token_name raises when paper appkey missing for paper domain"""
        kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
        with pytest.raises(ValueError, match="모의도메인 AppKey가 없습니다."):
            kis._get_hashed_token_name("paper")

    def test_request_get_validation_errors():
        """Request should validate GET body and appkey_location rules"""
        kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

        with pytest.raises(ValueError, match="GET 요청에는 body를 입력할 수 없습니다."):
            kis.request("/", method="GET", body={"a": 1})

        with pytest.raises(ValueError, match="GET 요청에는 appkey_location을 header로 설정해야 합니다."):
            kis.request("/", method="GET", appkey_location="body")


def test_keep_token_property():
    """keep_token 속성 테스트"""
    # keep_token=False인 경우
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    assert not kis.keep_token

    # keep_token=True인 경우
    with patch("vmkis.kis.get_cache_path") as mock_cache_path:
        mock_cache_path.return_value = "fake/cache/path"
        with patch("vmkis.kis.Path.exists", return_value=False):
            kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=True, use_websocket=False)
            assert kis.keep_token


def test_init_with_virtual_auth_validation():
    """paper_auth가 실전도메인일 때 에러 발생"""
    live_auth = MagicMock(spec=KisAuth)
    live_auth.paper = False
    live_auth.id = "test"
    live_auth.key = MagicMock()
    live_auth.key.appkey = VALID_APPKEY
    live_auth.account_number = "12345678-01"

    paper_auth = MagicMock(spec=KisAuth)
    paper_auth.paper = False  # Should be True
    paper_auth.id = "test"
    paper_auth.key = MagicMock()
    paper_auth.key.appkey = VALID_APPKEY

    with pytest.raises(ValueError, match="paper_auth에는 모의도메인 인증 정보를 입력해야 합니다."):
        VmKis(live_auth, paper_auth, use_websocket=False)


def test_init_with_auth_virtual_error():
    """auth가 모의도메인일 때 에러 발생"""
    paper_auth = MagicMock(spec=KisAuth)
    paper_auth.paper = True
    paper_auth.id = "test"
    paper_auth.key = MagicMock()
    paper_auth.account_number = "12345678-01"

    with pytest.raises(ValueError, match="auth에는 실전도메인 인증 정보를 입력해야 합니다."):
        VmKis(paper_auth, use_websocket=False)


def test_init_with_both_auth_objects():
    """실전도메인과 모의도메인 KisAuth 객체로 초기화"""
    live_auth = MagicMock(spec=KisAuth)
    live_auth.paper = False
    live_auth.id = "real_id"
    live_auth.key = MagicMock()
    live_auth.key.id = "real_id"
    live_auth.key.appkey = VALID_APPKEY
    live_auth.key.secretkey = VALID_SECRETKEY
    live_auth.account_number = "12345678-01"

    paper_auth = MagicMock(spec=KisAuth)
    paper_auth.paper = True
    paper_auth.id = "paper_id"
    paper_auth.key = MagicMock()
    paper_auth.key.id = "paper_id"
    paper_auth.key.appkey = VALID_APPKEY
    paper_auth.key.secretkey = VALID_SECRETKEY
    paper_auth.account_number = "12345678-01"

    kis = VmKis(live_auth, paper_auth, use_websocket=False)

    assert kis.appkey.id == "real_id"
    assert kis.paper_appkey.id == "paper_id"
    assert str(kis.primary_account) == "12345678-01"
    assert kis.paper


@patch("vmkis.kis.requests.Session")
def test_request_with_post_method_and_form(mock_session):
    """POST 요청 시 form 처리 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    mock_form = MagicMock(spec=KisForm)
    response = kis.request("/test", method="POST", form=[mock_form])

    assert response.json()["rt_cd"] == "0"
    mock_form.build.assert_called_once()


@patch("vmkis.kis.requests.Session")
def test_request_with_appkey_in_body(mock_session):
    """POST 요청 시 appkey_location이 body인 경우"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    response = kis.request("/test", method="POST", appkey_location="body")

    assert response.json()["rt_cd"] == "0"
    # appkey.build가 body에 호출되었는지는 간접적으로 확인됨


@patch("vmkis.kis.requests.Session")
def test_request_virtual_domain_without_virtual_appkey(mock_session):
    """paper 도메인 요청 시 paper_appkey가 없으면 에러"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    with pytest.raises(ValueError, match="모의도메인 AppKey가 없습니다."):
        kis.request("/test", domain="paper")


@patch("vmkis.kis.requests.Session")
def test_fetch_with_api_and_continuous(mock_session):
    """fetch 메서드의 api 및 continuous 파라미터 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0", "msg_cd": "SUCCESS", "msg1": "OK"}
    mock_session.return_value.request.return_value = mock_response

    result = kis.fetch("/test", api="TEST_API", continuous=True)

    assert result.rt_cd == "0"
    # headers에 tr_id와 tr_cont가 설정되었는지 확인
    call_kwargs = mock_session.return_value.request.call_args[1]
    assert call_kwargs["headers"]["tr_id"] == "TEST_API"
    assert call_kwargs["headers"]["tr_cont"] == "N"


@patch("vmkis.kis.requests.Session")
def test_fetch_with_verbose_false(mock_session):
    """fetch의 verbose=False 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    with patch("vmkis.logging.logger.debug") as mock_debug:
        result = kis.fetch("/test", verbose=False)
        assert result.rt_cd == "0"
        mock_debug.assert_not_called()


@patch("vmkis.kis.Path.exists")
@patch("vmkis.kis.KisAccessToken.load")
def test_load_cached_token_with_exceptions(mock_load, mock_exists):
    """캐시된 토큰 로딩 시 예외 처리 테스트"""
    mock_exists.return_value = True
    mock_load.side_effect = Exception("Load failed")

    # 예외가 발생해도 초기화는 성공해야 함
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=True, use_websocket=False)

    assert kis._token is None  # 로드 실패로 None이어야 함


@patch("vmkis.kis.Path.mkdir")
@patch("vmkis.kis.KisAccessToken.save")
def test_save_cached_token_with_force(mock_save, mock_mkdir):
    """_save_cached_token의 force 파라미터 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=True, use_websocket=False)

    # Mock token property to avoid actual token issuance
    mock_token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    with patch.object(VmKis, "token", new_callable=lambda: property(lambda self: mock_token)):
        with patch("vmkis.kis.VmKis._get_hashed_token_name") as mock_hash:
            mock_hash.return_value = "hashed.json"
            kis._save_cached_token(kis._keep_token, force=True)

            mock_save.assert_called_once()


@patch("vmkis.kis.Path.mkdir")
@patch("vmkis.kis.KisAccessToken.save")
def test_save_cached_token_virtual_domain(mock_save, mock_mkdir):
    """paper 도메인 토큰 저장 테스트"""
    kis = VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        keep_token=True,
        use_websocket=False,
    )

    kis._paper_token = KisObject.transform_(
        {
            "access_token": "paper_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    with patch("vmkis.kis.VmKis._get_hashed_token_name") as mock_hash:
        mock_hash.return_value = "hashed_virtual.json"
        kis._save_cached_token(kis._keep_token, domain="paper")

        assert mock_save.call_count == 1


@patch("vmkis.kis.requests.Session")
def test_close_method(mock_session):
    """close 메서드 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    kis.close()

    # 두 세션 모두 close 호출되어야 함
    assert mock_session.return_value.close.call_count == 2


@patch("vmkis.kis.requests.Session")
def test_del_method(mock_session):
    """__del__ 메서드 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    kis.__del__()

    # 두 세션 모두 close 호출되어야 함
    assert mock_session.return_value.close.call_count == 2


@patch("vmkis.kis.Path.exists")
@patch("vmkis.kis.KisAccessToken.load")
def test_load_cached_token_for_virtual_domain(mock_load, mock_exists):
    """paper 도메인 캐시 토큰 로딩 테스트"""
    mock_exists.return_value = True
    mock_token = KisObject.transform_(
        {
            "access_token": "cached_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    mock_load.return_value = mock_token

    VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        keep_token=True,
        use_websocket=False,
    )

    # 두 번 로드되어야 함 (live, paper)
    assert mock_load.call_count == 2


@patch("vmkis.kis.requests.Session")
def test_request_with_form_in_header(mock_session):
    """form_location이 header인 경우 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    mock_form = MagicMock(spec=KisForm)
    response = kis.request("/test", method="POST", form=[mock_form], form_location="header")

    assert response.json()["rt_cd"] == "0"
    mock_form.build.assert_called_once()


@patch("vmkis.kis.requests.Session")
def test_request_with_form_in_params(mock_session):
    """form_location이 params인 경우 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    mock_form = MagicMock(spec=KisForm)
    response = kis.request("/test", method="GET", form=[mock_form], form_location="params", params={})

    assert response.json()["rt_cd"] == "0"
    mock_form.build.assert_called_once()


def test_init_token_from_path():
    """토큰을 파일 경로에서 로드하는 초기화 테스트"""
    mock_token = KisObject.transform_(
        {
            "access_token": "loaded_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    with patch("vmkis.kis.KisAccessToken.load", return_value=mock_token):
        kis = VmKis(
            id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, token="fake/token.json", use_websocket=False
        )

        assert kis._token == mock_token


def test_init_virtual_token_from_path():
    """paper 토큰을 파일 경로에서 로드하는 초기화 테스트"""
    mock_token = KisObject.transform_(
        {
            "access_token": "loaded_paper_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    with patch("vmkis.kis.KisAccessToken.load", return_value=mock_token):
        kis = VmKis(
            id="t",
            appkey=VALID_APPKEY,
            secretkey=VALID_SECRETKEY,
            paper_appkey=VALID_APPKEY,
            paper_secretkey=VALID_SECRETKEY,
            paper_token="fake/vtoken.json",
            use_websocket=False,
        )

        assert kis._paper_token == mock_token


@patch("vmkis.kis.requests.Session")
@patch("vmkis.api.auth.token.token_issue")
def test_primary_token_for_virtual_domain(mock_token_issue, mock_session):
    """paper 도메인의 primary_token 테스트"""
    kis = VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        use_websocket=False,
    )

    mock_token_issue.return_value = KisObject.transform_(
        {
            "access_token": "paper_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    # primary_token은 paper 도메인에서 _virtual_token을 반환
    token = kis.primary_token
    assert token.token == "paper_token"
    mock_token_issue.assert_called_once_with(kis, domain="paper")


@patch("vmkis.kis.requests.Session")
def test_primary_token_returns_token_for_real_domain(mock_session):
    """live 도메인에서 primary_token이 token을 반환하는지 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    with patch("vmkis.api.auth.token.token_issue") as mock_issue:
        mock_issue.return_value = KisObject.transform_(
            {
                "access_token": "real_token",
                "token_type": "Bearer",
                "access_token_token_expired": "2099-01-01 00:00:00",
                "expires_in": 86400,
            },
            KisAccessToken,
        )

        token = kis.primary_token
        assert token.token == "real_token"
        # live 도메인이므로 token property를 통해 발급됨
        mock_issue.assert_called_once_with(kis, domain="live")


@patch("vmkis.kis.requests.Session")
def test_primary_token_setter(mock_session):
    """primary_token setter 테스트"""
    kis = VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        use_websocket=False,
    )

    mock_token = KisObject.transform_(
        {
            "access_token": "set_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    kis.primary_token = mock_token
    assert kis._paper_token == mock_token


@patch("vmkis.api.auth.token.token_revoke")
@patch("vmkis.kis.requests.Session")
def test_discard_real_domain_only(mock_session, mock_revoke):
    """실전 도메인만 토큰 폐기"""
    kis = VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        use_websocket=False,
    )

    kis._token = KisObject.transform_(
        {
            "access_token": "real_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    kis.discard(domain="live")

    assert mock_revoke.call_count == 1
    assert kis._token is None


@patch("vmkis.api.auth.token.token_revoke")
@patch("vmkis.kis.requests.Session")
def test_discard_virtual_domain_only(mock_session, mock_revoke):
    """모의 도메인만 토큰 폐기"""
    kis = VmKis(
        id="t",
        appkey=VALID_APPKEY,
        secretkey=VALID_SECRETKEY,
        paper_appkey=VALID_APPKEY,
        paper_secretkey=VALID_SECRETKEY,
        use_websocket=False,
    )

    kis._paper_token = KisObject.transform_(
        {
            "access_token": "paper_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    kis.discard(domain="paper")

    assert mock_revoke.call_count == 1
    assert kis._paper_token is None


@patch("vmkis.kis.requests.Session")
def test_request_without_auth(mock_session):
    """auth=False로 요청 시 토큰 없이 요청"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    response = kis.request("/test", auth=False)

    assert response.json()["rt_cd"] == "0"
    # auth=False이므로 토큰이 헤더에 추가되지 않음


@patch("vmkis.kis.requests.Session")
def test_request_without_appkey_location(mock_session):
    """appkey_location=None으로 요청"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    response = kis.request("/test", appkey_location=None)

    assert response.json()["rt_cd"] == "0"


@patch("vmkis.kis.requests.Session")
def test_fetch_basic_functionality(mock_session):
    """fetch의 기본 동작 테스트"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0", "output": {}}
    mock_session.return_value.request.return_value = mock_response

    result = kis.fetch("/test")
    # fetch가 정상적으로 응답을 처리하는지 확인
    assert result.rt_cd == "0"


@patch("vmkis.kis.requests.Session")
@patch("vmkis.api.auth.token.token_issue")
def test_primary_token_with_keep_token(mock_token_issue, mock_session):
    """primary_token 발급 시 keep_token이 활성화된 경우"""
    mock_token_issue.return_value = KisObject.transform_(
        {
            "access_token": "new_paper_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    with patch("vmkis.kis.Path.exists", return_value=False):
        kis = VmKis(
            id="t",
            appkey=VALID_APPKEY,
            secretkey=VALID_SECRETKEY,
            paper_appkey=VALID_APPKEY,
            paper_secretkey=VALID_SECRETKEY,
            keep_token=True,
            use_websocket=False,
        )

        with patch.object(kis, "_save_cached_token") as mock_save:
            token = kis.primary_token
            assert token.token == "new_paper_token"
            mock_save.assert_called_once()


@patch("vmkis.kis.requests.Session")
def test_request_response_json_exception(mock_session):
    """응답의 json() 호출 시 예외 처리"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=False, status_code=500)
    mock_response.json.side_effect = Exception("JSON parse error")
    mock_response.request = MagicMock()
    mock_response.request.url = "https://example.local/test"
    mock_response.request.method = "GET"
    mock_response.request.headers = {}
    mock_response.request.body = None
    mock_response.reason = "Internal Server Error"
    mock_response.text = "Error"
    mock_session.return_value.request.return_value = mock_response

    with pytest.raises(KisHTTPError):
        kis.request("/test")


@patch("vmkis.kis.requests.Session")
def test_request_with_none_form_element(mock_session):
    """form 리스트에 None 요소가 포함된 경우"""
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, use_websocket=False)
    kis._token = KisObject.transform_(
        {
            "access_token": "test_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )

    mock_response = MagicMock(ok=True)
    mock_response.json.return_value = {"rt_cd": "0"}
    mock_session.return_value.request.return_value = mock_response

    mock_form = MagicMock(spec=KisForm)
    response = kis.request("/test", method="POST", form=[mock_form, None])

    assert response.json()["rt_cd"] == "0"
    # None은 무시되고 mock_form만 build 호출됨
    mock_form.build.assert_called_once()


def test_save_cached_token_when_keep_token_is_an_existing_file(tmp_path) -> None:
    """#157. create_client 는 앱 이름 json 을 keep_token 으로 넘깁니다."""
    token_file = tmp_path / "app_paper_1.json"
    token_file.write_text("{}", encoding="utf-8")
    kis = VmKis(id="t", appkey=VALID_APPKEY, secretkey=VALID_SECRETKEY, keep_token=token_file, use_websocket=False)
    token = KisObject.transform_(
        {
            "access_token": "new_token",
            "token_type": "Bearer",
            "access_token_token_expired": "2099-01-01 00:00:00",
            "expires_in": 86400,
        },
        KisAccessToken,
    )
    kis._token = token
    kis._save_cached_token(kis._keep_token, domain="live")

    saved = list(tmp_path.glob("token_live_*.json"))
    assert saved, "파일 경로 keep_token 에서 토큰을 저장하지 못했습니다"
    assert token_file.is_file()


def test_mkdir_on_existing_token_file_is_caught(tmp_path) -> None:
    """결함을 되넣으면 파일이 있는 자리에 mkdir 합니다."""
    token_file = tmp_path / "app_paper_1.json"
    token_file.write_text("{}", encoding="utf-8")
    with pytest.raises(FileExistsError):
        token_file.mkdir(parents=True, exist_ok=True)
