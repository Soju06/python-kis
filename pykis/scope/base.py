
from typing import TYPE_CHECKING

from ..rtclient import KisRTClient
from ..client import KisClient, KisKey
from ..logging import KisLoggable

if TYPE_CHECKING:
    from ..kis import PyKis

class KisScopeBase(KisLoggable):
    kis: 'PyKis'
    '''메인 클래스'''

    def __init__(self, kis: 'PyKis'):
        self.kis = kis
    
    @property
    def client(self) -> 'KisClient':
        '''API 클라이언트'''
        return self.kis.client

    @property
    def rtclient(self) -> 'KisRTClient':
        '''실시간 API 클라이언트'''
        return self.kis.rtclient

    @property
    def key(self) -> 'KisKey':
        '''API Key'''
        return self.kis.key