from datetime import datetime, tzinfo
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Literal, get_args

from pykis.__env__ import EMPTY, EMPTY_TYPE, TIMEZONE
from pykis.api.account.order import (
    ORDER_CONDITION,
    ORDER_EXECUTION,
    ORDER_PRICE,
    KisOrder,
    KisOrderNumber,
)
from pykis.api.base.account_product import KisAccountProductBase
from pykis.api.stock.info import market_to_country
from pykis.api.stock.market import (
    DAYTIME_MARKET_SHORT_TYPE_MAP,
    MARKET_TIMEZONE_OBJECT_MAP,
    MARKET_TYPE,
    MARKET_TYPE_KOR_MAP,
)
from pykis.api.stock.quote import quote
from pykis.client.account import KisAccountNumber
from pykis.responses.dynamic import KisDynamic
from pykis.responses.exception import KisMarketNotOpenedError
from pykis.responses.response import KisAPIResponse, raise_not_found
from pykis.responses.types import KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis


class KisDomesticModifyOrder(KisAPIResponse, KisOrder):
    """한국투자증권 국내주식 정정 주문"""

    branch: str = KisString["KRX_FWDG_ORD_ORGNO"]
    """지점코드"""
    number: str = KisString["ODNO"]
    """주문번호"""
    time: datetime
    """주문시간 (현지시간)"""
    time_kst: datetime
    """주문시간 (한국시간)"""

    def __pre_init__(self, data: dict[str, Any]):
        # TODO: 정정주문 오류코드 처리
        # if data["msg_cd"] == "APBK0919":
        #     raise KisMarketNotOpenedError(
        #         data=data,
        #         response=data["__response__"],
        #     )

        # if data["msg_cd"] == "APBK0656":
        #     raise_not_found(
        #         data,
        #         code=self.symbol,
        #         market=self.market,
        #     )

        super().__pre_init__(data)

        self.time_kst = self.time = datetime.combine(
            datetime.now(TIMEZONE).date(),
            datetime.strptime(data["output"]["ORD_TMD"], "%H%M%S").time(),
            tzinfo=TIMEZONE,
        )


def domestic_modify_order(
    self: "PyKis",
    account: str | KisAccountNumber,
    order: KisOrderNumber,
    price: ORDER_PRICE | None | EMPTY_TYPE = EMPTY,
    qty: Decimal | None | EMPTY_TYPE = EMPTY,
    condition: ORDER_CONDITION | None | EMPTY_TYPE = EMPTY,
    execution: ORDER_EXECUTION | None | EMPTY_TYPE = EMPTY,
    include_foreign: bool = False,
) -> KisDomesticModifyOrder:
    """
    한국투자증권 국내 주식 주문정정

    국내주식주문 -> 주식주문(정정취소)[v1_국내주식-003]
    (업데이트 날짜: 2024/03/31)
    """
