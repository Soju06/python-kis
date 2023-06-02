from ...._import import *

# -PDNO	상품번호	String	Y	12	종목번호(뒷 6자리)
# -PRDT_NAME	상품명	String	Y	60	종목명
# -TRAD_DVSN_NAME	매매구분명	String	Y	60	매수매도구분
# -BFDY_BUY_QTY	전일매수수량	String	Y	10	
# -BFDY_SLL_QTY	전일매도수량	String	Y	10	
# -THDT_BUYQTY	금일매수수량	String	Y	10	
# -THDT_SLL_QTY	금일매도수량	String	Y	10	
# -HLDG_QTY	보유수량	String	Y	19	
# -ORD_PSBL_QTY	주문가능수량	String	Y	10	
# -PCHS_AVG_PRIC	매입평균가격	String	Y	22	매입금액 / 보유수량
# -PCHS_AMT	매입금액	String	Y	19	
# -PRPR	현재가	String	Y	19	
# -EVLU_AMT	평가금액	String	Y	19	
# -EVLU_PFLS_AMT	평가손익금액	String	Y	19	평가금액 - 매입금액
# -EVLU_PFLS_RT	평가손익율	String	Y	9	
# -EVLU_ERNG_RT	평가수익율	String	Y	31	
# -LOAN_DT	대출일자	String	Y	8	
# -LOAN_AMT	대출금액	String	Y	19	
# -STLN_SLNG_CHGS	대주매각대금	String	Y	19	
# -EXPD_DT	만기일자	String	Y	8	
# -FLTT_RT	등락율	String	Y	31	
# -BFDY_CPRS_ICDC	전일대비증감	String	Y	19	
# -ITEM_MGNA_RT_NAME	종목증거금율명	String	Y	20	
# -GRTA_RT_NAME	보증금율명	String	Y	20	
# -SBST_PRIC	대용가격	String	Y	19	증권매매의 위탁보증금으로서 현금 대신에 사용되는 유가증권 가격
# -STCK_LOAN_UNPR	주식대출단가	String	Y	22	

class KisAccountBalanceStock(KisDynamic):
    '''잔고 종목'''
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
    fltt_rt: float
    '''등락율'''
    bfdy_cprs_icdc: int
    '''전일대비증감'''
    item_mgna_rt_name: str
    '''종목증거금율명'''
    grta_rt_name: str
    '''보즘금율명'''
    sbst_pric: int
    '''대용가격'''
    stck_loan_unpr: float
    '''주식대출단가'''
    
    
# -DNCA_TOT_AMT	예수금총금액	String	Y	19	
# -NXDY_EXCC_AMT	익일정산금액	String	Y	19	
# -PRVS_RCDL_EXCC_AMT	가수도정산금액	String	Y	19	
# -CMA_EVLU_AMT	CMA평가금액	String	Y	19	
# -BFDY_BUY_AMT	전일매수금액	String	Y	19	
# -THDT_BUY_AMT	금일매수금액	String	Y	19	
# -NXDY_AUTO_RDPT_AMT	익일자동상환금액	String	Y	19	
# -BFDY_SLL_AMT	전일매도금액	String	Y	19	
# -THDT_SLL_AMT	금일매도금액	String	Y	19	
# -D2_AUTO_RDPT_AMT	D+2자동상환금액	String	Y	19	
# -BFDY_TLEX_AMT	전일제비용금액	String	Y	19	
# -THDT_TLEX_AMT	금일제비용금액	String	Y	19	
# -TOT_LOAN_AMT	총대출금액	String	Y	19	
# -SCTS_EVLU_AMT	유가평가금액	String	Y	19	
# -TOT_EVLU_AMT	총평가금액	String	Y	19	
# -NASS_AMT	순자산금액	String	Y	19	
# -FNCG_GLD_AUTO_RDPT_YN	융자금자동상환여부	String	Y	1	보유현금에 대한 융자금만 차감여부
# 신용융자 매수체결 시점에서는 융자비율을 매매대금 100%로 계산 하였다가 수도결제일에 보증금에 해당하는 금액을 고객의 현금으로 충당하여 융자금을 감소시키는 업무
# -PCHS_AMT_SMTL_AMT	매입금액합계금액	String	Y	19	
# -EVLU_AMT_SMTL_AMT	평가금액합계금액	String	Y	19	
# -EVLU_PFLS_SMTL_AMT	평가손익합계금액	String	Y	19	
# -TOT_STLN_SLNG_CHGS	총대주매각대금	String	Y	19	
# -BFDY_TOT_ASST_EVLU_AMT	전일총자산평가금액	String	Y	19	
# -ASST_ICDC_AMT	자산증감액	String	Y	19	


class KisAccountBalance(KisDynamicPagingAPIResponse):
    '''계좌잔고조회'''
    stocks: list[KisAccountBalanceStock]
    '''잔고 종목'''
    
    dnca_tot_amt: int
    '''예수금총금액'''
    nxdy_excc_amt: int
    '''익일정산금액'''
    prvs_rcdl_excc_amt: int
    '''가수도정산금액'''
    cma_evlu_amt: int
    '''CMA평가금액'''
    bfdy_buy_amt: int
    '''전일매수금액'''
    thdt_buy_amt: int
    '''금일매수금액'''
    nxdy_auto_rdpt_amt: int
    '''익일자동상환금액'''
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

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.stocks = [KisAccountBalanceStock(stock) for stock in data['output1']]
        self._parseDict(data['output2'][0])

    def __add__(self, other: 'KisAccountBalance'):
        self.stocks += other.stocks
        return self
    