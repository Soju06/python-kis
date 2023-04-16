from .order_cash import KisStockOrderBase
from ...._import import *

# -ord_dt	주문일자	String	Y	8	주문접수 일자
# -ord_gno_brno	주문채번지점번호	String	Y	5	계좌 개설 시 관리점으로 선택한 영업점의 고유번호
# -odno	주문번호	String	Y	10	접수한 주문의 일련번호
# -orgn_odno	원주문번호	String	Y	10	정정 또는 취소 대상 주문의 일련번호
# -pdno	상품번호	String	Y	12	종목코드
# -prdt_name	상품명	String	Y	60	종목명
# -sll_buy_dvsn_cd	매도매수구분코드	String	Y	2	01 : 매도
# 02 : 매수
# -sll_buy_dvsn_cd_name	매도매수구분코드명	String	Y	60	매수매도구분명
# -rvse_cncl_dvsn_cd	정정취소구분코드	String	Y	2	01 : 정정
# 02 : 취소
# -rvse_cncl_dvsn_cd_name	정정취소구분코드명	String	Y	60	정정취소구분명
# -rjct_rson	거부사유	String	Y	60	정상 처리되지 못하고 거부된 주문의 사유
# -rjct_rson_name	거부사유명	String	Y	60	정상 처리되지 못하고 거부된 주문의 사유명
# -ord_tmd	주문시각	String	Y	6	주문 접수 시간
# -tr_mket_name	거래시장명	String	Y	60
# -tr_crcy_cd	거래통화코드	String	Y	3	USD : 미국달러
# HKD : 홍콩달러
# CNY : 중국위안화
# JPY : 일본엔화
# VND : 베트남동
# -natn_cd	국가코드	String	Y	3
# -natn_kor_name	국가한글명	String	Y	60
# -ft_ord_qty	FT주문수량	String	Y	10	주문수량
# -ft_ccld_qty	FT체결수량	String	Y	10	체결된 수량
# -nccs_qty	미체결수량	String	Y	10	미체결수량
# -ft_ord_unpr3	FT주문단가3	String	Y	26	주문가격
# -ft_ccld_unpr3	FT체결단가3	String	Y	26	체결된 가격
# -ft_ccld_amt3	FT체결금액3	String	Y	23	체결된 금액
# -ovrs_excg_cd	해외거래소코드	String	Y	4	NASD : 나스닥
# NYSE : 뉴욕
# AMEX : 아멕스
# SEHK : 홍콩
# SHAA : 중국상해
# SZAA : 중국심천
# TKSE : 일본
# HASE : 베트남 하노이
# VNSE : 베트남 호치민
# -prcs_stat_name	처리상태명	String	Y	60
# -loan_type_cd	대출유형코드	String	Y	2	00 해당사항없음
# 01 자기융자일반형
# 03 자기융자투자형
# 05 유통융자일반형
# 06 유통융자투자형
# 07 자기대주
# 09 유통대주
# 11 주식담보대출
# 12 수익증권담보대출
# 13 ELS담보대출
# 14 채권담보대출
# 15 해외주식담보대출
# 16 기업신용공여
# 31 소액자동담보대출
# 41 매도담보대출
# 42 환매자금대출
# 43 매입환매자금대출
# 44 대여매도담보대출
# 81 대차거래
# 82 법인CMA론
# 91 공모주청약자금대출
# 92 매입자금
# 93 미수론서비스
# 94 대여
# -loan_dt	대출일자	String	Y	8	대출 실행일자

LOAN_TYPE_CD_CODES = {
    '00': '해당사항없음',
    '01': '자기융자일반형',
    '03': '자기융자투자형',
    '05': '유통융자일반형',
    '06': '유통융자투자형',
    '07': '자기대주',
    '09': '유통대주',
    '11': '주식담보대출',
    '12': '수익증권담보대출',
    '13': 'ELS담보대출',
    '14': '채권담보대출',
    '15': '해외주식담보대출',
    '16': '기업신용공여',
    '31': '소액자동담보대출',
    '41': '매도담보대출',
    '42': '환매자금대출',
    '43': '매입환매자금대출',
    '44': '대여매도담보대출',
    '81': '대차거래',
    '82': '법인CMA론',
    '91': '공모주청약자금대출',
    '92': '매입자금',
    '93': '미수론서비스',
    '94': '대여',
}


class KisOverseasStockRevisableOrder(KisDynamic):
    ord_dt: datetime
    '''주문일자'''
    ord_gno_brno: str
    '''주문채번지점번호'''
    odno: str
    '''주문번호'''
    orgn_odno: str
    '''원주문번호'''
    pdno: str
    '''상품번호'''
    prdt_name: str
    '''상품명'''
    sll_buy_dvsn_cd: Literal['01', '02']
    '''매도매수구분코드'''
    sll_buy_dvsn_cd_name: Literal['매도', '매수']
    '''매도매수구분코드명'''
    rvse_cncl_dvsn_cd: Literal['00', '01', '02']
    '''정정취소구분코드'''
    rvse_cncl_dvsn_cd_name: Literal['', '정정', '취소']
    '''정정취소구분코드명'''
    rjct_rson: str
    '''거부사유'''
    rjct_rson_name: str
    '''거부사유명'''
    ord_tmd: time
    '''주문시각'''
    tr_mket_name: str
    '''거래시장명'''
    tr_crcy_cd: Literal['USD', 'HKD', 'CNY', 'JPY', 'VND']
    natn_cd: str
    '''국가코드'''
    natn_kor_name: str
    '''국가한글명'''
    ft_ord_qty: int
    '''FT주문수량'''
    ft_ccld_qty: int
    '''FT체결수량'''
    nccs_qty: int
    '''미체결수량'''
    ft_ord_unpr3: float
    '''FT주문단가3'''
    ft_ccld_unpr3: float
    '''FT체결단가3'''
    ft_ccld_amt3: float
    '''FT체결금액3'''
    ovrs_excg_cd: Literal['NASD', 'NYSE', 'AMEX',
                          'SEHK', 'SHAA', 'SZAA', 'TKSE', 'HASE', 'VNSE']
    '''해외거래소코드'''
    prcs_stat_name: str
    '''처리상태명'''
    loan_type_cd: Literal[
        '00', '01', '03', '05', '06', '07', '09', '11', '12', '13',
        '14', '15', '16', '31', '41', '42', '43', '44', '81', '82',
        '91', '92', '93', '94'
    ]

    @property
    def order(self) -> KisStockOrderBase:
        '''주문'''
        return KisStockOrderBase(self.ord_gno_brno, self.odno, self.ord_tmd)

    @property
    def loan_type_cd_name(self) -> str:
        '''대출구분코드명'''
        return LOAN_TYPE_CD_CODES[self.loan_type_cd]

    @property
    def order_date(self) -> datetime:
        '''주문일시'''
        return datetime.combine(self.ord_dt, self.ord_tmd)


class KisOverseasStockRevisableOrders(KisDynamicLongPagingAPIResponse):
    orders: list[KisOverseasStockRevisableOrder]
    '''주문정정취소가능주문목록'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.orders = [KisOverseasStockRevisableOrder(
            order) for order in data['output']]

    def __add__(self, other: 'KisOverseasStockRevisableOrders'):
        self.orders += other.orders
        return self
