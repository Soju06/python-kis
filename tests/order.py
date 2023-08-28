from pykis import *


with open("B:\\vack.txt", "r") as f:
    APPKEY = f.readline().strip()
    APPSECRET = f.readline().strip()

with open("B:\\vacco.txt", "r") as f:
    ACCOUNT_NO = f.readline().strip()

kis = PyKis(
    # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    appkey=APPKEY,
    # 앱 시크릿  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    appsecret=APPSECRET,
    # 가상 계좌 여부
    virtual_account=True,
    # 실시간 조회 비활성화
    realtime=False,
)

# 잔고
account = kis.account(ACCOUNT_NO)  # 계좌번호 ex) 50071022-01 또는 5007102201

# 주식 정보
stock = kis.stock_search("하이닉스")

if not stock:
    print("주식 정보를 찾을 수 없습니다.")
    exit(1)

# 현재가 조회
unpr = stock.price().stck_prpr - 500  # 현재가 - 500원

# 매수가능 수량 조회
amount = account.amount(stock.code, unpr)

# 최대 매수 가능 수량
qty = amount.max_buy_qty

print(f"매수 수량: {qty:,}")
print(f"매수 단가: {unpr:,}")
print(f"매수 금액: {amount.max_buy_amt:,}")

# 매수 주문
order = account.buy(
    # 종목 코드 ex) 000660
    stock.code,
    # 주문 수량
    qty=qty,
    # 주문 단가
    unpr=unpr,
)

print(order.message)

# 주문 정정
order = account.revise(
    # 기존 주문
    order,
    # 주문 수량 None이면 전량
    None,
    unpr - 100,
)

print(order.message)

# 주문 취소
order = account.cancel(order)  # qty=None이면 전량

print(order.message)


# FM 대로 사용 다한 임시 토큰은 삭제함.
if kis.client.token:
    kis.client.token.discard()
