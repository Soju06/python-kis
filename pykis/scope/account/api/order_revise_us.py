from ._import import *

def order_revise_us(
    self: 'KisAccountScope',
    order: KisStockOrderBase,
    type: Literal['01', '02', '정정', '취소'],
    qty: int | None,
    unpr: int,
    dvsn: US_ORD_DVSN_TYPE = '지정가',
    market: US_OVRS_EXCG_CD = 'NASD'    
) -> 'KisStockOrder':
    '''주식 주문 정정/취소

    Args:
        order (KisStockOrder): 정정할 주식 주문
        type (Literal['01', '02', '취소', '정정']): 정정/취소 구분
        qty (int | None): 주문 수량 (None일 경우 전량 정정)
        unpr (int, optional): 주문 단가. 주문 취소시 0
        dvsn (US_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'
        market (US_OVRS_EXCG_CD, optional): 시장 구분. Defaults to 'NASD'.

    Returns:
        KisStockOrder: 주식 주문 응답
    '''
    # TODO: 전량 정정 테스트 필요
    if len(dvsn) != 2:
        dvsn = US_R_ORD_DVSNS[dvsn]  # type: ignore

    if type[0] != '0':
        type = '01' if type == '정정' else '02'
    
    return self.client.request(
        'post',
        '/uapi/overseas-stock/v1/trading/order-rvsecncl',
        headers={
            'tr_id': 'VTTT1004U' if self.key.virtual_account else 'JTTT1004U'
        },
        body=self.account.build_body({
            'KRX_FWDG_ORD_ORGNO': order.krx_fwdg_ord_orgno,
            'ORGN_ODNO': order.odno,
            'ORD_DVSN': dvsn,
            'RVSE_CNCL_DVSN_CD': type,
            'ORD_QTY': '0' if qty is None else qty,
            'ORD_UNPR': unpr,
            'QTY_ALL_ORD_YN': 'Y' if qty is None else 'N',
            'OVRS_EXCG_CD': market,
        }),
        response=KisStockOrder
    )


def cancel_us(
    self: 'KisAccountScope',
    order: KisStockOrderBase,
    qty: int | None = None
) -> 'KisStockOrder':
    '''주식 주문 취소

    Args:
        order (KisStockOrder): 취소할 주식 주문
        qty (int | None, optional): 주문 수량 (None일 경우 전량 취소). Defaults to None.

    Returns:
        KisStockOrder: 주식 주문 응답
    '''
    return self.order_revise_us(order, '취소', qty, 0)


def revise_us(
    self: 'KisAccountScope',
    order: KisStockOrderBase,
    qty: int | None,
    unpr: int,
    dvsn: ORD_DVSN_TYPE = '지정가',
) -> 'KisStockOrder':
    '''주식 주문 정정

    Args:
        order (KisStockOrder): 정정할 주식 주문
        qty (int | None): 주문 수량 (None일 경우 전량 정정)
        unpr (int): 주문 단가
        dvsn (ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.

    Returns:
        KisStockOrder: 주식 주문 응답
    '''
    return self.order_revise_us(order, '정정', qty, unpr, dvsn)
