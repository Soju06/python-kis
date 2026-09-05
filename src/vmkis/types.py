"""
VM-Stock-KIS 내부 타입 및 Protocol 정의

⚠️ 주의: 이 모듈은 라이브러리 내부 및 고급 사용자용입니다.

==============================================================================
누가 사용해야 하나?
==============================================================================

1️⃣ **일반 사용자 (추천)**
   └─ from vmkis import Quote, Balance, Order  (공개 타입 사용)
   └─ 설명서: docs/SIMPLEKIS_GUIDE.md, QUICKSTART.md

2️⃣ **Type Hint를 작성하는 개발자**
   ├─ from vmkis import Quote, Balance, Order  (공개 타입)
   └─ Type Hint 작성 가능

3️⃣ **고급 사용자 / 기여자 (직접 import)**
   ├─ from vmkis.types import KisObjectProtocol  (Protocol)
   ├─ from vmkis.adapter.* import * (Adapter/Mixin)
   └─ docs/architecture/ARCHITECTURE.md 문서 정독 필수

==============================================================================
내용 구성
==============================================================================

이 모듈은 다음을 포함합니다:

### Adapter/Mixin 클래스
- KisQuotableAccount: 시세 조회 기능 추가
- KisOrderableAccount: 주문 기능 추가
- KisOrderableAccountProduct: 상품별 주문 기능
- KisRealtimeOrderableAccount: WebSocket 기반 실시간 주문
- KisQuotableProduct, KisWebsocketQuotableProduct: 종목별 시세 기능

### API 응답 타입
- KisBalance, KisOrder: 계좌 잔고/주문 정보
- KisChart, KisOrderbook: 차트, 호가 정보
- KisQuote, KisTradingHours: 시세, 장시간 정보
- KisRealtimePrice, KisRealtimeExecution: 실시간 시세, 체결 정보

### Protocol 인터페이스
- KisAccountProtocol: 계좌 관련 인터페이스
- KisProductProtocol: 종목 관련 인터페이스
- KisMarketProtocol: 시장 관련 인터페이스
- KisObjectProtocol: 기본 API 객체 인터페이스

### 이벤트 및 핸들러
- KisEventHandler: 이벤트 핸들러
- KisEventFilter, KisEventCallback: 이벤트 필터/콜백
- KisEventTicket: 이벤트 구독 티켓

### 클라이언트 기능
- KisAuth: 인증 정보
- KisWebsocketClient: WebSocket 연결
- KisPage: 페이지네이션

==============================================================================
버전 정책
==============================================================================

| 버전 | 상태 | 설명 |
|------|------|------|
| 0.x | ⚪ 지난 경고 구간 | 루트에서 내부 타입을 가져오면 경고가 났음 |
| 1.0.0+ | ✅ 적용 | 루트 위임 없음. `from vmkis.types import …` 만 |

자세한 내용은 docs/MIGRATION_GUIDE.md 를 보세요.

==============================================================================
사용 예제
==============================================================================

### ❌ 나쁜 예 (권장하지 않음)

```python
# 일반 사용자가 직접 import (복잡함)
from vmkis.types import KisQuotableAccount, KisOrderableAccount
```

### ✅ 좋은 예 (권장)

```python
# 1. 공개 타입 사용
from vmkis import Quote, Balance, Order

def analyze_quote(quote: Quote) -> None:
    print(f"가격: {quote.price}원")

# 2. SimpleKIS 파사드 사용
from vmkis import create_client
from vmkis.simple import SimpleKIS

kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)
price = simple.get_price("005930")

# 3. 고급: VmKis 직접 사용 (필요시)
from vmkis import VmKis

kis = VmKis(auth)
quote = kis.stock("005930").quote()
```

### 🔬 고급 사용 (기여자용)

```python
# Protocol을 활용한 커스텀 구현
from vmkis.types import KisObjectProtocol

class MyCustomObject(KisObjectProtocol):
    def __init__(self, kis):
        self.kis = kis

    def custom_method(self):
        # 내부 API 활용
        return self.kis.fetch(...)
```

==============================================================================
"""

from vmkis.adapter.account.balance import KisQuotableAccount
from vmkis.adapter.account.order import KisOrderableAccount
from vmkis.adapter.account_product.order import KisOrderableAccountProduct
from vmkis.adapter.account_product.order_modify import (
    KisCancelableOrder,
    KisModifyableOrder,
    KisOrderableOrder,
)
from vmkis.adapter.product.quote import KisQuotableProduct
from vmkis.adapter.websocket.execution import KisRealtimeOrderableAccount
from vmkis.adapter.websocket.price import KisWebsocketQuotableProduct
from vmkis.api.account.balance import KisBalance, KisBalanceStock, KisDeposit
from vmkis.api.account.daily_order import KisDailyOrder, KisDailyOrders
from vmkis.api.account.order import (
    IN_ORDER_QUANTITY,
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    ORDER_QUANTITY,
    ORDER_TYPE,
    KisOrder,
    KisOrderNumber,
    KisSimpleOrder,
    KisSimpleOrderNumber,
)
from vmkis.api.account.order_profit import KisOrderProfit, KisOrderProfits
from vmkis.api.account.orderable_amount import (
    KisOrderableAmount,
    KisOrderableAmountResponse,
)
from vmkis.api.account.pending_order import KisPendingOrder, KisPendingOrders
from vmkis.api.auth.token import KisAccessToken
from vmkis.api.auth.websocket import KisWebsocketApprovalKey
from vmkis.api.base.account import KisAccountProtocol
from vmkis.api.base.account_product import KisAccountProductProtocol
from vmkis.api.base.market import KisMarketProtocol
from vmkis.api.base.product import KisProductProtocol
from vmkis.api.stock.chart import KisChart, KisChartBar
from vmkis.api.stock.info import (
    COUNTRY_TYPE,
    MARKET_INFO_TYPES,
    KisStockInfo,
    KisStockInfoResponse,
)
from vmkis.api.stock.market import CURRENCY_TYPE, MARKET_TYPE, ExDateType
from vmkis.api.stock.order_book import (
    KisOrderbook,
    KisOrderbookItem,
    KisOrderbookResponse,
)
from vmkis.api.stock.quote import (
    STOCK_RISK_TYPE,
    STOCK_SIGN_TYPE,
    KisIndicator,
    KisQuote,
    KisQuoteResponse,
)
from vmkis.api.stock.trading_hours import KisTradingHours
from vmkis.api.websocket.order_book import KisRealtimeOrderbook
from vmkis.api.websocket.order_execution import KisRealtimeExecution
from vmkis.api.websocket.price import KisRealtimePrice
from vmkis.client.account import KisAccountNumber
from vmkis.client.appkey import KisKey
from vmkis.client.auth import KisAuth
from vmkis.client.cache import KisCacheStorage
from vmkis.client.form import KisForm
from vmkis.client.messaging import (
    KisWebsocketEncryptionKey,
    KisWebsocketForm,
    KisWebsocketRequest,
    KisWebsocketTR,
)
from vmkis.client.object import KisObjectProtocol
from vmkis.client.page import KisPage, KisPageStatus
from vmkis.client.websocket import KisWebsocketClient
from vmkis.event.filters.order import KisOrderNumberEventFilter
from vmkis.event.filters.product import KisProductEventFilter
from vmkis.event.filters.subscription import KisSubscriptionEventFilter
from vmkis.event.handler import (
    EventCallback,
    KisEventArgs,
    KisEventCallback,
    KisEventFilter,
    KisEventHandler,
    KisEventTicket,
    KisLambdaEventCallback,
    KisLambdaEventFilter,
    KisMultiEventFilter,
)
from vmkis.event.subscription import (
    KisSubscribedEventArgs,
    KisSubscriptionEventArgs,
    KisUnsubscribedEventArgs,
)
from vmkis.kis import VmKis
from vmkis.responses.response import (
    KisAPIResponse,
    KisPaginationAPIResponse,
    KisPaginationAPIResponseProtocol,
    KisResponse,
    KisResponseProtocol,
)
from vmkis.responses.websocket import KisWebsocketResponse, KisWebsocketResponseProtocol
from vmkis.scope.account import KisAccount, KisAccountScope
from vmkis.scope.base import KisScope, KisScopeBase
from vmkis.scope.stock import KisStock, KisStockScope
from vmkis.utils.timex import TIMEX_TYPE

__all__ = [
    ################################
    ##            Types           ##
    ################################
    "TIMEX_TYPE",
    "COUNTRY_TYPE",
    "MARKET_TYPE",
    "CURRENCY_TYPE",
    "MARKET_INFO_TYPES",
    "ExDateType",
    "STOCK_SIGN_TYPE",
    "STOCK_RISK_TYPE",
    "ORDER_TYPE",
    "ORDER_PRICE",
    "ORDER_EXECUTION",
    "ORDER_CONDITION",
    "ORDER_QUANTITY",
    "IN_ORDER_QUANTITY",
    ################################
    ##             API            ##
    ################################
    "VmKis",
    "KisAccessToken",
    "KisAccountNumber",
    "KisKey",
    "KisAuth",
    "KisCacheStorage",
    "KisForm",
    "KisPage",
    "KisPageStatus",
    ################################
    ##          Websocket         ##
    ################################
    "KisWebsocketApprovalKey",
    "KisWebsocketForm",
    "KisWebsocketRequest",
    "KisWebsocketTR",
    "KisWebsocketEncryptionKey",
    "KisWebsocketClient",
    ################################
    ##            Events          ##
    ################################
    "EventCallback",
    "KisEventArgs",
    "KisEventCallback",
    "KisEventFilter",
    "KisEventHandler",
    "KisEventTicket",
    "KisLambdaEventCallback",
    "KisLambdaEventFilter",
    "KisMultiEventFilter",
    "KisSubscribedEventArgs",
    "KisUnsubscribedEventArgs",
    "KisSubscriptionEventArgs",
    ################################
    ##        Event Filters       ##
    ################################
    "KisProductEventFilter",
    "KisOrderNumberEventFilter",
    "KisSubscriptionEventFilter",
    ################################
    ##            Scope           ##
    ################################
    "KisScope",
    "KisScopeBase",
    "KisAccountScope",
    "KisAccount",
    "KisStock",
    "KisStockScope",
    ################################
    ##          Responses         ##
    ################################
    "KisAPIResponse",
    "KisResponse",
    "KisResponseProtocol",
    "KisPaginationAPIResponse",
    "KisPaginationAPIResponseProtocol",
    "KisWebsocketResponse",
    "KisWebsocketResponseProtocol",
    ################################
    ##          Protocols         ##
    ################################
    "KisObjectProtocol",
    "KisMarketProtocol",
    "KisProductProtocol",
    "KisAccountProtocol",
    "KisAccountProductProtocol",
    "KisStockInfo",
    "KisOrderbook",
    "KisOrderbookItem",
    "KisChartBar",
    "KisChart",
    "KisTradingHours",
    "KisIndicator",
    "KisQuote",
    "KisBalanceStock",
    "KisDeposit",
    "KisBalance",
    "KisDailyOrder",
    "KisDailyOrders",
    "KisOrderProfit",
    "KisOrderProfits",
    "KisOrderNumber",
    "KisOrder",
    "KisSimpleOrderNumber",
    "KisSimpleOrder",
    "KisOrderableAmount",
    "KisPendingOrder",
    "KisPendingOrders",
    "KisRealtimeOrderbook",
    "KisRealtimeExecution",
    "KisRealtimePrice",
    ################################
    ##           Adapters         ##
    ################################
    "KisQuotableAccount",
    "KisOrderableAccount",
    "KisOrderableAccountProduct",
    "KisQuotableProduct",
    "KisRealtimeOrderableAccount",
    "KisWebsocketQuotableProduct",
    "KisCancelableOrder",
    "KisModifyableOrder",
    "KisOrderableOrder",
    ################################
    ##        API Responses       ##
    ################################
    "KisStockInfoResponse",
    "KisOrderbookResponse",
    "KisQuoteResponse",
    "KisOrderableAmountResponse",
]
