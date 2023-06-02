from ...._import import *

# rt_cd	성공 실패 여부	String	Y	1	
# msg_cd	응답코드	String	Y	8	
# msg1	응답메세지	String	Y	80	
# Output1	응답상세	Object Array			Array
# -pdno	상품번호	String		12	종목번호(뒷 6자리)
# -prdt_name	상품명	String		60	종목명
# -trad_dvsn_name	매매구분명	String		60	매수매도구분
# -bfdy_buy_qty	전일매수수량	String		10	
# -bfdy_sll_qty	전일매도수량	String		10	
# -thdt_buyqty	금일매수수량	String		10	
# -thdt_sll_qty	금일매도수량	String		10	
# -hldg_qty	보유수량	String		19	
# -ord_psbl_qty	주문가능수량	String		10	
# -pchs_avg_pric	매입평균가격	String		23	매입금액 / 보유수량
# -pchs_amt	매입금액	String		19	
# -prpr	현재가	String		19	
# -evlu_amt	평가금액	String		19	
# -evlu_pfls_amt	평가손익금액	String		19	평가금액 - 매입금액
# -evlu_pfls_rt	평가손익율	String		10	
# -evlu_erng_rt	평가수익율	String		32	
# -loan_dt	대출일자	String		8	
# -loan_amt	대출금액	String		19	
# -stln_slng_chgs	대주매각대금	String		19	신용 거래에서, 고객이 증권 회사로부터 대부받은 주식의 매각 대금
# -expd_dt	만기일자	String		8	
# -stck_loan_unpr	주식대출단가	String		23	
# -bfdy_cprs_icdc	전일대비증감	String		19	
# -fltt_rt	등락율	String		32	
# Output2	응답상세2	Object			
# -dnca_tot_amt	예수금총금액	String		19	
# -nxdy_excc_amt	익일정산금액	String		19	
# -prvs_rcdl_excc_amt	가수도정산금액	String		19	
# -cma_evlu_amt	CMA평가금액	String		19	
# -bfdy_buy_amt	전일매수금액	String		19	
# -thdt_buy_amt	금일매수금액	String		19	
# -nxdy_auto_rdpt_amt	익일자동상환금액	String		19	
# -bfdy_sll_amt	전일매도금액	String		19	
# -thdt_sll_amt	금일매도금액	String		19	
# -d2_auto_rdpt_amt	D+2자동상환금액	String		19	
# -bfdy_tlex_amt	전일제비용금액	String		19	
# -thdt_tlex_amt	금일제비용금액	String		19	
# -tot_loan_amt	총대출금액	String		19	
# -scts_evlu_amt	유가평가금액	String		19	
# -tot_evlu_amt	총평가금액	String		19	
# -nass_amt	순자산금액	String		19	
# -fncg_gld_auto_rdpt_yn	융자금자동상환여부	String		1	
# -pchs_amt_smtl_amt	매입금액합계금액	String		19	
# -evlu_amt_smtl_amt	평가금액합계금액	String		19	
# -evlu_pfls_smtl_amt	평가손익합계금액	String		19	
# -tot_stln_slng_chgs	총대주매각대금	String		19	
# -bfdy_tot_asst_evlu_amt	전일총자산평가금액	String		19	
# -asst_icdc_amt	자산증감액	String		19	
# -asst_icdc_erng_rt	자산증감수익율	String		32	
# -rlzt_pfls	실현손익	String		19	
# -rlzt_erng_rt	실현수익율	String		32	
# -real_evlu_pfls	실평가손익	String		19	
# -real_evlu_pfls_erng_rt	실평가손익수익율	String		32	

class KisRealizedProfitStock(KisDynamic):
    pdno: str
    '''상품번호'''
    prdt_name: str
    '''상품명'''
    trad_dvsn_name: str
    '''매매구분명'''
    bfdy_buy_qty: int
    '''전일매수수량'''
    bfdy_sll_qty: int
    '''전일매도수량'''
    thdt_buyqty: int
    '''금일매수수량'''
    thdt_sll_qty: int
    '''금일매도수량'''
    hldg_qty: int
    '''보유수량'''
    ord_psbl_qty: int
    '''주문가능수량'''
    pchs_avg_pric: float
    '''매입평균가격'''
    pchs_amt: int
    '''매입금액'''
    prpr: int
    '''현재가'''
    evlu_amt: int
    '''평가금액'''
    evlu_pfls_amt: int
    '''평가손익금액'''
    evlu_pfls_rt: float
    '''평가손익율'''
    evlu_erng_rt: float
    '''평가수익율'''
    loan_dt: datetime | None
    '''대출일자'''
    loan_amt: int
    '''대출금액'''
    stln_slng_chgs: int
    '''대주매각대금'''
    expd_dt: datetime | None
    '''만기일자'''
    stck_loan_unpr: float
    '''주식대출단가'''
    bfdy_cprs_icdc: int
    '''전일대비증감'''
    fltt_rt: float
    '''등락율'''


class KisRealizedProfit(KisDynamicAPIResponse):
    '''실현손익'''
    stocks: list[KisRealizedProfitStock]
    '''잔고 종목'''
    
    bfdy_sll_amt: int
    '''전일매도금액'''
    thdt_sll_amt: int
    '''금일매도금액'''
    d2_auto_rdpt_amt: int
    '''D+2자동상환금액'''
    bfdy_tlex_amt: int
    '''전일제비용금액'''
    thdt_tlex_amt: int
    '''금일제비용금액'''
    tot_loan_amt: int
    '''총대출금액'''
    scts_evlu_amt: int
    '''유가평가금액'''
    tot_evlu_amt: int
    '''총평가금액'''
    nass_amt: int
    '''순자산금액'''
    fncg_gld_auto_rdpt_yn: bool
    '''융자금자동상환여부'''
    pchs_amt_smtl_amt: int
    '''매입금액합계금액'''
    evlu_amt_smtl_amt: int
    '''평가금액합계금액'''
    evlu_pfls_smtl_amt: int
    '''평가손익합계금액'''
    tot_stln_slng_chgs: int
    '''총대주매각대금'''
    bfdy_tot_asst_evlu_amt: int
    '''전일총자산평가금액'''
    asst_icdc_amt: int
    '''자산증감액'''
    asst_icdc_erng_rt: float
    '''자산증감수익율'''
    rlzt_pfls: int
    '''실현손익'''
    rlzt_erng_rt: float
    '''실현수익율'''
    real_evlu_pfls: int
    '''실평가손익'''
    real_evlu_pfls_erng_rt: float
    '''실평가손익수익율'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.stocks = [KisRealizedProfitStock(stock) for stock in data['output1']]
        self._parseDict(data['output2'][0])
