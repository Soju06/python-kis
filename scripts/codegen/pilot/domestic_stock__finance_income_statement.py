"""[domestic_stock] finance_income_statement  v1_국내주식-079

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/finance_income_statement` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisString

FINANCE_INCOME_STATEMENT = KisEndpoint(
    path="/uapi/domestic-stock/v1/finance/income-statement",
    tr_live="FHKST66430200",
)


class KisFinanceIncomeStatementItem(KisDynamic):
    """finance_income_statement 응답 항목 — `output` (13개 필드)"""

    stac_yymm: str = KisString["stac_yymm"]
    """결산 년월"""
    sale_account: str = KisString["sale_account"]
    """매출액"""
    sale_cost: str = KisString["sale_cost"]
    """매출 원가"""
    sale_totl_prfi: str = KisString["sale_totl_prfi"]
    """매출 총 이익"""
    depr_cost: str = KisString["depr_cost"]
    """감가상각비"""
    sell_mang: str = KisString["sell_mang"]
    """판매 및 관리비"""
    bsop_prti: str = KisString["bsop_prti"]
    """영업 이익"""
    bsop_non_ernn: str = KisString["bsop_non_ernn"]
    """영업 외 수익"""
    bsop_non_expn: str = KisString["bsop_non_expn"]
    """영업 외 비용"""
    op_prfi: str = KisString["op_prfi"]
    """경상 이익"""
    spec_prfi: str = KisString["spec_prfi"]
    """특별 이익"""
    spec_loss: str = KisString["spec_loss"]
    """특별 손실"""
    thtr_ntin: str = KisString["thtr_ntin"]
    """당기순이익"""


class KisFinanceIncomeStatement(KisAPIResponse):
    """finance_income_statement 응답"""

    __path__ = None

    # ⚠️ `output` 이 리스트인지 단건인지 원본이 알려주지 않습니다
    #    (샘플이 `isinstance(x, list)` 로 방어하고 있습니다).
    #    실제 응답을 보고 KisList / KisObject 중 하나로 확정하세요.
    output: list[KisFinanceIncomeStatementItem] = KisList(KisFinanceIncomeStatementItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 13개:
#   stac_yymm, sale_account, sale_cost, sale_totl_prfi, depr_cost, sell_mang
#   bsop_prti, bsop_non_ernn, bsop_non_expn, op_prfi, spec_prfi, spec_loss
#   thtr_ntin
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
