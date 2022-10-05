from ._import import *

TR_ID_CODES = [
# [실전투자]
# TTTC8001R : 주식 일별 주문 체결 조회(3개월이내)
# CTSC9115R : 주식 일별 주문 체결 조회(3개월이전)

# [모의투자]
# VTTC8001R : 주식 일별 주문 체결 조회(3개월이내)
# VTSC9115R : 주식 일별 주문 체결 조회(3개월이전)
# * 일별 조회로, 당일 주문내역은 지연될 수 있습니다.
    'TTTC8001R',
    'CTSC9115R',
    'VTTC8001R',
    'VTSC9115R'
]

def daily_order(
    self: 'KisAccountScope',
    start_date: datetime,
    end_date: datetime,
    order: KisStockOrderBase | None = None,
    code: str = '',
    dvsn: BUY_CELL_DVSN_TYPE = '전체',
    dvsn_1: INQR_DVSN_1_CODES_TYPE = '전체',
    dvsn_3: INQR_DVSN_3_CODES_TYPE = '전체',
    ccld: CCLD_TYPE = '전체',
    reversed: bool = False,
    old_order: bool = False,
    page: KisPage = KisPage.first()
) -> 'KisStockDailyOrders':
    '''일별 주문내역 조회

    Args:
        start_date (datetime): 시작일
        end_date (datetime): 종료일
        order (KisStockOrderBase, optional): 주문. Defaults to None.
        code (str, optional): 종목코드. Defaults to ''.
        dvsn (BUY_CELL_DVSN_TYPE, optional): 매수매도구분. Defaults to '전체'.
        dvsn_1 (INQR_DVSN_1_CODES_TYPE, optional): 조회구분1. Defaults to '전체'.
        dvsn_3 (INQR_DVSN_3_CODES_TYPE, optional): 조회구분3. Defaults to '전체'.
        ccld (CCLD_TYPE, optional): 체결구분. Defaults to '전체'.
        reversed (bool, optional): 역순. Defaults to False.
        old_order (bool, optional): 3개월 이전 주문내역. Defaults to False.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
    '''
    if code and len(code) != 6:
        raise ValueError('종목코드는 6자리입니다.')
    
    if len(dvsn) != 1:
        dvsn = BUY_CELL_DVSN[dvsn]  # type: ignore

    if ccld in CCLD_CODES:
        ccld = CCLD_CODES[ccld]  # type: ignore

    if len(dvsn_1) > 1:
        dvsn_1 = INQR_DVSN_1_CODES[dvsn_1]  # type: ignore

    if dvsn_3[0] != '0':
        dvsn_3 = INQR_DVSN_3_CODES[dvsn_3]  # type: ignore

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/trading/inquire-daily-ccld',
        headers={
            'tr_id': TR_ID_CODES[(2 if self.key.virtual_account else 0) + (1 if old_order else 0)]
        },
        params=self.account.build_body(page.build_body({
            'INQR_STRT_DT': start_date.strftime('%Y%m%d'),
            'INQR_END_DT': end_date.strftime('%Y%m%d'),
            'SLL_BUY_DVSN_CD': dvsn,
            'INQR_DVSN': '00' if reversed else '01',
            'PDNO': code,
            'CCLD_DVSN': ccld,
            'ORD_GNO_BRNO': order.krx_fwdg_ord_orgno if order else '',
            'ODNO': order.odno if order else '',
            'INQR_DVSN_3': dvsn_3,
            'INQR_DVSN_1': dvsn_1,
        })),
        response=KisStockDailyOrders
    )

def daily_orders(
    self: 'KisAccountScope',
    start_date: datetime,
    end_date: datetime,
    order: KisStockOrderBase | None = None,
    code: str = '',
    dvsn: BUY_CELL_DVSN_TYPE = '전체',
    dvsn_1: INQR_DVSN_1_CODES_TYPE = '전체',
    dvsn_3: INQR_DVSN_3_CODES_TYPE = '전체',
    ccld: CCLD_TYPE = '전체',
    reversed: bool = False,
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> Iterable['KisStockDailyOrders']:
    '''일별 주문내역 조회

    Args:
        start_date (datetime): 시작일
        end_date (datetime): 종료일
        order (KisStockOrderBase, optional): 주문. Defaults to None.
        code (str, optional): 종목코드. Defaults to ''.
        dvsn (BUY_CELL_DVSN_TYPE, optional): 매수매도구분. Defaults to '전체'.
        dvsn_1 (INQR_DVSN_1_CODES_TYPE, optional): 조회구분1. Defaults to '전체'.
        dvsn_3 (INQR_DVSN_3_CODES_TYPE, optional): 조회구분3. Defaults to '전체'.
        ccld (CCLD_TYPE, optional): 체결구분. Defaults to '전체'.
        reversed (bool, optional): 역순. Defaults to False.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 조회할 개수. Defaults to None.
    '''
    return KisStockDailyOrders.iterable(
        daily_order,
        args=(self,),
        kwargs={
            'start_date': start_date,
            'end_date': end_date,
            'order': order,
            'code': code,
            'dvsn': dvsn,
            'dvsn_1': dvsn_1,
            'dvsn_3': dvsn_3,
            'ccld': ccld,
            'reversed': reversed,
        },
        page=page, 
        count=count
    )

def daily_order_all(
    self: 'KisAccountScope',
    start_date: datetime,
    end_date: datetime,
    order: KisStockOrderBase | None = None,
    code: str = '',
    dvsn: BUY_CELL_DVSN_TYPE = '전체',
    dvsn_1: INQR_DVSN_1_CODES_TYPE = '전체',
    dvsn_3: INQR_DVSN_3_CODES_TYPE = '전체',
    ccld: CCLD_TYPE = '전체',
    reversed: bool = False,
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> 'KisStockDailyOrders':
    '''일별 주문내역 조회

    Args:
        start_date (datetime): 시작일
        end_date (datetime): 종료일
        order (KisStockOrderBase, optional): 주문. Defaults to None.
        code (str, optional): 종목코드. Defaults to ''.
        dvsn (BUY_CELL_DVSN_TYPE, optional): 매수매도구분. Defaults to '전체'.
        dvsn_1 (INQR_DVSN_1_CODES_TYPE, optional): 조회구분1. Defaults to '전체'.
        dvsn_3 (INQR_DVSN_3_CODES_TYPE, optional): 조회구분3. Defaults to '전체'.
        ccld (CCLD_TYPE, optional): 체결구분. Defaults to '전체'.
        reversed (bool, optional): 역순. Defaults to False.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 조회할 개수. Defaults to None.
    '''
    return KisStockDailyOrders.join(daily_orders(
        self,
        start_date=start_date,
        end_date=end_date,
        order=order,
        code=code,
        dvsn=dvsn,
        dvsn_1=dvsn_1,
        dvsn_3=dvsn_3,
        ccld=ccld,
        reversed=reversed,
        page=page,
        count=count
    ))
