from pykis import *


with open('../tests/vack.txt', 'r') as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

with open('../tests/vacco.txt', 'r') as f:
    ACCOUNT_NO = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
    # 실시간 조회 비활성화
    realtime=False
)

# 잔고
account = kis.account(ACCOUNT_NO) # 계좌번호 ex) 50071022-01 또는 5007102201

# 미국주식 매수 주문
order1 = account.buy_us(
    # 종목 코드 ex) TSLA
    'TSLA',
    # 주문 수량
    qty=1,
    # 주문 단가
    unpr=100,
)

print(order1.message)

# 주문 정정
order2 = account.revise_us(
    # 기존 주문
    order1,
    # 주문 수량 None이면 전량
    None,
    # 주문 단가
    unpr=110,
)

print(order2.message)

# 주문 취소
order3 = account.cancel_us(order2) # qty=None이면 전량
print(order3.message)


# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
