from pykis import *

with open('B:\\vack.txt', 'r') as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

with open('B:\\vacco.txt', 'r') as f:
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
account = kis.account(ACCOUNT_NO)  # 계좌번호 ex) 50071022-01 또는 5007102201
print(f'예수금총액: {account.balance_all().dnca_tot_amt}')

# 미국주식 매수 주문
order1 = account.overseas_buy(
    market='나스닥',
    # 종목 코드 ex) TSLA
    code='TSLA',
    # 주문 수량
    qty=1,
    # 주문 단가
    unpr=100,
)

print(order1.message)

# # 주문 정정
order2 = account.overseas_revise(
    market='나스닥',
    # 티커(종목코드)
    code='TSLA',
    # 기존 주문
    order=order1,
    # 주문 수량 (국내주식과 다르게 None 입력 불가)
    qty=1,
    # 주문 단가
    unpr=110,
)

print(order2.message)

# 전량 주문 취소
order3 = account.overseas_cancel(
    market='나스닥',
    code='TSLA',
    order=order2,
)

print(order3.message)

# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
