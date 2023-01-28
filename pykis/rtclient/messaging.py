from datetime import datetime, time
import types
from typing import get_args

from .encrypt import KisRTEncrypt

class KisRTRequest:
    '''한국투자증권 실시간 요청'''
    approval_key: str
    tr_id: str
    tr_key: str
    tr_type: bool
    '''등록 여부'''

    def __init__(self, approval_key: str, tr_id: str, tr_key: str, tr_type: bool = True):
        self.approval_key = approval_key
        self.tr_id = tr_id
        self.tr_key = tr_key
        self.tr_type = tr_type
    
    def dict(self):
        return {
            'header': {
                'authoriztion': '',
                # 보안강화 대응.
                # 'appkey': self.key.appkey,
                # 'appsecret': self.key.appsecret,
                'approval_key': self.approval_key,
                'tr_type': '1' if self.tr_type else '2',
                'custtype': 'P',
                'content-type': 'utf-8',
            },
            'body': {
                'input': {
                    'tr_id': self.tr_id,
                    'tr_key': self.tr_key,
                }
            }
        }


class KisRTSysResponse:
    '''한국투자증권 시스템 응답'''
    
    tr_id: str
    tr_key: str | None = None
    encrypt: bool
    rt_cd: str | None = None
    msg_cd: str | None = None
    msg1: str | None = None
    iv: str | None = None
    key: str | None = None

    def __init__(self, data: dict):
        body = data.get('body', None)
        header = data['header']

        self.tr_id = header['tr_id']
        self.tr_key = header.get('tr_key', None)
        self.encrypt = header.get('encrypt', None) == 'Y'

        if body:
            self.msg1 = body['msg1']
            self.msg_cd = body['msg_cd']
            self.rt_cd = body['rt_cd']

            if 'output' in body:
                output = body['output']
                self.iv = output['iv']
                self.key = output['key']


class KisRTResponse:
    '''한국투자증권 실시간 응답'''
    encrypt: bool
    '''암호화 여부'''
    tr_id: str
    count: int
    '''데이터 개수'''

    def __init__(self, data: str, parse: bool = True, encrypt: KisRTEncrypt | None = None):
        items = data.split('|')
        self.encrypt = items[0] == '1'
        self.tr_id = items[1]
        self.count = int(items[2])
        if parse:
            data = items[3]

            if self.encrypt:
                if not encrypt:
                    raise Exception('암호화된 데이터는 암호화 객체가 필요합니다.')

                data = encrypt.decrypt(data)

            self._parse(data)
    
    def _parse(self, res: str):
        items = res.split('^')
        j = len(items)
        l = 0

        for k, v in self.__annotations__.items():
            if l >= j:
                break

            i = items[l]
            l += 1

            if v != str:
                nullable = False
                
                if isinstance(v, types.UnionType):
                    atype = get_args(v)
                    if len(atype) != 2: raise Exception('Union type must have 2 types')
                    v, nullable = atype
                    if nullable == types.NoneType: nullable = True

                try:
                    if v == bool:
                        i = i == 'Y'
                    elif v == int:
                        i = int(i)
                    elif v == float:
                        i = float(i)
                    elif v == datetime:
                        i = datetime.strptime(i, '%Y%m%d')
                    elif v == time:
                        i = datetime.strptime(i, '%H%M%S').time()
                    elif v.__name__ == 'Literal':
                        pass
                except Exception as e:
                    if nullable: i = None
                    else: raise Exception(f'Failed to convert {k}: {i} to type {v}, {e}') from e

            self.__dict__[k] = i

    @staticmethod
    def get_tr_id(data: str):
        return data.split('|')[1]