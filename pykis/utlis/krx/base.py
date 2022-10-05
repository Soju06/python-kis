from abc import abstractmethod
from datetime import datetime
import requests
from typing import Literal, TypeVar

from ...client import KisDynamic

TITEM = TypeVar('TITEM', bound=KisDynamic)

class KRXBase(KisDynamic):
    bld = ''

    @staticmethod
    def _fetch(
        bld: str,
        response: type[TITEM],
        **data
    ) -> list[TITEM] | TITEM:
        res = requests.post(
            'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'bld': bld,
                **data
            }
        )

        res.raise_for_status()

        data = res.json()

        if 'OutBlock_1' in data and isinstance(data['OutBlock_1'], list):
            return [response(item) for item in data['OutBlock_1']]
        else:
            return response(data)

    @staticmethod
    def _last_date() -> datetime:
        eres = requests.get(
            'http://data.krx.co.kr/comm/bldAttendant/executeForResourceBundle.cmd?baseName=krx.mdc.i18n.component&key=B128.bld&locale=ko')
        eres.raise_for_status()
        return datetime.strptime(eres.json()['result']['output'][0]['max_work_dt'], '%Y%m%d')
