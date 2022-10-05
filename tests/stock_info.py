from datetime import datetime, timedelta
import asciichartpy as ac
from pykis import PyKis

with open('B:\\vack.txt', 'r') as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True
)

stock = kis.stock('005930')

if stock is None:
    raise ValueError('코스피/코스닥 종목이 존재하지 않습니다.')

price = stock.price()

print(stock.code, stock.name, end=' ')
print(f'전일대비율: {price.prdy_ctrt:.2f}%', end=' ')
print(f'현재가: {price.stck_prpr:,}', end=' ')
print(f'전일대비: {price.prdy_vrss:,}', end=' ')
print(f'전일대비거래량비율: {price.prdy_vrss_vol_rate:.2f}%', end=' ')
print(f'거래대금: {price.acml_tr_pbmn:,}')

now = datetime.now()
prices = stock.period_price(now-timedelta(weeks=26), now, org_adj=True)

print(f'26주 최고가: {prices.stck_hgpr} 최저가: {prices.stck_lwpr} 거래량: {prices.acml_vol:,}')

print('26주 주가')
print(ac.plot([p.stck_clpr for p in prices.prices], {'height': 16}))

print('26주 거래량')
print(ac.plot([p.acml_vol for p in prices.prices], {'height': 6}))


# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
