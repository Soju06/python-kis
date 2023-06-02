from .order_cash import KisStockOrderBase
from ...._import import *


INQR_ORDER_BY = {
    # 0 : 조회순서
    # 1 : 주문순
    # 2 : 종목순
    '기본': '0',
    '주문순': '1',
    '종목순': '2'
}

BUY_CELL_DVSN = {
    # 0 : 전체
    # 1 : 매도
    # 2 : 매수
    '전체': '0',
    '매도': '1',
    '매수': '2'
}

INQR_ORDER_BY_TYPE = Literal['기본', '주문순', '종목순', '0', '1', '2']
BUY_CELL_DVSN_TYPE = Literal['전체', '매도', '매수', '0', '1', '2']

# -ORD_GNO_BRNO	주문채번지점번호	String	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
# -ODNO	주문번호	String	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
# -ORGN_ODNO	원주문번호	String	Y	10	정정/취소주문 인경우 원주문번호
# -ORD_DVSN_NAME	주문구분명	String	Y	60
# -PDNO	상품번호	String	Y	12	종목번호(뒤 6자리만 해당)
# -PRDT_NAME	상품명	String	Y	60	종목명
# -RVSE_CNCL_DVSN_NAME	정정취소구분명	String	Y	60	정정 또는 취소 여부 표시
# -ORD_QTY	주문수량	String	Y	10	주문수량
# -ORD_UNPR	주문단가	String	Y	19	1주당 주문가격
# -ORD_TMD	주문시각	String	Y	6	주문시각(시분초HHMMSS)
# -TOT_CCLD_QTY	총체결수량	String	Y	10	주문 수량 중 체결된 수량
# -TOT_CCLD_AMT	총체결금액	String	Y	19	주문금액 중 체결금액
# -PSBL_QTY	가능수량	String	Y	10	정정/취소 주문 가능 수량
# -SLL_BUY_DVSN_CD	매도매수구분코드	String	Y	2	01 : 매도
# 02 : 매수
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
# 51 : 장중대량
# -MGCO_APTM_ODNO	운용사지정주문번호	String	Y	12	주문 번호 (운용사 통한 주문)

SLL_BUY_DVSN_CD_CODES = {
    '01': '매도',
    '02': '매수',
}

ORD_DVSN_CD_CODES = {
    '00': '지정가',
    '01': '시장가',
    '02': '조건부지정가',
    '03': '최유리지정가',
    '04': '최우선지정가',
    '05': '장전 시간외',
    '06': '장후 시간외',
    '07': '시간외 단일가',
    '08': '자기주식',
    '09': '자기주식S-Option',
    '10': '자기주식금전신탁',
    '11': 'IOC지정가 (즉시체결,잔량취소)',
    '12': 'FOK지정가 (즉시체결,전량취소)',
    '13': 'IOC시장가 (즉시체결,잔량취소)',
    '14': 'FOK시장가 (즉시체결,전량취소)',
    '15': 'IOC최유리 (즉시체결,잔량취소)',
    '16': 'FOK최유리 (즉시체결,전량취소)',
    '51': '장중대량',
}


class KisStockRevisableOrder(KisDynamic):
    ord_gno_brno: str
    '''주문채번지점번호'''
    odno: str
    '''주문번호'''
    orgn_odno: str
    '''원주문번호'''
    ord_dvsn_name: str
    '''주문구분명'''
    pdno: str
    '''상품번호'''
    prdt_name: str
    '''상품명'''
    rvse_cncl_dvsn_name: str
    '''정정취소구분명'''
    ord_qty: int
    '''주문수량'''
    ord_unpr: int
    '''주문단가'''
    ord_tmd: time
    '''주문시각'''
    tot_ccld_qty: int
    '''총체결수량'''
    tot_ccld_amt: int
    '''총체결금액'''
    psbl_qty: int
    '''가능수량'''
    sll_buy_dvsn_cd: Literal['01', '02']
    '''매도매수구분코드'''
    ord_dvsn_cd: Literal['00', '01', '02', '03', '04', '05', '06',
                         '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '51']
    '''주문구분코드'''
    mgco_aptm_odno: str
    '''운용사지정주문번호'''

    @property
    def sll_buy_dvsn_name(self) -> str:
        '''매도매수구분명'''
        return SLL_BUY_DVSN_CD_CODES[self.sll_buy_dvsn_cd]

    @property
    def ord_dvsn_cd_name(self) -> str:
        '''주문구분코드명'''
        return ORD_DVSN_CD_CODES[self.ord_dvsn_cd]

    @property
    def order(self) -> KisStockOrderBase:
        '''주문'''
        return KisStockOrderBase(self.ord_gno_brno, self.odno, self.ord_tmd)

    def __init__(self, data: dict):
        super().__init__(data)


class KisStockRevisableOrders(KisDynamicPagingAPIResponse):
    orders: list[KisStockRevisableOrder]
    '''주문정정취소가능주문목록'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.orders = [KisStockRevisableOrder(
            order) for order in data['output']]

    def __add__(self, other: 'KisStockRevisableOrders'):
        self.orders += other.orders
        return self
