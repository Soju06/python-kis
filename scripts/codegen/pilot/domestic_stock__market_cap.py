"""[domestic_stock] market_cap  v1_국내주식-091

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/market_cap` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from decimal import Decimal

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisDecimal, KisInt, KisString

MARKET_CAP = KisEndpoint(
    path="/uapi/domestic-stock/v1/ranking/market-cap",
    tr_live="FHPST01740000",
)


class KisMarketCapItem(KisDynamic):
    """market_cap 응답 항목 — `output` (11개 필드)"""

    mksc_shrn_iscd: str = KisString["mksc_shrn_iscd"]
    """유가증권 단축 종목코드"""
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
    lstn_stcn: str = KisString["lstn_stcn"]
    """상장 주수"""
    stck_avls: str = KisString["stck_avls"]
    """시가 총액"""
    mrkt_whol_avls_rlim: str = KisString["mrkt_whol_avls_rlim"]
    """시장 전체 시가총액 비중"""


class KisMarketCap(KisAPIResponse):
    """market_cap 응답"""

    __path__ = None

    output: list[KisMarketCapItem] = KisList(KisMarketCapItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 5개:
#   mksc_shrn_iscd, hts_kor_isnm, lstn_stcn, stck_avls, mrkt_whol_avls_rlim
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
