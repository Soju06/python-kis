
from datetime import datetime, time
from typing import Literal


from ..messaging import KisRTResponse

# CUST_ID	고객 ID	String	Y	8	
# ACNT_NO	계좌번호	String	Y	10	
# ODER_NO	주문번호	String	Y	10	
# OODER_NO	원주문번호	String	Y	10	
# SELN_BYOV_CLS	매도매수구분	String	Y	2	01 : 매도
# 02 : 매수
# RCTF_CLS	정정구분	String	Y	1	
# ODER_KIND	주문종류	String	Y	2	00 : 지정가
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
# ODER_COND	주문조건	String	Y	1	
# STCK_SHRN_ISCD	주식 단축 종목코드	String	Y	9	
# CNTG_QTY	체결 수량	String	Y	10	
# CNTG_UNPR	체결단가	String	Y	9	
# STCK_CNTG_HOUR	주식 체결 시간	String	Y	6	
# RFUS_YN	거부여부	String	Y	1	0 : 승인
# 1 : 거부
# CNTG_YN	체결여부	String	Y	1	1 : 주문,정정,취소,거부,
# 2 : 체결 (★ 체결만 보실경우 2번만 보시면 됩니다)
# ACPT_YN	접수여부	String	Y	1	1 : 주문접수
# 2 : 확인
# 3:취소(FOK/IOC)
# BRNC_NO	지점번호	String	Y	5	
# ODER_QTY	주문수량	String	Y	9	
# ACNT_NAME	계좌명	String	Y	12	
# CNTG_ISNM	체결종목명	String	Y	14	
# CRDT_CLS	신용구분	String	Y	2	
# CRDT_LOAN_DATE	신용대출일자	String	Y	8	
# CNTG_ISNM40	체결종목명40	String	Y	40	
# ODER_PRC	주문가격	String	Y	9	

SELN_BYOV_CLS_CODES = {
    "01": "매도",
    "02": "매수",
}

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

RFUS_YN_CODES = {
    "0": "승인",
    "1": "거부",
}

CNTG_YN_CODES = {
    "1": "주문",
    "2": "체결",
}

ACPT_YN_CODES = {
    "1": "주문접수",
    "2": "확인",
    "3": "취소(FOK/IOC)",
}

class KisRTConclude(KisRTResponse):
    '''주식 체결'''
    cust_id: str
    '''고객 ID'''
    acnt_no: str
    '''계좌번호'''
    oder_no: str
    '''주문번호'''
    ooder_no: str
    '''원주문번호'''
    seln_byov_cls: Literal['01', '02']
    '''매도매수구분'''
    rctf_cls: str
    '''정정구분'''
    oder_kind: Literal['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']
    '''주문종류'''
    oder_cond: str
    '''주문조건'''
    stck_shrn_iscd: str
    '''주식 단축 종목코드'''
    cntg_qty: int
    '''체결 수량'''
    cntg_unpr: int
    '''체결단가'''
    stck_cntg_hour: time
    '''주식 체결 시간'''
    rfus_yn: Literal['0', '1']
    '''거부여부'''
    cntg_yn: Literal['1', '2']
    '''체결여부'''
    acpt_yn: Literal['1', '2', '3']
    '''접수여부'''
    brnc_no: str
    '''지점번호'''
    oder_qty: int
    '''주문수량'''
    acnt_name: str
    '''계좌명'''
    cntg_isnm: str
    '''체결종목명'''
    crdt_cls: str
    '''신용구분'''
    crdt_loan_date: datetime | None
    '''신용대출일자'''
    cntg_isnm40: str
    '''체결종목명40'''
    oder_prc: int | None
    '''주문가격'''

    @property
    def seln_byov_cls_name(self) -> str:
        return SELN_BYOV_CLS_CODES[self.seln_byov_cls]

    @property
    def order_kind_name(self) -> str:
        return ORD_DVSNS[self.oder_kind]

    @property
    def rfus_yn_name(self) -> str:
        return RFUS_YN_CODES[self.rfus_yn]

    @property
    def cntg_yn_name(self) -> str:
        return CNTG_YN_CODES[self.cntg_yn]
    
    @property
    def acpt_yn_name(self) -> str:
        return ACPT_YN_CODES[self.acpt_yn]

    @property
    def cntg(self) -> bool:
        '''체결여부'''
        return self.cntg_yn == '2'

