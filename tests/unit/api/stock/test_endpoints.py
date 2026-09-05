"""시세 계열 엔드포인트 스펙 검증 (이슈 #43).

**이 파일이 필요한 이유.** 시세 테스트는 `params` 만 단언하고 TR ID 는 보지
않았습니다. 실제로 `DOMESTIC_QUOTE.tr_live` 을 `"WRONG_TR_ID"` 로 바꿔도
`tests/unit/api/stock` 165건이 전부 통과했습니다. 스펙이 데이터가 된 지금은
네트워크 없이 규칙을 직접 확인할 수 있습니다.

시세·차트 TR 은 **모의도메인에 없습니다.** `tr_paper` 을 생략하는 것으로
그 사실을 표현하고, `resolve()` 가 모의 계좌에서도 실전 도메인을 돌려줍니다.
예전에는 호출부마다 도메인을 손으로 지정했고 빠뜨리면 모의 계정에서만
터졌습니다.
"""

import pytest

from vmkis.api.account.order import FOREIGN_DAYTIME_ORDER_ENDPOINTS
from vmkis.api.stock.daily_chart import DOMESTIC_DAILY_CHART, FOREIGN_DAILY_CHART
from vmkis.api.stock.day_chart import DOMESTIC_DAY_CHART, FOREIGN_DAY_CHART
from vmkis.api.stock.info import DOMESTIC_QUOTE as INFO_DOMESTIC_QUOTE
from vmkis.api.stock.info import FOREIGN_PRICE, PRODUCT_INFO
from vmkis.api.stock.quote import DOMESTIC_QUOTE, FOREIGN_QUOTE

# (스펙, 기대 TR ID, 기대 경로)
QUOTE_ENDPOINTS = [
    (DOMESTIC_QUOTE, "FHKST01010100", "/uapi/domestic-stock/v1/quotations/inquire-price"),
    (FOREIGN_QUOTE, "HHDFS76200200", "/uapi/overseas-price/v1/quotations/price-detail"),
    (FOREIGN_PRICE, "HHDFS00000300", "/uapi/overseas-price/v1/quotations/price"),
    (PRODUCT_INFO, "CTPF1604R", "/uapi/domestic-stock/v1/quotations/search-info"),
    (
        DOMESTIC_DAILY_CHART,
        "FHKST03010100",
        "/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice",
    ),
    (FOREIGN_DAILY_CHART, "HHDFS76240000", "/uapi/overseas-price/v1/quotations/dailyprice"),
    (
        DOMESTIC_DAY_CHART,
        "FHKST03010200",
        "/uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice",
    ),
    (
        FOREIGN_DAY_CHART,
        "HHDFS76950200",
        "/uapi/overseas-price/v1/quotations/inquire-time-itemchartprice",
    ),
]


@pytest.mark.parametrize(("endpoint", "tr_id", "path"), QUOTE_ENDPOINTS)
def test_quote_endpoint_identity(endpoint, tr_id, path):
    """TR ID 와 경로가 KIS 문서와 일치한다."""
    assert endpoint.tr_live == tr_id
    assert endpoint.path == path


@pytest.mark.parametrize(("endpoint", "tr_id", "_path"), QUOTE_ENDPOINTS)
def test_quote_endpoints_route_to_real_domain(endpoint, tr_id, _path):
    """모의 계좌로 호출해도 실전 도메인으로 나간다.

    시세 TR 은 모의 서버에 없습니다. `tr_paper` 이 `None` 인 것만으로
    라우팅이 결정되므로 `domain_override` 를 함께 줄 필요가 없습니다.
    """
    assert endpoint.tr_paper is None
    assert endpoint.domain_override is None

    assert endpoint.resolve(paper=False) == (tr_id, "live")
    assert endpoint.resolve(paper=True) == (tr_id, "live")


def test_info_shares_domestic_quote_spec():
    """`info.py` 는 `quote.py` 의 스펙을 재정의하지 않고 그대로 씁니다."""
    assert INFO_DOMESTIC_QUOTE is DOMESTIC_QUOTE


@pytest.mark.parametrize(("order", "tr_id"), [("buy", "TTTS6036U"), ("sell", "TTTS6037U")])
def test_foreign_daytime_order_endpoints(order, tr_id):
    """주간거래 주문은 모의투자를 지원하지 않는다."""
    endpoint = FOREIGN_DAYTIME_ORDER_ENDPOINTS[order]

    assert endpoint.tr_live == tr_id
    assert endpoint.path == "/uapi/overseas-stock/v1/trading/daytime-order"
    assert endpoint.method == "POST"
    assert endpoint.resolve(paper=True) == (tr_id, "live")
