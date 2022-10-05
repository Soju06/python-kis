from ._import import *

def revisable_order(
    self: 'KisAccountScope',
    order_by: INQR_ORDER_BY_TYPE = '주문순',
    where_by: BUY_CELL_DVSN_TYPE = '전체',
    page: KisPage = KisPage.first()
) -> 'KisStockRevisableOrders':
    '''정정가능 주문 조회 (가상계좌 불가)
    
    Args:
        order_by (INQR_ORDER_BY_TYPE, optional): 조회순서. Defaults to '주문순'.
        where_by (BUY_CELL_DVSN_TYPE, optional): 매도/매수 제약 조건. Defaults to '전체'.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
    '''
    if self.key.virtual_account:
        raise NotImplementedError('가상계좌는 주식 정정/취소 가능 조회 기능을 지원하지 않습니다.')

    if len(order_by) != 1:
        order_by = INQR_ORDER_BY[order_by]  # type: ignore
    
    if len(where_by) != 1:
        where_by = BUY_CELL_DVSN[where_by]  # type: ignore

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/trading/inquire-psbl-rvsecncl',
        headers={
            'tr_id': 'TTTC8036R'
        },
        params=self.account.build_body(page.build_body({
            'INQR_DVSN_1': order_by,
            'INQR_DVSN_2': where_by,
        })),
        response=KisStockRevisableOrders
    )

def revisable_orders(
    self: 'KisAccountScope',
    order_by: INQR_ORDER_BY_TYPE = '주문순',
    where_by: BUY_CELL_DVSN_TYPE = '전체',
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> Iterable['KisStockRevisableOrders']:
    '''정정가능 주문 조회 (가상계좌 불가)

    Args:
        order_by (INQR_ORDER_BY_TYPE, optional): 조회순서. Defaults to '주문순'.
        where_by (BUY_CELL_DVSN_TYPE, optional): 매도/매수 제약 조건. Defaults to '전체'.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 조회할 페이지 수. Defaults to None.
    '''
    return KisStockRevisableOrders.iterable(
        revisable_order,
        args=(self,),
        kwargs={
            'order_by': order_by, 
            'where_by': where_by
        },
        page=page, 
        count=count
    )

def revisable_order_all(
    self: 'KisAccountScope',
    order_by: INQR_ORDER_BY_TYPE = '주문순',
    where_by: BUY_CELL_DVSN_TYPE = '전체',
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> 'KisStockRevisableOrders':
    '''정정가능 주문 조회 (가상계좌 불가)

    Args:
        order_by (INQR_ORDER_BY_TYPE, optional): 조회순서. Defaults to '주문순'.
        where_by (BUY_CELL_DVSN_TYPE, optional): 매도/매수 제약 조건. Defaults to '전체'.
    '''
    return KisStockRevisableOrders.join(revisable_orders(
        self,
        order_by=order_by,
        where_by=where_by,
        page=page,
        count=count
    ))
