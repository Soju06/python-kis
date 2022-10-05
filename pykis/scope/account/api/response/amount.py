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
# 51 : 장중대량
# 52 : 장중바스켓
# 62 : 장개시전 시간외대량
# 63 : 장개시전 시간외바스켓
# 67 : 장개시전 금전신탁자사주
# 69 : 장개시전 자기주식
# 72 : 시간외대량
# 77 : 시간외자사주신탁
# 79 : 시간외대량자기주식
# 80 : 바스켓

from typing import Literal


A_ORD_DVSNS = {
    '00': '지정가',
    '01': '시장가',
    '02': '조건부지정가',
    '03': '최유리지정가',
    '04': '최우선지정가',
    '05': '장전시간외',
    '06': '장후시간외',
    '07': '시간외단일가',
    '08': '자기주식',
    '09': '자기주식S-Option',
    '10': '자기주식금전신탁',
    '11': 'IOC지정가',
    '12': 'FOK지정가',
    '13': 'IOC시장가',
    '14': 'FOK시장가',
    '15': 'IOC최유리',
    '16': 'FOK최유리',
    '51': '장중대량',
    '52': '장중바스켓',
    '62': '장개시전시간외대량',
    '63': '장개시전시간외바스켓',
    '67': '장개시전금전신탁자사주',
    '69': '장개시전자기주식',
    '72': '시간외대량',
    '77': '시간외자사주신탁',
    '79': '시간외대량자기주식',
    '80': '바스켓',
}

R_A_ORD_DVSNS = {v: k for k, v in A_ORD_DVSNS.items()}

A_ORD_DVSN_TYPE = Literal[
    '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14',
    '15', '16', '51', '52', '62', '63', '67', '69', '72', '77', '79', '80',
    '지정가', '시장가', '조건부지정가', '최유리지정가', '최우선지정가', '장전시간외', '장후시간외', '시간외단일가',
    '자기주식', '자기주식S-Option', '자기주식금전신탁', 'IOC지정가', 'FOK지정가', 'IOC시장가', 'FOK시장가',
    'IOC최유리', 'FOK최유리', '장중대량', '장중바스켓', '장개시전시간외대량', '장개시전시간외바스켓',
    '장개시전금전신탁자사주', '장개시전자기주식', '시간외대량', '시간외자사주신탁', '시간외대량자기주식', '바스켓',
]

# -ORD_PSBL_CASH	주문가능현금	String	Y	19	
# -ORD_PSBL_SBST	주문가능대용	String	Y	19	
# -RUSE_PSBL_AMT	재사용가능금액	String	Y	19	
# -FUND_RPCH_CHGS	펀드환매대금	String	Y	19	
# -PSBL_QTY_CALC_UNPR	가능수량계산단가	String	Y	19	
# -NRCVB_BUY_AMT	미수없는매수금액	String	Y	19	
# -NRCVB_BUY_QTY	미수없는매수수량	String	Y	10	
# -MAX_BUY_AMT	최대매수금액	String	Y	19	
# -MAX_BUY_QTY	최대매수수량	String	Y	10	
# -CMA_EVLU_AMT	CMA평가금액	String	Y	19	
# -OVRS_RE_USE_AMT_WCRC	해외재사용금액원화	String	Y	19	
# -ORD_PSBL_FRCR_AMT_WCRC	주문가능외화금액원화	String	Y	19	

class KisAccountAmount(KisDynamicAPIResponse):
    ord_psbl_cash: int
    '''주문가능현금'''
    ord_psbl_sbst: int
    '''주문가능대용'''
    ruse_psbl_amt: int
    '''재사용가능금액'''
    fund_rpch_chgs: int
    '''펀드환매대금'''
    psbl_qty_calc_unpr: int
    '''가능수량계산단가'''
    nrcvb_buy_amt: int
    '''미수없는매수금액'''
    nrcvb_buy_qty: int
    '''미수없는매수수량'''
    max_buy_amt: int
    '''최대매수금액'''
    max_buy_qty: int
    '''최대매수수량'''
    cma_evlu_amt: int
    '''CMA평가금액'''
    ovrs_re_use_amt_wcrc: int
    '''해외재사용금액원화'''
    ord_psbl_frcr_amt_wcrc: int
    '''주문가능외화금액원화'''
