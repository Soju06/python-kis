kis = PyKis(KisKey.load("key.json"))
account = kis.account("50087142-01", primary=True)

for stock in account.stocks():
    if stock.qty < 1:
        stock.sell_all() # 시장가 전량 매도
        
    chart = stock.day_chart()
    
    if chart[-1].close > chart[-2].close:
        stock.buy(qty=1) # 시장가 1주 매수

nvida = kis.stock("NVDA")
print(nvida.price())
print(account.stock(nvida).qty)

# 주문
order = nvida.buy(qty=10) # 시장가 10주 매수

# 체결 이벤트
event = account.on("order", lambda order: print(order))
event.cancel()
# 단일 체결 이벤트 (특정 주문만)
account.once("order", lambda order: print(order), where=order)

# 주문 정정
order.modify(price=485.09)
# 주문 취소
order.cancel()

# 종목 실시간 시세
nvida.on("tick", lambda tick: print(tick))

# 종목 검색
for stock in kis.search("삼성전자"):
    print(stock.code, stock.name)

# 거래량 상위 10개 종목
for stock in kis.top_volume():
    print(stock.code, stock.name)
