# 실시간 응답 클래스 등록 (부수효과 목적의 import).
#
# 각 응답 클래스의 `@register_websocket_response(...)` 가 클래스 정의 시점에
# 레지스트리를 채웁니다. 이 모듈이 로드되지 않으면 레지스트리가 비고,
# **구독은 되지만 수신 이벤트가 조용히 버려집니다.**
#
# 지금도 `VmKis` -> adapter -> api 경로로 우연히 로드되기는 하지만, 어댑터를
# 리팩터링하면 그 경로가 끊길 수 있습니다. 여기서 명시적으로 고정합니다.
# `tests/unit/api/websocket/test_registry.py` 가 이것을 지킵니다. (이슈 #17)
import vmkis.api.websocket  # noqa: F401
from vmkis.__env__ import (
    __author__,
    __author_email__,
    __authors__,
    __license__,
    __maintainers__,
    __package_name__,
    __upstream_author__,
    __upstream_url__,
    __url__,
    __version__,
)

# 핵심 인증/클래스
from vmkis.client.auth import KisAuth
from vmkis.exceptions import *
from vmkis.kis import VmKis

# 공개 타입은 `vmkis.public_types`에서 재export
from vmkis.public_types import (
    Balance,
    Chart,
    MarketInfo,
    Order,
    Orderbook,
    Quote,
    TradingHours,
)

# isort: split
#
# 초보자용 유틸.
#
# 예전에는 아래 두 줄이 각각 `try/except ImportError: ... = None` 로 감싸여
# 있었습니다. 그 폴백의 이력은 이렇습니다.
#
#   1. 처음에는 하나의 `try` 에 `except Exception` 이었습니다.
#   2. helpers 가 실패하면 이미 성공한 SimpleKIS 까지 None 으로 덮어써져서
#      try 를 둘로 쪼갰고, except 도 ImportError 로 좁혔습니다.
#   3. 그래도 남는 문제가 이것입니다 — 폴백이 걸리면 사용자가 받는 것은
#      `TypeError: 'NoneType' object is not callable` 이고, **pyyaml 도
#      helpers 도 이름이 나오지 않습니다.** 무엇을 설치해야 하는지, 어디가
#      고장 났는지 알 수 없습니다.
#
# 이슈 #73 에서 폴백을 없앴습니다. pyyaml 은 필수 의존성으로 유지하므로
# (`pyproject.toml` 참고) 여기서 남는 ImportError 원인은 helpers/simple
# **자체의 버그**뿐이고, 그건 조용히 None 이 되면 안 됩니다.
#
# `tests/unit/test_helpers_import_contract.py` 가 이것을 지킵니다.
#
# `# isort: split` 은 위 핵심 블록과 이 두 줄을 갈라 두기 위한 것입니다.
# 없으면 정렬이 helpers 를 `kis` 앞으로, simple 을 맨 뒤로 흩어 놓아 이
# 주석이 가리키는 "두 줄"이 서로 떨어집니다.
from vmkis.helpers import create_client, save_config_interactive
from vmkis.simple import SimpleKIS

__all__ = [
    # 핵심
    "VmKis",
    "KisAuth",
    # 공개 타입
    "Quote",
    "Balance",
    "Order",
    "Chart",
    "Orderbook",
    "MarketInfo",
    "TradingHours",
    # 초보자 도구
    "SimpleKIS",
    "create_client",
    "save_config_interactive",
]
