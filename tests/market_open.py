from datetime import datetime
from pykis import KRXMarketOpen
from pykis.timezone import tz_kst


with open('B:\\dsvck.txt', 'r') as f:
    service_key = f.readline().strip()

KRXMarketOpen.set_service_key(service_key)

server_time = KRXMarketOpen.kis_server_date()
now = datetime.now(tz=tz_kst)

print(f'서버 시간: {server_time:%Y-%m-%d %H:%M:%S} 지연: {now.timestamp()-server_time.timestamp():.2f}초')

print(f'오늘 시장 오픈 여부: {KRXMarketOpen.daily_open()}')
print(f'이전 오픈일: {KRXMarketOpen.prev_open()}')
print(f'다음 오픈일: {KRXMarketOpen.next_open()}')

tdt = datetime(2022, 10, 3)

print(f'{tdt:%Y-%m-%d} 시장 오픈 여부: {KRXMarketOpen.daily_open(tdt)}')
