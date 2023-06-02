from datetime import datetime, timedelta
from pykis import PyKis

with open("B:\\vack.txt", "r") as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
)


for holiday in kis.market.holiday():
    print(
        f"{holiday.bass_dt:%Y-%m-%d} {holiday.wday_dvsn_cd_name} 휴장: {holiday.is_holiday} 거래: {holiday.is_trading_day} 결제: {holiday.is_settlement_day} 영업: {holiday.is_business_day}"
    )

today = kis.market.today()

# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
