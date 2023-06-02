from ...._import import *
from .revisable_order import ORD_DVSN_CD_CODES
from .order_cash import KisStockOrderBase


CCLD_CODES = {
    # 00 : 전체
    # 01 : 체결
    # 02 : 미체결
    "전체": "00",
    "체결": "01",
    "미체결": "02",
}

INQR_DVSN_3_CODES = {
    # 00 : 전체
    # 01 : 현금
    # 02 : 융자
    # 03 : 대출
    # 04 : 대주
    "전체": "00",
    "현금": "01",
    "융자": "02",
    "대출": "03",
    "대주": "04",
}

INQR_DVSN_1_CODES = {
    # 공란 : 전체
    # 1 : ELW
    # 2 : 프리보드
    "전체": "",
    "ELW": "1",
    "프리보드": "2",
}

CCLD_TYPE = Literal["전체", "체결", "미체결", "00", "01", "02"]
INQR_DVSN_3_CODES_TYPE = Literal[
    "전체", "현금", "융자", "대출", "대주", "00", "01", "02", "03", "04"
]
INQR_DVSN_1_CODES_TYPE = Literal["전체", "ELW", "프리보드", "", "1", "2"]

# -ORD_DT	주문일자	String	Y	8	주문일자
# -ORD_GNO_BRNO	주문채번지점번호	String	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
# -ODNO	주문번호	String	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
# -ORGN_ODNO	원주문번호	String	Y	10	이전 주문에 채번된 주문번호
# -ORD_DVSN_NAME	주문구분명	String	Y	60
# -SLL_BUY_DVSN_CD	매도매수구분코드	String	Y	2	01 : 매도
# 02 : 매수
# -SLL_BUY_DVSN_CD_NAME	매도매수구분코드명	String	Y	60
# -PDNO	상품번호	String	Y	12	종목번호(6자리)
# -PRDT_NAME	상품명	String	Y	60	종목명
# -ORD_QTY	주문수량	String	Y	10
# -ORD_UNPR	주문단가	String	Y	19
# -ORD_TMD	주문시각	String	Y	6
# -TOT_CCLD_QTY	총체결수량	String	Y	10
# -AVG_PRVS	평균가	String	Y	19	체결평균가 ( 총체결금액 / 총체결수량 )
# -CNCL_YN	취소여부	String	Y	1
# -TOT_CCLD_AMT	총체결금액	String	Y	19
# -LOAN_DT	대출일자	String	Y	8
# -ORD_DVSN_CD	주문구분코드	String	Y	2	00 : 지정가
# 01 : 시장가
# 02 : 조건부지정가
# 03 : 최유리지정가
# 04 : 최우선지정가
# 05 : 장전 시간외
# 06 : 장후 시간외
# 07 : 시간외 단일가
# 08 : 자기주식
# 09 : 자기주식S-Option
# 10 : 자기주식금전신탁
# 11 : IOC지정가 (즉시체결,잔량취소)
# 12 : FOK지정가 (즉시체결,전량취소)
# 13 : IOC시장가 (즉시체결,잔량취소)
# 14 : FOK시장가 (즉시체결,전량취소)
# 15 : IOC최유리 (즉시체결,잔량취소)
# 16 : FOK최유리 (즉시체결,전량취소)
# -CNCL_CFRM_QTY	취소확인수량	String	Y	10
# -RMN_QTY	잔여수량	String	Y	10
# -RJCT_QTY	거부수량	String	Y	10
# -CCLD_CNDT_NAME	체결조건명	String	Y	10
# -INFM_TMD	통보시각	String	Y	6	※ 실전투자계좌로는 해당값이 제공되지 않습니다.
# -CTAC_TLNO	연락전화번호	String	Y	20
# -PRDT_TYPE_CD	상품유형코드	String	Y	3	300 : 주식
# 301 : 선물옵션
# 302 : 채권
# 306 : ELS
# -EXCG_DVSN_CD	거래소구분코드	String	Y	2	01 : 한국증권
# 02 : 증권거래소
# 03 : 코스닥
# 04 : K-OTC
# 05 : 선물거래소
# 06 : CME
# 07 : EUREX
# 21 : 금현물
# 51 : 홍콩
# 52 : 상해B
# 53 : 심천
# 54 : 홍콩거래소
# 55 : 미국
# 56 : 일본
# 57 : 상해A
# 58 : 심천A
# 59 : 베트남
# 61 : 장전시간외시장
# 64 : 경쟁대량매매
# 65 : 경매매시장
# 81 : 시간외단일가시장

SLL_BUY_DVSN_CD_CODES = {
    "01": "매도",
    "02": "매수",
}

PRDT_TYPE_CD_CODES = {
    "300": "주식",
    "301": "선물옵션",
    "302": "채권",
    "306": "ELS",
}

EXCG_DVSN_CD_CODES = {
    "01": "한국증권",
    "02": "증권거래소",
    "03": "코스닥",
    "04": "K-OTC",
    "05": "선물거래소",
    "06": "CME",
    "07": "EUREX",
    "21": "금현물",
    "51": "홍콩",
    "52": "상해B",
    "53": "심천",
    "54": "홍콩거래소",
    "55": "미국",
    "56": "일본",
    "57": "상해A",
    "58": "심천A",
    "59": "베트남",
    "61": "장전시간외시장",
    "64": "경쟁대량매매",
    "65": "경매매시장",
    "81": "시간외단일가시장",
}


class KisStockDailyOrder(KisDynamic):
    ord_dt: datetime
    """주문일자"""
    ord_gno_brno: str
    """주문채번지점번호"""
    odno: str
    """주문번호"""
    orgn_odno: str
    """원주문번호"""
    ord_dvsn_name: str
    """주문구분명"""
    sll_buy_dvsn_cd: Literal["01", "02"]
    """매도매수구분코드"""
    sll_buy_dvsn_cd_name: str
    """매도매수구분코드명"""
    pdno: str
    """상품번호"""
    prdt_name: str
    """상품명"""
    ord_qty: int
    """주문수량"""
    ord_unpr: int
    """주문단가"""
    ord_tmd: time
    """주문시각"""
    tot_ccdl_qty: int
    """총체결수량"""
    avg_prvs: int
    """평균가"""
    cncl_yn: bool
    """취소여부"""
    tot_ccdl_amt: int
    """총체결금액"""
    loan_dt: datetime | None
    """대출일자"""
    ord_dvsn_cd: Literal[
        "00",
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
    ]
    """주문구분코드"""
    cncl_cfrm_qty: int
    """취소확인수량"""
    rmn_qty: int
    """잔여수량"""
    rjct_qty: int
    """거부수량"""
    cctd_cndt_name: str
    """체결조건명"""
    infm_tmd: time
    """통보시각"""
    ctac_tlno: str
    """연락전화번호"""
    prdt_type_cd: Literal["300", "301", "302", "306"]
    excg_dvsn_cd: Literal[
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "21",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "61",
        "64",
        "65",
        "81",
    ]

    @property
    def sll_buy_dvsn_name(self) -> str | None:
        return SLL_BUY_DVSN_CD_CODES.get(self.sll_buy_dvsn_cd)

    @property
    def ord_dvsn_cd_name(self) -> str | None:
        return ORD_DVSN_CD_CODES.get(self.ord_dvsn_cd)

    @property
    def prdt_type_name(self) -> str | None:
        return PRDT_TYPE_CD_CODES.get(self.prdt_type_cd)

    @property
    def excg_dvsn_name(self) -> str | None:
        return EXCG_DVSN_CD_CODES.get(self.excg_dvsn_cd)

    @property
    def order(self) -> KisStockOrderBase:
        """주문"""
        return KisStockOrderBase(self.ord_gno_brno, self.odno, self.ord_tmd)

    @property
    def order_date(self) -> datetime:
        """주문일시"""
        return datetime.combine(self.ord_dt, self.ord_tmd)


class KisStockDailyOrders(KisDynamicPagingAPIResponse):
    # -TOT_ORD_QTY	총주문수량	String	Y	10	미체결주문수량 + 체결수량 (취소주문제외)
    # -TOT_CCLD_QTY	총체결수량	String	Y	10
    # -PCHS_AVG_PRIC	매입평균가격	String	Y	22	총체결금액 / 총체결수량
    # -TOT_CCLD_AMT	총체결금액	String	Y	19
    # -PRSM_TLEX_SMTL	추정제비용합계	String	Y	19	제세 + 주문수수료
    tot_ord_qty: int
    """총주문수량"""
    tot_ccld_qty: int
    """총체결수량"""
    pchs_avg_pric: float
    """매입평균가격"""
    tot_ccld_amt: int
    """총체결금액"""
    prsm_tlex_smtl: int
    """추정제비용합계"""

    orders: list[KisStockDailyOrder]
    """주문"""

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.orders = [KisStockDailyOrder(order) for order in data["output1"]]

    def __add__(self, other: "KisStockDailyOrders"):
        self.orders += other.orders
        return self
