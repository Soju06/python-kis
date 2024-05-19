from pykis.api.websocket.asking_price import (
    KisAsiaRealtimeAskingPrice,
    KisDomesticRealtimeAskingPrice,
    KisUSARealtimeAskingPrice,
)
from pykis.api.websocket.price import KisDomesticRealtimePrice, KisOverseasRealtimePrice
from pykis.responses.websocket import KisWebsocketResponse

WEBSOCKET_RESPONSES_MAP: dict[str, type[KisWebsocketResponse]] = {
    "H0STCNT0": KisDomesticRealtimePrice,
    "HDFSCNT0": KisOverseasRealtimePrice,
    "H0STASP0": KisDomesticRealtimeAskingPrice,
    "HDFSASP1": KisAsiaRealtimeAskingPrice,
    "HDFSASP0": KisUSARealtimeAskingPrice,
}
