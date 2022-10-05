from ._import import *

def amount(
    self: 'KisAccountScope',
    code: str | None,
    unpr: int = 0,
    dvsn: A_ORD_DVSN_TYPE = '지정가',
    include_cma: bool = True,
    include_overseas: bool = True,
) -> 'KisAccountAmount':
    '''주문 가능 금액 조회

    Args:
        code (str): 종목코드
        unpr (int, optional): 단가. Defaults to 0.
        dvsn (A_ORD_DVSN_TYPE, optional): 주문 구분. Defaults to '지정가'.
        include_cma (bool, optional): CMA 포함 여부. Defaults to True.
        include_overseas (bool, optional): 해외 포함 여부. Defaults to True.
    '''
    if len(dvsn) != 2:
        dvsn = R_A_ORD_DVSNS[dvsn]  # type: ignore

    return self.client.request(
        'get',
        '/uapi/domestic-stock/v1/trading/inquire-psbl-order',
        headers={
            'tr_id': 'VTTC8908R' if self.key.virtual_account else 'TTTC8908R'
        },
        params=self.account.build_body({
            'PDNO': code if code else '',
            'ORD_UNPR': unpr,
            'ORD_DVSN': dvsn,
            'CMA_EVLU_AMT_ICLD_YN': 'Y' if include_cma else 'N',
            'OVRS_ICLD_YN': 'Y' if include_overseas else 'N',
        }),
        response=KisAccountAmount
    )
