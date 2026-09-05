"""[domestic_stock] volume_rank  v1_국내주식-047

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/volume_rank` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from decimal import Decimal

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisDecimal, KisInt, KisString

VOLUME_RANK = KisEndpoint(
    path="/uapi/domestic-stock/v1/quotations/volume-rank",
    tr_live="FHPST01710000",
)


class KisVolumeRankItem(KisDynamic):
    """volume_rank 응답 항목 — `output` (19개 필드)"""

    hts_kor_isnm: str = KisString["hts_kor_isnm"]
    """HTS 한글 종목명"""
    mksc_shrn_iscd: str = KisString["mksc_shrn_iscd"]
    """가중권 단축 종목코드"""
    data_rank: int = KisInt["data_rank"]
    """데이터 순위"""
    stck_prpr: Decimal = KisDecimal["stck_prpr"]
    """주식 현재가"""
    prdy_vrss_sign: str = KisString["prdy_vrss_sign"]
    """전일 대비 부호"""
    prdy_vrss: Decimal = KisDecimal["prdy_vrss"]
    """전일 대비"""
    prdy_ctrt: Decimal = KisDecimal["prdy_ctrt"]
    """전일 대비율"""
    acml_vol: int = KisInt["acml_vol"]
    """누적 거래량"""
    prdy_vol: int = KisInt["prdy_vol"]
    """전일 거래량"""
    lstn_stcn: str = KisString["lstn_stcn"]
    """상장 주식수"""
    avrg_vol: int = KisInt["avrg_vol"]
    """평균 거래량"""
    n_befr_clpr_vrss_prpr_rate: Decimal = KisDecimal["n_befr_clpr_vrss_prpr_rate"]
    """전일종가대비현재가(%)"""
    vol_inrt: str = KisString["vol_inrt"]
    """거래량증가율"""
    vol_tnrt: str = KisString["vol_tnrt"]
    """거래량회전율"""
    nday_vol_tnrt: str = KisString["nday_vol_tnrt"]
    """N일 거래량회전율"""
    avrg_tr_pbmn: Decimal = KisDecimal["avrg_tr_pbmn"]
    """평균 거래 대금"""
    tr_pbmn_tnrt: str = KisString["tr_pbmn_tnrt"]
    """거래대금회전율"""
    nday_tr_pbmn_tnrt: str = KisString["nday_tr_pbmn_tnrt"]
    """N일 거래대금회전율"""
    acml_tr_pbmn: Decimal = KisDecimal["acml_tr_pbmn"]
    """누적 거래 대금"""


class KisVolumeRank(KisAPIResponse):
    """volume_rank 응답"""

    __path__ = None

    output: list[KisVolumeRankItem] = KisList(KisVolumeRankItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 8개:
#   hts_kor_isnm, mksc_shrn_iscd, lstn_stcn, vol_inrt, vol_tnrt, nday_vol_tnrt
#   tr_pbmn_tnrt, nday_tr_pbmn_tnrt
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
