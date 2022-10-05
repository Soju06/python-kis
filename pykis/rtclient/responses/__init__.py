from typing import Any, Literal

from .rt_asking_price import KisRTAskingPrice
from .rt_price import KisRTPrice
from .rt_conclude import KisRTConclude

RT_RESPONSES: dict[str, Any] = {
    'H0STCNT0': KisRTPrice,
    'H0STASP0': KisRTAskingPrice,
    'H0STCNI0': KisRTConclude,
    'H0STCNI9': KisRTConclude,
}

RT_CODE_MAP: dict[str, str | tuple[str, str]] = {
    '체결가': 'H0STCNT0',
    '호가': 'H0STASP0',
    '체결': ('H0STCNI0', 'H0STCNI9')
}

RT_RESPONSE_TYPE = KisRTPrice | KisRTAskingPrice
RT_CODE_TYPE = Literal['체결가', '호가', '체결']

def _rtcd(id: str, va: bool) -> str:
    tr_id = RT_CODE_MAP.get(id, None)
    
    if not tr_id:
        raise KeyError(f'RTC unknown item code: {id}')
    
    if isinstance(tr_id, tuple):
        tr_id = tr_id[1 if va else 0]
    
    return tr_id
    