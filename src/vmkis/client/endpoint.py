"""엔드포인트 선언 스펙.

KIS 는 같은 기능이라도 실전/모의의 TR ID 가 다르고(잔고: `TTTC8434R` /
`VTTC8434R`), 시세처럼 모의 서버에 아예 없는 TR 도 있습니다. 그 규칙이
엔드포인트마다 반복되면 **빠뜨릴 기회**가 생깁니다. 특히 `domain="live"` 을
누락하면 모의 계정에서만 터지는 버그가 됩니다.

`KisEndpoint` 는 "이 API 는 이런 것"만 데이터로 적고, 실행 규칙은
`VmKis.call()` 한 곳에 둡니다.

    DOMESTIC_BALANCE = KisEndpoint(
        path="/uapi/domestic-stock/v1/trading/inquire-balance",
        tr_live="TTTC8434R",
        tr_paper="VTTC8434R",
        page_size=100,
    )

    kis.call(DOMESTIC_BALANCE, form=[account], page=page, response_type=...)

이 방식은 저장소에 이미 절반쯤 있었습니다 — `api/account/order.py` 가
`(실전여부, 주문종류) -> TR ID` 표를 들고 있었습니다. 그 표에서 **실전/모의
차원만 떼어내 `KisEndpoint` 로 옮기면** 나머지 차원은 그대로
`dict[key, KisEndpoint]` 로 남습니다. 지금은 표가 전부 이 형태이며
(`DOMESTIC_ORDER_ENDPOINTS`, `FOREIGN_ORDER_MODIFY_ENDPOINTS` 등),
문자열 표는 남아 있지 않습니다.

이슈 #43 참고.
"""

from dataclasses import dataclass
from typing import Literal

__all__ = ["KisEndpoint"]

DOMAIN_TYPE = Literal["live", "paper"]


@dataclass(frozen=True)
class KisEndpoint:
    """단일 KIS 엔드포인트의 선언적 스펙.

    `frozen=True` 인 이유: 스펙은 상수입니다. 실행 중에 바뀌면 같은 엔드포인트가
    호출마다 다른 곳을 가리키게 됩니다.
    """

    path: str
    """`/uapi/...` 로 시작하는 요청 경로."""

    tr_live: str
    """실전도메인 TR ID."""

    tr_paper: str | None = None
    """모의도메인 TR ID.

    `None` 이면 **모의투자를 지원하지 않는 TR** 입니다. 이때 모의 계좌로
    호출해도 실전 도메인으로 보냅니다(시세 조회 등이 이 경우입니다).
    """

    method: Literal["GET", "POST"] = "GET"

    domain_override: DOMAIN_TYPE | None = None
    """도메인을 강제합니다.

    `tr_paper` 이 있어도 이 값이 우선합니다. 실전 계좌인데 굳이 모의로
    보내야 하는 경우처럼 예외적인 상황에만 씁니다.

    모의 미지원 TR 은 `tr_paper` 을 생략하는 것으로 충분하므로
    `domain_override="live"` 을 함께 줄 필요가 없습니다.
    """

    page_size: int | None = None
    """연속조회 커서 길이. `KisPage.to()` 에 넘길 값입니다.

    `None` 이면 페이징이 없는 엔드포인트입니다.
    """

    def resolve(self, paper: bool) -> tuple[str, DOMAIN_TYPE]:
        """계좌 종류에 맞는 `(TR ID, 도메인)` 을 고릅니다.

        이 판단이 흩어져 있으면 매번 다시 기억해야 합니다. 규칙은 셋뿐입니다.

        1. 모의 계좌인데 이 TR 에 모의 버전이 없으면 → **실전 도메인**
        2. 모의 계좌이고 모의 버전이 있으면 → 모의
        3. `domain_override` 가 있으면 위를 덮어씀
        """
        if paper and self.tr_paper is not None:
            tr_id: str = self.tr_paper
            domain: DOMAIN_TYPE = "paper"
        else:
            # 실전 계좌이거나, 모의 계좌인데 모의 TR 이 없는 경우.
            # 후자에서 모의 도메인으로 보내면 "없는 TR" 오류가 납니다.
            tr_id = self.tr_live
            domain = "live"

        if self.domain_override is not None:
            domain = self.domain_override

        return tr_id, domain
