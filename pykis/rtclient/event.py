
from typing import TYPE_CHECKING, Any, Callable

from .responses import RT_CODE_TYPE, RT_RESPONSES, RT_RESPONSE_TYPE, _rtcd

if TYPE_CHECKING:
    from .rtclient import KisRTClient

RT_EVENT_FUNCTION = Callable[['KisRTClient', Any], Any]


class KisRTEventScope:
    '''한국투자증권 실시간 이벤트 범위 리스너'''
    tr_id: str | None
    '''TR ID. None일 경우 전체 TR에 대한 이벤트'''
    listeners: list[RT_EVENT_FUNCTION]
    '''범위 리스너'''

    def __init__(self, event: 'KisRTEvent', tr_id: str | None):
        self.listeners = event._scope_list(tr_id)
        
    def __add__(self, listener: RT_EVENT_FUNCTION):
        self.listeners.append(listener)
        return self

    def __sub__(self, listener: RT_EVENT_FUNCTION):
        self.listeners.remove(listener)
        return self

    def add(self, listener: RT_EVENT_FUNCTION):
        '''리스너 추가
        
        Args:
            listener (RT_EVENT_FUNCTION): 리스너

        Examples:
            체결가 이벤트 리스너 추가
            >>> def on_cntg(cli: KisRTClient, res: KisRTPrice):
            ...     print(res)
            ... kis.rtclient.event.cntg.add(on_cntg)
            호가 이벤트 리스너 추가
            >>> def on_rsqn(cli: KisRTClient, res: KisRTAskingPrice):
            ...     print(res)
            ... kis.rtclient.event.rsqn.add(on_rsqn)
            체결 이벤트 리스너 추가
            >>> def on_oder(cli: KisRTClient, res: KisRTConclude):
            ...     print(res)
            ... kis.rtclient.event.oder.add(on_oder)
        '''
        self.listeners.append(listener)

    def remove(self, listener: RT_EVENT_FUNCTION):
        self.listeners.remove(listener)

    def remove_all(self):
        self.listeners.clear()


class KisRTEvent:
    '''한국투자증권 실시간 이벤트'''
    listeners: dict[str | None, list[RT_EVENT_FUNCTION]]
    '''리스너'''
    client: 'KisRTClient'
    '''한국투자증권 실시간 클라이언트'''
    
    def __init__(self, client: 'KisRTClient') -> None:
        self.listeners = {}
        self.client = client

    def _scope_list(self, tr_id: str | None) -> list[RT_EVENT_FUNCTION]:
        if tr_id is not None and tr_id not in RT_RESPONSES:
            raise KeyError(f'Invalid TR_ID: {tr_id}')
        if tr_id not in self.listeners:
            self.listeners[tr_id] = l = []
        else: l = self.listeners[tr_id]
        return l

    def scope(self, id: RT_CODE_TYPE) -> KisRTEventScope:
        '''특정 TR_ID에 대한 이벤트 리스너를 반환합니다.'''
        return KisRTEventScope(self, _rtcd(id, self.client.key.virtual_account))

    @property
    def cntg(self) -> KisRTEventScope:
        '''체결가 이벤트 리스너를 반환합니다.'''
        return self.scope('체결가')
    
    @property
    def rsqn(self) -> KisRTEventScope:
        '''호가 이벤트 리스너를 반환합니다.'''
        return self.scope('호가')
    
    @property
    def oder(self) -> KisRTEventScope:
        '''주문 체결 이벤트 리스너를 반환합니다.'''
        return self.scope('체결')


    def __add__(self, listener: RT_EVENT_FUNCTION):
        self._scope_list(None).append(listener)
        return self

    def __sub__(self, listener: RT_EVENT_FUNCTION):
        self._scope_list(None).remove(listener)
        return self


    def _emit(self, rt: RT_RESPONSE_TYPE):
        listeners = self.listeners.get(rt.tr_id, None)
        
        if listeners:
            for listener in listeners:
                listener(self.client, rt)

        listeners = self.listeners.get(None, None)

        if listeners:
            for listener in self.listeners[None]:
                listener(self.client, rt)
