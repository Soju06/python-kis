from ...._import import *

# 00 : 지정가
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

ORD_DVSNS = {
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
    '11': 'IOC지정가',
    '12': 'FOK지정가',
    '13': 'IOC시장가',
    '14': 'FOK시장가',
    '15': 'IOC최유리',
    '16': 'FOK최유리'
}

R_ORD_DVSNS = {
    '지정가': '00',
    '시장가': '01',
    '조건부지정가': '02',
    '최유리지정가': '03',
    '최우선지정가': '04',
    '장전 시간외': '05',
    '장후 시간외': '06',
    '시간외 단일가': '07',
    '자기주식': '08',
    '자기주식S-Option': '09',
    '자기주식금전신탁': '10',
    'IOC지정가': '11',
    'FOK지정가': '12',
    'IOC시장가': '13',
    'FOK시장가': '14',
    'IOC최유리': '15',
    'FOK최유리': '16'
}

ORD_DVSN_TYPE = Literal[
    '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
    '지정가', '시장가', '조건부지정가', '최유리지정가', '최우선지정가', '장전 시간외', '장후 시간외', '시간외 단일가',
    '자기주식', '자기주식S-Option', '자기주식금전신탁', 'IOC지정가', 'FOK지정가', 'IOC시장가', 'FOK시장가', 'IOC최유리', 'FOK최유리'
]

# -KRX_FWDG_ORD_ORGNO	한국거래소전송주문조직번호	String	Y	5	주문시 한국투자증권 시스템에서 지정된 영업점코드
# -ODNO	주문번호	String	Y	10	주문시 한국투자증권 시스템에서 채번된 주문번호
# -ORD_TMD	주문시각	String	Y	6	주문시각(시분초HHMMSS)


class KisStockOrderBase:
    '''주식 주문'''
    krx_fwdg_ord_orgno: str
    '''한국거래소전송주문조직번호'''
    odno: str
    '''주문번호'''
    ord_tmd: time | None
    '''주문시각'''

    def __init__(self, krx_fwdg_ord_orgno: str, odno: str, ord_tmd: time | None = None):
        self.krx_fwdg_ord_orgno = krx_fwdg_ord_orgno
        self.odno = odno
        self.ord_tmd = ord_tmd


class KisStockOrder(KisDynamicAPIResponse, KisStockOrderBase):
    '''주식 주문'''
    krx_fwdg_ord_orgno: str
    '''한국거래소전송주문조직번호'''
    odno: str
    '''주문번호'''
    ord_tmd: time
    '''주문시각'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
