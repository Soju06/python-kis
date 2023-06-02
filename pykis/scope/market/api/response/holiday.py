from datetime import timedelta
from ...._import import *

# Output	응답상세1	Object	Y		
# -bass_dt	기준일자	String	Y	8	기준일자(YYYYMMDD)
# -wday_dvsn_cd	요일구분코드	String	Y	2	01:일요일, 02:월요일, 03:화요일, 04:수요일, 05:목요일, 06:금요일, 07:토요일
# -bzdy_yn	영업일여부	String	Y	1	Y/N
# -tr_day_yn	거래일여부	String	Y	1	Y/N
# -opnd_yn	개장일여부	String	Y	1	Y/N
# -sttl_day_yn	결제일여부	String	Y	1	Y/N

WEEKDAY_DVSN_CD_CODES = {
    '01': '일요일',
    '02': '월요일',
    '03': '화요일',
    '04': '수요일',
    '05': '목요일',
    '06': '금요일',
    '07': '토요일'
}

class KisMarketHoliday(KisDynamic):
    bass_dt: date
    '''기준일자'''
    wday_dvsn_cd: Literal['01', '02', '03', '04', '05', '06', '07']
    '''요일구분코드'''
    bzdy_yn: bool
    '''영업일여부'''
    tr_day_yn: bool
    '''거래일여부'''
    opnd_yn: bool
    '''개장일여부'''
    sttl_day_yn: bool
    '''결제일여부'''

    @property
    def date(self) -> date:
        '''기준일자'''
        return self.bass_dt

    @property
    def wday_dvsn_cd_name(self) -> str:
        '''요일구분코드 이름'''
        return WEEKDAY_DVSN_CD_CODES[self.wday_dvsn_cd]
    
    @property
    def is_holiday(self) -> bool:
        '''휴장일 여부'''
        return not self.opnd_yn
    
    @property
    def is_trading_day(self) -> bool:
        '''거래일 여부'''
        return self.tr_day_yn
    
    @property
    def is_settlement_day(self) -> bool:
        '''결제일 여부'''
        return self.sttl_day_yn
    
    @property
    def is_business_day(self) -> bool:
        '''영업일 여부'''
        return self.bzdy_yn
    
    @property
    def is_today(self) -> bool:
        '''오늘 여부'''
        return self.bass_dt == datetime.today()
    
    @property
    def is_yesterday(self) -> bool:
        '''어제 여부'''
        return self.bass_dt == datetime.today() - timedelta(days=1)
    
    @property
    def is_tomorrow(self) -> bool:
        '''내일 여부'''
        return self.bass_dt == datetime.today() + timedelta(days=1)
    

class KisMarketHolidays(KisDynamicZeroPagingAPIResponse):
    holidays: dict[date, KisMarketHoliday]
    '''휴장일 목록'''

    def __init__(self, data: dict, response: requests.Response):
        super().__init__(data, response)

        self.holidays = {}

        for holiday in data['output']:
            holiday = KisMarketHoliday(holiday)
            self.holidays[holiday.bass_dt] = holiday

    def __getitem__(self, key: date | datetime | str) -> KisMarketHoliday:
        if isinstance(key, datetime):
            key = key.date()
        elif isinstance(key, str):
            key = datetime.strptime(key, '%Y%m%d').date()
            
        return self.holidays[key]
    
    def __contains__(self, key: date) -> bool:
        return key in self.holidays
    
    def __iter__(self):
        return iter(self.holidays.values())
    
    def __len__(self) -> int:
        return len(self.holidays)
    
    def __add__(self, other: 'KisMarketHolidays'):
        self.holidays.update(other.holidays)
        return self
    
    def get(self, key: date | datetime | str) -> KisMarketHoliday | None:
        '''휴장일 정보 조회'''
        if isinstance(key, datetime):
            key = key.date()
        elif isinstance(key, str):
            key = datetime.strptime(key, '%Y%m%d').date()
            
        return self.holidays.get(key)
    
    @property
    def first(self) -> KisMarketHoliday:
        '''첫번째 휴장일 정보'''
        return next(iter(self.holidays.values()))
    
    @property
    def today(self) -> KisMarketHoliday | None:
        '''오늘 휴장일 정보'''
        return self.holidays.get(datetime.today())
    
    @property
    def yesterday(self) -> KisMarketHoliday | None:
        '''어제 휴장일 정보'''
        return self.holidays.get(datetime.today() - timedelta(days=1))
    
    @property
    def tomorrow(self) -> KisMarketHoliday | None:
        '''내일 휴장일 정보'''
        return self.holidays.get(datetime.today() + timedelta(days=1))
    