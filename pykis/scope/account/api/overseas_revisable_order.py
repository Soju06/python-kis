from ._import import *

# [실전투자]
# JTTT3018R : PSBL_YN(주야간 원장 구분) = 'Y' (야간용)
# TTTS3018R : PSBL_YN(주야간 원장 구분) = 'N' (주간용)

# [모의투자]
# VTTS3018R : PSBL_YN(주야간 원장 구분) = 'Y' (야간용)
# VTTS3018R : PSBL_YN(주야간 원장 구분) = 'N' (주간용)

TR_ID_CODES: list[tuple[str, str]] = [
    # [실전투자]
    ('JTTT3018R', 'TTTS3018R'),
    # [모의투자]
    ('VTTS3018R', 'VTTS3018R'),
]


def overseas_revisable_order(
    self: 'KisAccountScope',
    market: OVERSEAS_OVRS_EXCG_CD,
    psbl: bool = False,
    reverse: bool = False,
    page: KisLongPage = KisLongPage.first()
) -> 'KisOverseasStockRevisableOrders':
    '''해외 미체결 주문 조회 (가상계좌 불가)

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        psbl (bool): 야간 주문 여부
        reverse (bool): 정렬 순서
    '''
    if market not in OVERSEAS_OVRS_EXCGS:
        market = OVERSEAS_R_OVRS_EXCGS.get(market, None)  # type: ignore
        if market is None:
            raise ValueError(
                f'해외 시장 구분은 ({", ".join(f"{k}, {v}" for k, v in OVERSEAS_R_OVRS_EXCGS.items())}) 중 하나여야 합니다.')

    return self.client.request(
        'get',
        '/uapi/overseas-stock/v1/trading/inquire-nccs',
        headers={
            'tr_id': TR_ID_CODES[1 if self.key.virtual_account else 0][1 if psbl else 0],
        },
        params=self.account.build_body(page.build_body({
            'OVRS_EXCG_CD': market,
            'SORT_SQN': '' if reverse else 'DS',
        })),
        response=KisOverseasStockRevisableOrders
    )


def overseas_revisable_orders(
    self: 'KisAccountScope',
    market: OVERSEAS_OVRS_EXCG_CD,
    psbl: bool = False,
    reverse: bool = False,
    page: KisLongPage = KisLongPage.first(),
    count: int | None = None
) -> Iterable['KisOverseasStockRevisableOrders']:
    '''정정가능 주문 조회 (가상계좌 불가)

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        psbl (bool): 야간 주문 여부
        reverse (bool): 정렬 순서
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 조회할 페이지 수. Defaults to None.
    '''
    return KisOverseasStockRevisableOrders.iterable(
        overseas_revisable_order,
        args=(self,),
        kwargs={
            'market': market,
            'psbl': psbl,
            'reverse': reverse,
        },
        page=page,
        count=count
    )


def overseas_revisable_order_all(
    self: 'KisAccountScope',
    market: OVERSEAS_OVRS_EXCG_CD,
    psbl: bool = False,
    reverse: bool = False,
    page: KisLongPage = KisLongPage.first(),
    count: int | None = None
) -> 'KisOverseasStockRevisableOrders':
    '''정정가능 주문 조회 (가상계좌 불가)

    Args:
        market (US_OVRS_EXCG_CD): 해외 시장 구분
        psbl (bool): 야간 주문 여부
        reverse (bool): 정렬 순서
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 조회할 페이지 수. Defaults to None.
    '''
    return KisOverseasStockRevisableOrders.join(overseas_revisable_orders(
        self,
        market=market,
        psbl=psbl,
        reverse=reverse,
        page=page,
        count=count
    ))
