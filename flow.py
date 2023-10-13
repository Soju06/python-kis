# 코드 흐름 정의

kis = PyKis(KisKey.load("key.json"))
account = kis.account("50087142-01", primary=True)

for stock in account.stocks():
    if stock.qty < 1:
        stock.sell_all()  # 시장가 전량 매도

    chart = stock.day_chart()

    if chart[-1].close > chart[-2].close:
        stock.buy(qty=1)  # 시장가 1주 매수

nvida = kis.stock("NVDA")
print(nvida.price())
print(account.stock(nvida).qty)

# 주문
order = nvida.buy(qty=10)  # 시장가 10주 매수

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


######


# 해당 클래스는 account.once("order", lambda order: print(order), where=order) 처럼 where문을 사용할 수 있는 베이스 클래스이다.
class KisRealtimeFilter:
    pass


class KisStock:
    kis: "PyKis"
    # 이는 scope된 account를 불러오기 위함이다.
    _account: "KisAccount | None"

    @property
    def account(self):
        return self._account or self.kis.primary_account  # kis에 primary_account가 설정되어있지 않으면 에러가 발생한다.

    # 아래와 같이 기본 account는 개체 비교를 code로 한다.
    def __eq__(self, other):
        return self.code == other.code


# event는 하나의 필터에 여러개의 콜백을 등록할 수 있으며, 이벤트를 취소할 수 있다.
class KisRealtimeEvent:
    callbacks: "List[Callable]"
    where: "KisRealtimeFilter | None"

    def add(self, callback):
        pass

    def cancel(self):
        pass


# 아래와 같이 실시간과 관련된 기능을 처리하는 베이스 클래스이다.
class KisRealtimeAdapter:
    def on(self, event, callback, where=None):
        pass


class KisAccountStock(KisStock, KisRealtimeFilter, KisRealtimeAdapter):
    pass
