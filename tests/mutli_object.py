from datetime import timedelta
from pykis import *


with open("B:\\vack.txt", "r") as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

with open("B:\\vacco.txt", "r") as f:
    ACCOUNT_NO = f.readline().strip()

kises = [
    PyKis(
        # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
        appkey=APPKEY,
        # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
        appsecret=APPSECRET,
        # 가상 계좌 여부
        virtual_account=True,
        # 실시간 조회 비활성화
        realtime=False,
        market_auto_sync_interval=timedelta(seconds=10),
    )
    for _ in range(10)
]

input()
