"""[domestic_stock] chk_holiday  국내주식-040

**이 파일은 생성물입니다.** `scripts/generate_endpoint.py` 가 만들었습니다.
손으로 고치면 다음 생성 때 사라집니다.

출처 스펙: `examples_llm/domestic_stock/chk_holiday` — **사실만** 옮겼습니다
(경로 · TR ID · 필드명 · 한글 라벨). 원문 설명문은 옮기지 않습니다.

이슈 [#21](https://github.com/visualmoney/vm-stock-kis/issues/21) 파일럿 산출물이며,
아직 패키지에 편입되지 않았습니다.
"""

from datetime import date

from vmkis.client.endpoint import KisEndpoint
from vmkis.client.page import NO_SUFFIX
from vmkis.responses.dynamic import KisDynamic, KisList
from vmkis.responses.response import KisAPIResponse
from vmkis.responses.types import KisBool, KisDate, KisString

CHK_HOLIDAY = KisEndpoint(
    path="/uapi/domestic-stock/v1/quotations/chk-holiday",
    tr_live="CTCA0903R",
    page_size=NO_SUFFIX,  # 접미사 없는 CTX_AREA_FK
)


class KisChkHolidayItem(KisDynamic):
    """chk_holiday 응답 항목 — `output` (6개 필드)"""

    bass_dt: date = KisDate["bass_dt"]
    """기준일자"""
    wday_dvsn_cd: str = KisString["wday_dvsn_cd"]
    """요일구분코드"""
    bzdy_yn: bool = KisBool["bzdy_yn"]
    """영업일여부"""
    tr_day_yn: bool = KisBool["tr_day_yn"]
    """거래일여부"""
    opnd_yn: bool = KisBool["opnd_yn"]
    """개장일여부"""
    sttl_day_yn: bool = KisBool["sttl_day_yn"]
    """결제일여부"""


class KisChkHoliday(KisAPIResponse):
    """chk_holiday 응답"""

    __path__ = None

    # ⚠️ `output` 이 리스트인지 단건인지 원본이 알려주지 않습니다
    #    (샘플이 `isinstance(x, list)` 로 방어하고 있습니다).
    #    실제 응답을 보고 KisList / KisObject 중 하나로 확정하세요.
    output: list[KisChkHolidayItem] = KisList(KisChkHolidayItem)["output"]
    """output 목록"""
