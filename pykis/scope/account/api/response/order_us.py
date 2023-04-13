from ...._import import *

# [Header tr_id JTTT1002U(미국 매수 주문)]
# 00 : 지정가
# 32 : LOO(장개시지정가)
# 34 : LOC(장마감지정가)
# * 모의투자 VTTT1002U(미국 매수 주문)로는 00:지정가만 가능

# [Header tr_id JTTT1006U(미국 매도 주문)]
# 00 : 지정가
# 31 : MOO(장개시시장가)
# 32 : LOO(장개시지정가)
# 33 : MOC(장마감시장가)
# 34 : LOC(장마감지정가)
# * 모의투자 VTTT1006U(미국 매도 주문)로는 00:지정가만 가능

US_ORD_DVSNS = {
    '00': '지정가',
    '31': '장개시시장가',
    '32': '장개시지정가',
    '33': '장마감시장가',
    '34': '장마감지정가'
}

US_R_ORD_DVSNS = {
    '지정가': '00',
    '장개시시장가': '31',
    '장개시지정가': '32',
    '장마감시장가': '33',
    '장마감지정가': '34'
}

US_ORD_DVSN_TYPE = Literal[
    '00', '31', '32', '33', '34',
    '지정가', '장개시시장가', '장개시지정가', '장마감시장가', '장마감지정가'
]

US_OVRS_EXCG_CD = Literal[
    'NASD', 'NYSE'
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

    def __init__(self, krx_fwdg_ord_orgno: str, odno: str):
        self.krx_fwdg_ord_orgno = krx_fwdg_ord_orgno
        self.odno = odno

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
