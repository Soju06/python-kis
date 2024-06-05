from pykis.api.websocket.asking_price import (
    KisAsiaRealtimeAskingPrice,
    KisDomesticRealtimeAskingPrice,
    KisUSRealtimeAskingPrice,
)
from pykis.api.websocket.order_execution import KisDomesticRealtimeOrderExecution
from pykis.api.websocket.price import KisDomesticRealtimePrice, KisForeignRealtimePrice
from pykis.responses.websocket import KisWebsocketResponse

WEBSOCKET_RESPONSES_MAP: dict[str, type[KisWebsocketResponse]] = {
    "H0STCNT0": KisDomesticRealtimePrice,
    "HDFSCNT0": KisForeignRealtimePrice,
    "H0STASP0": KisDomesticRealtimeAskingPrice,
    "HDFSASP1": KisAsiaRealtimeAskingPrice,
    "HDFSASP0": KisUSRealtimeAskingPrice,
    "H0STCNI0": KisDomesticRealtimeOrderExecution,
    "H0STCNI9": KisDomesticRealtimeOrderExecution,
}
