from ._import import *

def profit(
    self: 'KisAccountScope',
    overtime: bool = False,
    include_fund: bool = False,
    prcs: bool = True,
) -> 'KisRealizedProfit':
    '''계좌 실현손익 조회 (가상계좌 불가)

    Args:
        overtime (bool, optional): 시간외단일가여부. Defaults to False.
        include_fund (bool, optional): 펀드결제분포함여부. Defaults to False.
        prcs (bool, optional): 전일매매포함 여부. Defaults to True.
        page (KisPage, optional): 페이지. Defaults to KisPage.first().
    '''
    if self.key.virtual_account:
        raise NotImplementedError('가상계좌는 실현손익 조회 기능을 지원하지 않습니다.')

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/trading/inquire-balance-rlz-pl',
        headers={
            'tr_id': 'TTTC8494R'
        },
        params=self.account.build_body(KisPage.first().build_body({
            'AFHR_FLPR_YN': 'Y' if overtime else 'N',
            'OFL_YN': '',
            'INQR_DVSN': '00',
            'UNPR_DVSN': '01',
            'FUND_STTL_ICLD_YN': 'Y' if include_fund else 'N',
            'FNCG_AMT_AUTO_RDPT_YN': 'N',
            'PRCS_DVSN': '01' if prcs else '00',
            'COST_ICLD_YN': '',

        })),
        response=KisRealizedProfit
    )
