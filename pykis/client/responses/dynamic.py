
from datetime import date, datetime, time
import types
from typing import get_args

STORE_RESPONSE: bool = False

def set_store_response(value: bool):
    '''응답을 저장할지 여부를 설정합니다.'''
    global STORE_RESPONSE
    STORE_RESPONSE = value

class KisDynamic:
    '''KIS 동적 응답 결과'''
    data: dict | None = None
    '''원본 응답 데이터'''

    def __init__(self, data: dict):
        self._parseDict(data)

        if STORE_RESPONSE:
            self.data = data

    def _parseDict(self, data: dict):
        for k, v in data.items():
            key = k.lower()
            if (key in ['output', 'output1', 'output2']) and isinstance(v, dict):
                self._parseDict(v)
            elif key in self.__annotations__:
                type = self.__annotations__[key]
                self.__dict__[key] = KisDynamic(v) if isinstance(v, dict) else self._convert(type, v, k)


    def _convert(self, type, value, k):
        if type != str:
            nullable = False
            
            if isinstance(type, types.UnionType):
                atype = get_args(type)
                if len(atype) != 2: raise Exception('Union type must have 2 types')
                type, nullable = atype
                if nullable == types.NoneType: nullable = True

            try:
                if type == KisDynamic:
                    return KisDynamic(value)
                elif type == bool:
                    return value == 'Y'
                elif type == int:
                    if ',' in value:
                        return int(value.replace(',', ''))
                    return int(value)
                elif type == float:
                    if ',' in value:
                        return float(value.replace(',', ''))
                    return float(value)
                elif type == datetime:
                    return datetime.strptime(value, '%Y%m%d')
                elif type == date:
                    return datetime.strptime(value, '%Y%m%d').date()
                elif type == time:
                    return datetime.strptime(value, '%H%M%S').time()
                elif type.__name__ == 'list' and len(get_args(type)) == 1:
                    item_type = get_args(type)[0]
                    return [self._convert(item_type, i, k) for i in value]
                elif type.__name__ == 'Literal':
                    return value
            except Exception as e:
                if nullable: return None
                
                raise Exception(f'Failed to convert {k}: {value} to type {type}') from e
        
            raise NotImplementedError(f'Not implemented type: {type}')

        return value

