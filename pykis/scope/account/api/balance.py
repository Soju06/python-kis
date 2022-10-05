from ._import import *

def balance(
    self: 'KisAccountScope',
    overtime: bool = False,
    include_fund: bool = False,
    prcs: bool = True,
    page: KisPage = KisPage.first()
) -> 'KisAccountBalance':
    '''계좌 잔고 조회

    Args:
        overtime (bool, optional): 시간외단일가여부. Defaults to False.
        include_fund (bool, optional): 펀드결제분포함여부. Defaults to False.
        prcs (bool, optional): 전일매매포함 여부. Defaults to True.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
    '''
    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/trading/inquire-balance',
        headers={
            'tr_id': 'VTTC8434R' if self.key.virtual_account else 'TTTC8434R'
        },
        params=self.account.build_body(page.build_body({
            'AFHR_FLPR_YN': 'Y' if overtime else 'N',
            'OFL_YN': '',
            'INQR_DVSN': '02',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'Y' if include_fund else 'N',
            'FNCG_AMT_AUTO_RDPT_YN' : 'N',
            'PRCS_DVSN': '00' if prcs else '01',
        })),
        response=KisAccountBalance
    )

def balances(
    self: 'KisAccountScope',
    overtime: bool = False,
    include_fund: bool = False,
    prcs: bool = True,
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> Iterable['KisAccountBalance']:
    '''계좌 잔고 조회

    Args:
        overtime (bool, optional): 시간외단일가여부. Defaults to False.
        include_fund (bool, optional): 펀드결제분포함여부. Defaults to False.
        prcs (bool, optional): 전일매매포함 여부. Defaults to True.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 페이지 개수. Defaults to None.
    '''
    return KisAccountBalance.iterable(
        balance,
        args=(self,),
        kwargs={
            'overtime': overtime,
            'include_fund': include_fund,
            'prcs': prcs,
        },
        page=page, 
        count=count
    )


def balance_all(
    self: 'KisAccountScope',
    overtime: bool = False,
    include_fund: bool = False,
    prcs: bool = True,
    page: KisPage = KisPage.first(),
    count: int | None = None
) -> 'KisAccountBalance':
    '''계좌 잔고 조회

    Args:
        overtime (bool, optional): 시간외단일가여부. Defaults to False.
        include_fund (bool, optional): 펀드결제분포함여부. Defaults to False.
        prcs (bool, optional): 전일매매포함 여부. Defaults to True.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
        count (int, optional): 페이지 개수. Defaults to None.
    '''
    return KisAccountBalance.join(balances(
        self,
        overtime=overtime,
        include_fund=include_fund,
        prcs=prcs,
        page=page,
        count=count
    ))
