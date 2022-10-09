import requests
import base64
from datetime import date, datetime, timedelta
import email.utils as eut

from ..timezone import ensure_datetime, tz_kst


CACHE: dict[tuple[int, int], tuple[datetime, dict[int, str]]] = {}
SERVICE_KEY: str | None = None
REFRESH_TIME = timedelta(days=1)

def get_holiday(year: int, month: int) -> dict[int, str]:
    if SERVICE_KEY is None:
        raise RuntimeError('SERVICE_KEY is not set')

    if (year, month) in CACHE:
        updated_at, cache = CACHE[(year, month)]

        if datetime.now(tz_kst) - updated_at < REFRESH_TIME:
            return cache
    
    res = requests.get(
        'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo',
        params={
            'serviceKey': SERVICE_KEY,
            'solYear': year,
            'solMonth': f'{month:02d}',
            'numOfRows': 1000,
            '_type': 'json',
        }
    )

    if res.status_code != 200:
        raise ValueError(f'API 요청에 실패했습니다. ({res.status_code}) {res.text}')

    data = res.json()
    count = data['response']['body']['totalCount']

    if count < 1:
        data = []
    else:
        data = data['response']['body']['items']['item']

    if count == 1:
        holidays = {int(str(data['locdate'])[6:8]): data['dateName']}  # type: ignore
    else:
        holidays = dict([(int(str(item['locdate'])[6:8]), item['dateName']) for item in data])

    CACHE[(year, month)] = (datetime.now(tz_kst), holidays)

    return holidays


class KRXMarketOpen:
    '''국내 주식 시장 운영'''

    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def set_service_key(service_key: str):
        '''서비스 키를 설정합니다.

        공공데이터포털의 한국천문연구원_특일 정보를 이용합니다.

        정확한 공휴일을 계산하려면 서비스 키[일반 인증키 (Decoding)]가 필요합니다.

        서비스 키는 https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690 에서 발급받을 수 있습니다.
        '''
        if not service_key:
            raise ValueError('서비스 키가 입력되지 않았습니다.')
        
        try:
            base64.b64decode(service_key)
        except Exception:
            raise ValueError('서비스 키가 잘못되었습니다.')

        global SERVICE_KEY
        SERVICE_KEY = service_key

    @staticmethod
    def is_holiday(date: datetime | date | None = None) -> tuple[bool, str]:
        '''휴일/공휴일 여부. 폐장일은 계산되지 않습니다.'''
        date = ensure_datetime(date)
        if date.weekday() in (5, 6):
            return True, '주말'

        hds = get_holiday(date.year, date.month)

        if SERVICE_KEY is None or date.day not in hds:
            return False, '평일'
        
        return True, hds[date.day]
    
    @staticmethod
    def daily_open(date: datetime | date | None = None) -> tuple[bool, str]:
        '''일간 시장 오픈 여부'''
        date = ensure_datetime(date)
        hd, re = KRXMarketOpen.is_holiday(date)
        if hd: return False, re
        
        # 폐장일 계산
        if date.month == 12 and date.day == 31:
            return False, '폐장일'
        
        return True, re
        
    @staticmethod
    def next_open(date: datetime | date | None = None) -> date:
        '''다음 오픈일'''
        date = ensure_datetime(date)
        date += timedelta(days=1)

        while True:
            hd, _ = KRXMarketOpen.daily_open(date)
            if hd: break
            date += timedelta(days=7 - date.weekday() if date.weekday() >= 4 else 1)
        
        return date.date()

    @staticmethod
    def prev_open(date: datetime | date | None = None) -> date:
        '''이전 오픈일'''
        date = ensure_datetime(date)
        date -= timedelta(days=1)

        while True:
            hd, _ = KRXMarketOpen.daily_open(date)
            if hd: break
            date -= timedelta(days=1)
        
        return date.date()

    @staticmethod
    def kis_server_date() -> datetime:
        '''KIS 서버 시간 (서비스 키 필요 없음)'''
        res = requests.get('https://openapi.koreainvestment.com:9443')
        return eut.parsedate_to_datetime(res.headers['Date']).astimezone(tz_kst) + (res.elapsed / 2)
