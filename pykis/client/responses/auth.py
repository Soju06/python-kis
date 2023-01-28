from datetime import datetime
import requests
import email.utils as eut
from .response import KisResponse
from ...timezone import tz_kst

class KisAccessTokenResponse(KisResponse):
    '''한국투자증권 API 접속 토큰 응답'''
    access_token: str
    '''접속 토큰'''
    token_type: str
    '''토큰 타입'''
    timestamp: datetime
    '''토큰 발급 시간'''
    expires_in: int
    '''토큰 만료 시간 (초)'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.timestamp = eut.parsedate_to_datetime(response.headers['Date']).astimezone(tz_kst)
        self.access_token = data['access_token']
        self.token_type = data['token_type']
        self.expires_in = data['expires_in']

class KisHashKeyResponse(KisResponse):
    '''한국투자증권 API 해시키 응답'''
    hash_key: str
    '''해시키'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.hash_key = data['HASH']

class KisWSApprovalKeyResponse(KisResponse):
    '''한국투자증권 API 웹소켓 접속키 응답'''
    approval_key: str
    '''접속 키'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)
        self.approval_key = data['approval_key']
