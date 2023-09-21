from ...._import import *

# 300 주식
# 301 선물옵션
# 302 채권
# 512 미국 나스닥 / 513 미국 뉴욕 / 529 미국 아멕스
# 515 일본
# 501 홍콩 / 543 홍콩CNY / 558 홍콩USD
# 507 베트남 하노이 / 508 베트남 호치민
# 551 중국 상해A / 552 중국 심천A'

PRDT_TYPE_CD = Literal[
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

PRDT_TYPES = {
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

# -pdno	상품번호	String	Y	12
# -prdt_type_cd	상품유형코드	String	Y	3
# -prdt_name	상품명	String	Y	60
# -prdt_name120	상품명120	String	Y	120
# -prdt_abrv_name	상품약어명	String	Y	60
# -prdt_eng_name	상품영문명	String	Y	60
# -prdt_eng_name120	상품영문명120	String	Y	120
# -prdt_eng_abrv_name	상품영문약어명	String	Y	60
# -std_pdno	표준상품번호	String	Y	12
# -shtn_pdno	단축상품번호	String	Y	12
# -prdt_sale_stat_cd	상품판매상태코드	String	Y	2
# -prdt_risk_grad_cd	상품위험등급코드	String	Y	2
# -prdt_clsf_cd	상품분류코드	String	Y	6
# -prdt_clsf_name	상품분류명	String	Y	60
# -sale_strt_dt	판매시작일자	String	Y	8
# -sale_end_dt	판매종료일자	String	Y	8
# -wrap_asst_type_cd	랩어카운트자산유형코드	String	Y	2
# -ivst_prdt_type_cd	투자상품유형코드	String	Y	4
# -ivst_prdt_type_cd_name	투자상품유형코드명	String	Y	60
# -frst_erlm_dt	최초등록일자	String	Y	8


class KisMarketSearchInfo(KisDynamicAPIResponse):
    pdno: str
    """상품번호"""
    prdt_type_cd: PRDT_TYPE_CD
    """상품유형코드"""
    prdt_name: str
    """상품명"""
    prdt_name120: str
    """상품명120"""
    prdt_abrv_name: str
    """상품약어명"""
    prdt_eng_name: str
    """상품영문명"""
    prdt_eng_name120: str
    """상품영문명120"""
    prdt_eng_abrv_name: str
    """상품영문약어명"""
    std_pdno: str
    """표준상품번호"""
    shtn_pdno: str
    """단축상품번호"""
    prdt_sale_stat_cd: str
    """상품판매상태코드"""
    prdt_risk_grad_cd: str
    """상품위험등급코드"""
    prdt_clsf_cd: str
    """상품분류코드"""
    prdt_clsf_name: str
    """상품분류명"""
    sale_strt_dt: date | None
    """판매시작일자"""
    sale_end_dt: date | None
    """판매종료일자"""
    wrap_asst_type_cd: str
    """랩어카운트자산유형코드"""
    ivst_prdt_type_cd: str
    """투자상품유형코드"""
    ivst_prdt_type_cd_name: str
    """투자상품유형코드명"""
    frst_erlm_dt: date | None
    """최초등록일자"""

    @property
    def prdt_type_name(self) -> str:
        """상품유형명"""
        return PRDT_TYPES[self.prdt_type_cd]
