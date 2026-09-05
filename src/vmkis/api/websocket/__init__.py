from vmkis.api.websocket.order_book import (
    KisAsiaRealtimeOrderbook,
    KisDomesticRealtimeOrderbook,
    KisUSRealtimeOrderbook,
)
from vmkis.api.websocket.order_execution import (
    KisDomesticRealtimeOrderExecution,
    KisForeignRealtimeOrderExecution,
)
from vmkis.api.websocket.price import KisDomesticRealtimePrice, KisForeignRealtimePrice

# 위 import 들이 곧 등록입니다. 각 응답 클래스에 붙은
# `@register_websocket_response(...)` 데코레이터가 클래스 정의 시점에
# `vmkis.responses.websocket.WEBSOCKET_RESPONSES_MAP` 을 채웁니다.
#
# 예전에는 이 파일이 dict 리터럴을 소유하고 `client/websocket.py` 가 그것을
# import 했습니다. 통신 계층이 상위 계층에 의존하는 역방향 간선이었습니다
# (이슈 #17).
#
# 하위 호환을 위해 이름은 그대로 재export 합니다.
from vmkis.responses.websocket import (
    WEBSOCKET_RESPONSES_MAP,  # noqa: E402
    KisWebsocketResponse,
)

__all__ = [
    "KisAsiaRealtimeOrderbook",
    "KisDomesticRealtimeOrderExecution",
    "KisDomesticRealtimeOrderbook",
    "KisDomesticRealtimePrice",
    "KisForeignRealtimeOrderExecution",
    "KisForeignRealtimePrice",
    "KisUSRealtimeOrderbook",
    "KisWebsocketResponse",
    "WEBSOCKET_RESPONSES_MAP",
]
