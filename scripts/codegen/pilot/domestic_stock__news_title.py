"""[domestic_stock] news_title  국내주식-141

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/news_title` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from datetime import date, time

from vmkis.client.endpoint import KisEndpoint
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisDate, KisString, KisTime

NEWS_TITLE = KisEndpoint(
    path="/uapi/domestic-stock/v1/quotations/news-title",
    tr_live="FHKST01011800",
)


class KisNewsTitleItem(KisDynamic):
    """news_title 응답 항목 — `output` (12개 필드)"""

    cntt_usiq_srno: str = KisString["cntt_usiq_srno"]
    """내용 조회용 일련번호"""
    news_ofer_entp_code: str = KisString["news_ofer_entp_code"]
    """뉴스 제공 업체 코드"""
    data_dt: date = KisDate["data_dt"]
    """작성일자"""
    data_tm: time = KisTime["data_tm"]
    """작성시간"""
    hts_pbnt_titl_cntt: str = KisString["hts_pbnt_titl_cntt"]
    """HTS 공시 제목 내용"""
    news_lrdv_code: str = KisString["news_lrdv_code"]
    """뉴스 대구분"""
    dorg: str = KisString["dorg"]
    """자료원"""
    iscd1: str = KisString["iscd1"]
    """종목 코드1"""
    iscd2: str = KisString["iscd2"]
    """종목 코드2"""
    iscd3: str = KisString["iscd3"]
    """종목 코드3"""
    iscd4: str = KisString["iscd4"]
    """종목 코드4"""
    iscd5: str = KisString["iscd5"]
    """종목 코드5"""


class KisNewsTitle(KisAPIResponse):
    """news_title 응답"""

    __path__ = None

    # ⚠️ `output` 이 리스트인지 단건인지 원본이 알려주지 않습니다
    #    (샘플이 `isinstance(x, list)` 로 방어하고 있습니다).
    #    실제 응답을 보고 KisList / KisObject 중 하나로 확정하세요.
    output: list[KisNewsTitleItem] = KisList(KisNewsTitleItem)["output"]
    """output 목록"""


# 타입을 추정하지 못해 KisString 으로 둔 필드 8개:
#   cntt_usiq_srno, hts_pbnt_titl_cntt, dorg, iscd1, iscd2, iscd3
#   iscd4, iscd5
# KisString 은 어떤 문자열도 받으므로 런타임 오류가 나지 않습니다.
# 실제 응답을 보고 승격하세요.
