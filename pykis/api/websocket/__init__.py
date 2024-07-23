from pykis.api.websocket.order_book import (
    KisAsiaRealtimeOrderBook,
    KisDomesticRealtimeOrderBook,
    KisUSRealtimeOrderBook,
)
from pykis.api.websocket.order_execution import KisDomesticRealtimeOrderExecution
from pykis.api.websocket.price import KisDomesticRealtimePrice, KisForeignRealtimePrice
from pykis.responses.websocket import KisWebsocketResponse

WEBSOCKET_RESPONSES_MAP: dict[str, type[KisWebsocketResponse]] = {
    "H0STCNT0": KisDomesticRealtimePrice,
    "HDFSCNT0": KisForeignRealtimePrice,
    "H0STASP0": KisDomesticRealtimeOrderBook,
    "HDFSASP1": KisAsiaRealtimeOrderBook,
    "HDFSASP0": KisUSRealtimeOrderBook,
    "H0STCNI0": KisDomesticRealtimeOrderExecution,
    "H0STCNI9": KisDomesticRealtimeOrderExecution,
}
