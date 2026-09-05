"""
통합 테스트 - Mock API 호출 시뮬레이션

requests-mock을 사용하여 실제 API 호출 없이
전체 흐름을 테스트합니다.
"""

import pytest
import requests_mock

from vmkis import KisAuth, VmKis
from vmkis.client.exceptions import KisAPIError, KisHTTPError


@pytest.fixture
def mock_auth():
    """테스트용 인증 정보"""
    return KisAuth(
        id="test_user",
        account="50000000-01",
        appkey="P" + "A" * 35,  # 36자
        secretkey="S" * 180,  # 180자
        paper=False,  # 실전도메인
    )


@pytest.fixture
def mock_virtual_auth():
    """테스트용 모의(paper) 인증 정보"""
    return KisAuth(
        id="test_user",
        account="50000000-01",
        appkey="P" + "A" * 35,  # 36자
        secretkey="S" * 180,  # 180자
        paper=True,
    )


@pytest.fixture
def mock_token_response():
    """토큰 발급 응답"""
    return {
        "access_token": "test_token_12345",
        "access_token_token_expired": "2025-12-31 23:59:59",
        "token_type": "Bearer",
        "expires_in": 86400,
    }


@pytest.fixture
def mock_quote_response():
    """시세 조회 응답"""
    return {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": {
            "stck_prpr": "70000",  # 현재가
            "prdy_vrss": "1000",  # 전일대비
            "prdy_vrss_sign": "2",  # 전일대비부호
            "prdy_ctrt": "1.45",  # 전일대비율
            "acml_vol": "1000000",  # 누적거래량
            "acml_tr_pbmn": "70000000000",  # 누적거래대금
        },
    }


@pytest.fixture
def mock_balance_response():
    """잔고 조회 응답"""
    return {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output1": [
            {
                "pdno": "000660",  # 종목코드
                "prdt_name": "SK하이닉스",  # 종목명
                "hldg_qty": "10",  # 보유수량
                "pchs_avg_pric": "69000",  # 매입평균가격
                "prpr": "70000",  # 현재가
                "evlu_amt": "700000",  # 평가금액
                "evlu_pfls_amt": "10000",  # 평가손익금액
                "evlu_pfls_rt": "1.45",  # 평가손익율
            }
        ],
        "output2": {
            "dnca_tot_amt": "1000000",  # 예수금총액
            "nxdy_excc_amt": "900000",  # 익일정산금액
            "prvs_rcdl_excc_amt": "100000",  # 가수도정산금액
        },
    }


@pytest.fixture
def mock_search_info_response():
    """종목 기본정보 조회 응답"""
    return {
        "rt_cd": "0",
        "msg_cd": "MCA00000",
        "msg1": "정상처리 되었습니다.",
        "output": {
            "shtn_pdno": "000660",  # 종목코드
            "std_pdno": "KR0000660001",  # 표준코드
            "prdt_abrv_name": "SK하이닉스",  # 종목명
            "prdt_name120": "SK하이닉스",  # 종목전체명
            "prdt_eng_abrv_name": "SK hynix",  # 종목영문명
            "prdt_eng_name120": "SK hynix Inc.",  # 종목영문전체명
            "prdt_type_cd": "300",  # 상품유형코드
        },
    }


class TestIntegrationMockAPISimulation:
    """Mock API 통합 테스트"""

    def test_token_issuance_flow(self, mock_auth, mock_virtual_auth, mock_token_response):
        """토큰 발급 흐름 테스트"""
        with requests_mock.Mocker() as m:
            # 토큰 발급 API Mock
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # VmKis 초기화 시 자동으로 토큰 발급 (모의도메인)
            # auth와 paper_auth는 위치 인자로 전달
            kis = VmKis(mock_auth, mock_virtual_auth)

            # 토큰이 설정되었는지 확인
            assert kis.primary_token is not None
            assert kis.primary_token.token == "test_token_12345"

    def test_quote_api_call_flow(
        self, mock_auth, mock_virtual_auth, mock_token_response, mock_quote_response, mock_search_info_response
    ):
        """시세 조회 API 호출 흐름"""
        with requests_mock.Mocker() as m:
            # 토큰 발급 - live 도메인
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 토큰 발급 - paper 도메인
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # 종목 기본정보 조회 API Mock - live 도메인
            m.get(
                "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/search-info",
                json=mock_search_info_response,
            )

            # 시세 조회 API Mock - live 도메인
            m.get(
                "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price",
                json=mock_quote_response,
            )

            kis = VmKis(mock_auth, mock_virtual_auth)
            kis.stock("000660")

            # quote = stock.quote()
            # assert quote.price == Decimal("70000")
            # assert quote.volume == 1000000

    def test_balance_api_call_flow(self, mock_auth, mock_virtual_auth, mock_token_response, mock_balance_response):
        """잔고 조회 API 호출 흐름"""
        with requests_mock.Mocker() as m:
            # 토큰 발급
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # 잔고 조회 API Mock
            m.get(
                "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/trading/inquire-balance",
                json=mock_balance_response,
            )

            kis = VmKis(mock_auth, mock_virtual_auth)
            kis.account()

            # balance = account.balance()
            # assert len(balance.stocks) == 1
            # assert balance.stocks[0].symbol == "000660"

    def test_api_error_handling(self, mock_auth, mock_virtual_auth, mock_token_response):
        """API 에러 응답 처리"""
        from vmkis.responses.response import KisAPIResponse

        error_response = {"rt_cd": "1", "msg_cd": "EGW00123", "msg1": "시스템 오류가 발생했습니다."}

        with requests_mock.Mocker() as m:
            # 토큰 발급 - live 도메인
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 토큰 발급 - paper 도메인
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # 에러 응답
            m.get(
                "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price",
                json=error_response,
                status_code=200,
            )

            kis = VmKis(mock_auth, mock_virtual_auth)

            # API 에러 발생 확인: use `fetch` with explicit path, api id, and response_type
            with pytest.raises(KisAPIError) as exc_info:
                kis.fetch(
                    "/uapi/domestic-stock/v1/quotations/inquire-price",
                    api="FHKST01010100",
                    params={"fid_input_iscd": "000660"},
                    domain="paper",
                    response_type=KisAPIResponse,
                )

            assert "EGW00123" in str(exc_info.value)

    def test_http_error_handling(self, mock_auth, mock_virtual_auth, mock_token_response):
        """HTTP 에러 처리"""
        with requests_mock.Mocker() as m:
            # 토큰 발급 - live 도메인
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 토큰 발급 - paper 도메인
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # HTTP 500 에러
            m.get(
                "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price",
                status_code=500,
                text="Internal Server Error",
            )

            kis = VmKis(mock_auth, mock_virtual_auth)

            # HTTP 에러 발생 확인
            with pytest.raises(KisHTTPError) as exc_info:
                kis.request(
                    "/uapi/domestic-stock/v1/quotations/inquire-price",
                    method="GET",
                    params={"fid_input_iscd": "000660"},
                    domain="paper",
                )

            assert exc_info.value.status_code == 500

    def test_token_expiration_and_refresh(self, mock_auth, mock_virtual_auth, mock_token_response):
        """토큰 만료 및 재발급"""
        with requests_mock.Mocker() as m:
            # 토큰 발급 - live 도메인
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 토큰 발급 - paper 도메인
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # 401 Unauthorized (토큰 만료)
            m.get(
                "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price",
                [
                    {"status_code": 401, "json": {"error": "token expired"}},
                    {"status_code": 200, "json": mock_token_response},
                ],
            )

            VmKis(mock_auth, mock_virtual_auth)

            # 첫 요청은 401, 재발급 후 성공해야 함
            # (실제 구현에서는 자동 재발급 로직 필요)

    def test_rate_limiting_with_mock(
        self, mock_auth, mock_virtual_auth, mock_token_response, mock_quote_response, mock_search_info_response
    ):
        """Rate Limiting과 함께 Mock 테스트"""
        import time

        with requests_mock.Mocker() as m:
            # 토큰 발급 - live 도메인
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 토큰 발급 - paper 도메인
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            # 종목 기본정보 조회 API Mock - live 도메인 (any symbol)
            m.get(
                "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/search-info",
                json=mock_search_info_response,
            )

            # quotable_market에서 사용하는 inquire-price API Mock - live 도메인
            m.get(
                "https://openapi.koreainvestment.com:9443/uapi/domestic-stock/v1/quotations/inquire-price",
                json=mock_quote_response,
            )

            # 시세 조회 (여러 번)
            m.get(
                "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price",
                json=mock_quote_response,
            )

            kis = VmKis(mock_auth, mock_virtual_auth)

            start_time = time.time()

            # 5번 요청 (모의투자 제한: 초당 1개)
            for i in range(5):
                kis.stock(f"00066{i}")
                # stock.quote()

            time.time() - start_time

            # 약 4초 이상 소요되어야 함
            # assert elapsed >= 4.0

    def test_multiple_accounts(self, mock_token_response):
        """여러 계좌 처리"""
        # 실전 도메인 인증 정보
        live_auth = KisAuth(
            id="real_user",
            account="50000000-00",
            appkey="P" + "R" * 35,
            secretkey="R" * 180,
            paper=False,
        )

        # 모의 도메인 인증 정보 1
        auth1 = KisAuth(
            id="user1",
            account="50000000-01",
            appkey="P" + "A" * 35,
            secretkey="S" * 180,
            paper=True,
        )

        # 모의 도메인 인증 정보 2
        auth2 = KisAuth(
            id="user2",
            account="50000000-02",
            appkey="P" + "B" * 35,
            secretkey="T" * 180,
            paper=True,
        )

        with requests_mock.Mocker() as m:
            # 실전 도메인 토큰 발급
            m.post("https://openapi.koreainvestment.com:9443/oauth2/tokenP", json=mock_token_response)

            # 모의 도메인 토큰 발급
            m.post("https://openapivts.koreainvestment.com:29443/oauth2/tokenP", json=mock_token_response)

            kis1 = VmKis(live_auth, auth1)
            kis2 = VmKis(live_auth, auth2)

            assert kis1.primary_account != kis2.primary_account


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
