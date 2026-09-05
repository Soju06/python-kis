"""[domestic_stock] fluctuation  v1_국내주식-088

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/fluctuation` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from datetime import date
from decimal import Decimal

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisDate, KisDecimal, KisInt, KisString

FLUCTUATION = KisEndpoint(
    path="/uapi/domestic-stock/v1/ranking/fluctuation",
    tr_live="FHPST01700000",
)


class KisFluctuationItem(KisDynamic):
    """fluctuation 응답 항목 — `output` (24개 필드)"""

    stck_shrn_iscd: str = KisString["stck_shrn_iscd"]
    """주식 단축 종목코드"""
    data_rank: int = KisInt["data_rank"]
    """데이터 순위"""
    hts_kor_isnm: str = KisString["hts_kor_isnm"]
    """HTS 한글 종목명"""
    stck_prpr: Decimal = KisDecimal["stck_prpr"]
    """주식 현재가"""
    prdy_vrss: Decimal = KisDecimal["prdy_vrss"]
    """전일 대비"""
    prdy_vrss_sign: str = KisString["prdy_vrss_sign"]
    """전일 대비 부호"""
    prdy_ctrt: Decimal = KisDecimal["prdy_ctrt"]
    """전일 대비율"""
    acml_vol: int = KisInt["acml_vol"]
    """누적 거래량"""
    stck_hgpr: Decimal = KisDecimal["stck_hgpr"]
    """주식 최고가"""
    hgpr_hour: str = KisString["hgpr_hour"]
    """최고가 시간"""
    acml_hgpr_date: date = KisDate["acml_hgpr_date"]
    """누적 최고가 일자"""
    stck_lwpr: Decimal = KisDecimal["stck_lwpr"]
    """주식 최저가"""
    lwpr_hour: str = KisString["lwpr_hour"]
    """최저가 시간"""
    acml_lwpr_date: date = KisDate["acml_lwpr_date"]
    """누적 최저가 일자"""
    lwpr_vrss_prpr_rate: Decimal = KisDecimal["lwpr_vrss_prpr_rate"]
    """저가 대비 현재가 비율"""
    dsgt_date_clpr_vrss_prpr_rate: Decimal = KisDecimal["dsgt_date_clpr_vrss_prpr_rate"]
    """영업 일수 대비 현재가 비율"""
    cnnt_ascn_dynu: str = KisString["cnnt_ascn_dynu"]
    """연속 상승 일수"""
    hgpr_vrss_prpr_rate: Decimal = KisDecimal["hgpr_vrss_prpr_rate"]
    """고가 대비 현재가 비율"""
    cnnt_down_dynu: str = KisString["cnnt_down_dynu"]
    """연속 하락 일수"""
    oprc_vrss_prpr_sign: str = KisString["oprc_vrss_prpr_sign"]
    """시가 대비 부호"""
    oprc_vrss_prpr: Decimal = KisDecimal["oprc_vrss_prpr"]
    """시가 대비"""
    oprc_vrss_prpr_rate: Decimal = KisDecimal["oprc_vrss_prpr_rate"]
    """시가 대비 현재가 비율"""
    prd_rsfl: str = KisString["prd_rsfl"]
    """기간 등락"""
    prd_rsfl_rate: Decimal = KisDecimal["prd_rsfl_rate"]
    """기간 등락 비율"""


class KisFluctuation(KisAPIResponse):
    """fluctuation 응답"""

    __path__ = None

    output: list[KisFluctuationItem] = KisList(KisFluctuationItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 7개:
#   stck_shrn_iscd, hts_kor_isnm, hgpr_hour, lwpr_hour, cnnt_ascn_dynu, cnnt_down_dynu
#   prd_rsfl
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
