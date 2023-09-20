

# 해당 클래스는 account.once("order", lambda order: print(order), where=order) 처럼 where문을 사용할 수 있는 베이스 클래스이다.
class KisRealtimeFilter:
    pass

class KisStock:
    kis: "PyKis"
    # 이는 scope된 account를 불러오기 위함이다.
    _account: "KisAccount | None"

    @property
    def account(self):
        return self._account or self.kis.primary_account # kis에 primary_account가 설정되어있지 않으면 에러가 발생한다.
    
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

