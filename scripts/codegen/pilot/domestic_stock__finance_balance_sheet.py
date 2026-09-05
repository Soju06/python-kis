"""[domestic_stock] finance_balance_sheet  v1_국내주식-078

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/finance_balance_sheet` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisString

FINANCE_BALANCE_SHEET = KisEndpoint(
    path="/uapi/domestic-stock/v1/finance/balance-sheet",
    tr_live="FHKST66430100",
)


class KisFinanceBalanceSheetItem(KisDynamic):
    """finance_balance_sheet 응답 항목 — `output` (11개 필드)"""

    stac_yymm: str = KisString["stac_yymm"]
    """결산 년월"""
    cras: str = KisString["cras"]
    """유동자산"""
    fxas: str = KisString["fxas"]
    """고정자산"""
    total_aset: str = KisString["total_aset"]
    """자산총계"""
    flow_lblt: str = KisString["flow_lblt"]
    """유동부채"""
    fix_lblt: str = KisString["fix_lblt"]
    """고정부채"""
    total_lblt: str = KisString["total_lblt"]
    """부채총계"""
    cpfn: str = KisString["cpfn"]
    """자본금"""
    cfp_surp: str = KisString["cfp_surp"]
    """자본 잉여금"""
    prfi_surp: str = KisString["prfi_surp"]
    """이익 잉여금"""
    total_cptl: str = KisString["total_cptl"]
    """자본총계"""


class KisFinanceBalanceSheet(KisAPIResponse):
    """finance_balance_sheet 응답"""

    __path__ = None

    output: list[KisFinanceBalanceSheetItem] = KisList(KisFinanceBalanceSheetItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 11개:
#   stac_yymm, cras, fxas, total_aset, flow_lblt, fix_lblt
#   total_lblt, cpfn, cfp_surp, prfi_surp, total_cptl
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
