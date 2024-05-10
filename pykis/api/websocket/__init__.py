from pykis.api.websocket.price import KisDomesticRealtimePrice, KisOverseasRealtimePrice
from pykis.responses.websocket import KisWebsocketResponse

WEBSOCKET_RESPONSES_MAP: dict[str, type[KisWebsocketResponse]] = {
    "H0STCNT0": KisDomesticRealtimePrice,
    "HDFSCNT0": KisOverseasRealtimePrice,
}
