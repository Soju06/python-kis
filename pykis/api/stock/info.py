from typing import TYPE_CHECKING, Literal
from pykis.api.stock.market import MARKET_TYPE

from pykis.client.exception import KisAPIError
from pykis.responses.response import KisAPIResponse
from pykis.responses.types import KisString

if TYPE_CHECKING:
    from pykis.kis import PyKis

MARKET_TYPE_MAP = {
    "주식": ["300"],
    "선물옵션": ["301"],
    "채권": ["302"],
    "국내": ["300", "301", "302"],
    "KRX": ["300", "301", "302"],
    "나스닥": ["512"],
    "NASD": ["512"],
    "뉴욕": ["513"],
    "NYSE": ["513"],
    "아멕스": ["529"],
    "AMEX": ["529"],
    "미국": ["512", "513", "529"],
    "일본": ["515"],
    "TKSE": ["515"],
    "홍콩": ["501"],
    "SEHK": ["501"],
    "홍콩CNY": ["543"],
    "홍콩USD": ["558"],
    "홍콩전체": ["501", "543", "558"],
    "하노이": ["507"],
    "HASE": ["507"],
    "호치민": ["508"],
    "VNSE": ["508"],
    "베트남": ["507", "508"],
    "상해": ["551"],
    "SHAA": ["551"],
    "심천": ["552"],
    "SZAA": ["552"],
    "중국": ["551", "552"],
    "전체": [
        "300",
        "301",
        "302",
        "512",
        "513",
        "529",
        "515",
        "501",
        "543",
        "558",
        "507",
        "508",
        "551",
        "552",
    ],
}

R_MARKET_TYPE_MAP = {
    "300": "주식",
    "301": "선물옵션",
    "302": "채권",
    "512": "나스닥",
    "513": "뉴욕",
    "529": "아멕스",
    "515": "일본",
    "501": "홍콩",
    "543": "홍콩CNY",
    "558": "홍콩USD",
    "507": "하노이",
    "508": "호치민",
    "551": "상해",
    "552": "심천",
}


MARKET_CODE = Literal[
    "300",
    "301",
    "302",
    "512",
    "513",
    "529",
    "515",
    "501",
    "543",
    "558",
    "507",
    "508",
    "551",
    "552",
]

MARKET_KOR_TYPE = Literal[
    "주식",
    "선물옵션",
    "채권",
    "나스닥",
    "뉴욕",
    "아멕스",
    "일본",
    "홍콩",
    "홍콩CNY",
    "홍콩USD",
    "하노이",
    "호치민",
    "상해",
    "심천",
]

MARKET_CODE_MAP = {
    "300": "KRX",
    "301": "KRX",
    "302": "KRX",
    "512": "NASD",
    "513": "NYSE",
    "529": "AMEX",
    "515": "TKSE",
    "501": "SEHK",
    "543": "SEHK",
    "558": "SEHK",
    "507": "HASE",
    "508": "VNSE",
    "551": "SHAA",
    "552": "SZAA",
}


class KisStockInfo(KisAPIResponse):
    """상품기본정보"""

    code: str = KisString["shtn_pdno"]
    """종목코드"""
    std_code: str = KisString["std_pdno"]
    """표준코드"""
    name_kor: str = KisString["prdt_abrv_name"]
    """종목명"""
    full_name_kor: str = KisString["prdt_name120"]
    """종목전체명"""
    name_eng: str = KisString["prdt_eng_abrv_name"]
    """종목영문명"""
    full_name_eng: str = KisString["prdt_eng_name120"]
    """종목영문전체명"""

    @property
    def name(self) -> str:
        """종목명"""
        return self.name_kor

    market_code: MARKET_CODE = KisString["prdt_type_cd"]
    """상품유형코드"""

    @property
    def market(self) -> MARKET_TYPE:
        """상품유형타입"""
        return MARKET_CODE_MAP[self.market_code]  # type: ignore

    @property
    def market_name(self) -> str:
        """상품유형명"""
        return R_MARKET_TYPE_MAP[self.market_code]

    @property
    def overseas(self) -> bool:
        """해외종목 여부"""
        return self.market_code not in ["300", "301", "302"]


MARKET_INFO_TYPES = (
    MARKET_KOR_TYPE | MARKET_TYPE | Literal["국내", "미국", "홍콩전체", "베트남", "중국", "전체"] | MARKET_CODE | None
)


def info(
    self: "PyKis",
    code: str,
    market: MARKET_INFO_TYPES = "주식",
):
    """
    상품기본정보 조회.

    국내주식시세 -> 상품기본조회[v1_국내주식-029]
    (업데이트 날짜: 2023/09/05)

    Args:
        code (str): 종목코드
        market (str): 상품유형명

    Raises:
        KisAPIError: API 호출에 실패한 경우
    """
    if not code:
        raise ValueError("종목 코드를 입력해주세요.")

    if market == None:
        market = "전체"

    err = None

    for market_ in MARKET_TYPE_MAP.get(market, [market]):
        try:
            result = self.fetch(
                "/uapi/domestic-stock/v1/quotations/search-info",
                api="CTPF1604R",
                params={
                    "PDNO": code,
                    "PRDT_TYPE_CD": market_,
                },
                domain="real",
                response_type=KisStockInfo,
            )

            return result
        except KisAPIError as e:
            if e.rt_cd == 7:
                # 조회된 데이터가 없는 경우
                err = e
                continue

            raise e

    raise err or ValueError("종목 정보를 찾을 수 없습니다.")
