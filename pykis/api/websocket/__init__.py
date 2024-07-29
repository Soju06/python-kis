from pykis.api.websocket.order_book import (
    KisAsiaRealtimeOrderbook,
    KisDomesticRealtimeOrderbook,
    KisUSRealtimeOrderbook,
)
from pykis.api.websocket.order_execution import KisDomesticRealtimeOrderExecution
from pykis.api.websocket.price import KisDomesticRealtimePrice, KisForeignRealtimePrice
from pykis.responses.websocket import KisWebsocketResponse

WEBSOCKET_RESPONSES_MAP: dict[str, type[KisWebsocketResponse]] = {
    "H0STCNT0": KisDomesticRealtimePrice,
    "HDFSCNT0": KisForeignRealtimePrice,
    "H0STASP0": KisDomesticRealtimeOrderbook,
    "HDFSASP1": KisAsiaRealtimeOrderbook,
    "HDFSASP0": KisUSRealtimeOrderbook,
    "H0STCNI0": KisDomesticRealtimeOrderExecution,
    "H0STCNI9": KisDomesticRealtimeOrderExecution,
}
