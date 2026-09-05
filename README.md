![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%ED%95%9C%EA%B5%AD%ED%88%AC%EC%9E%90%EC%A6%9D%EA%B6%8C%20API&fontSize=50&animation=fadeIn&fontAlignY=38&desc=KIS%20Open%20Trading%20API%20Client&descAlignY=51&descAlign=62&customColorList=24)

[![CI](https://github.com/visualmoney/vm-stock-kis/actions/workflows/ci.yml/badge.svg)](https://github.com/visualmoney/vm-stock-kis/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/vm-stock-kis)](https://pypi.org/project/vm-stock-kis/)
[![Python](https://img.shields.io/pypi/pyversions/vm-stock-kis)](https://pypi.org/project/vm-stock-kis/)
[![License](https://img.shields.io/pypi/l/vm-stock-kis)](./LICENCE)

## 1. 파이썬용 한국투자증권 API 소개 ✨

한국투자증권의 트레이딩 OPEN API 서비스를 파이썬 환경에서 사용할 수 있도록 만든 강력한 커뮤니티 라이브러리입니다.

업스트림 [`python-kis`](https://github.com/Soju06/python-kis) 1.x 는
[v1.0.6 태그](https://github.com/Soju06/python-kis/tree/v1.0.6)와 위키 스냅샷
[Home](https://github.com/Soju06/python-kis/wiki/Home/d6aaf207dc523b92b52e734908dd6b8084cd36ff) ·
[Tutorial](https://github.com/Soju06/python-kis/wiki/Tutorial/d6aaf207dc523b92b52e734908dd6b8084cd36ff) ·
[Examples](https://github.com/Soju06/python-kis/wiki/Examples/d6aaf207dc523b92b52e734908dd6b8084cd36ff)
에 있습니다. 이 배포판(`vm-stock-kis`)의 사용법은 아래와
[CHANGELOG.md](./CHANGELOG.md) 를 보세요.

### 빠른 시작

- [QUICKSTART.md](./QUICKSTART.md) — 설치, 설정 파일 예제, 테스트 팁
- [SECURITY.md](./SECURITY.md) ([English](./SECURITY.en.md)) — 자격증명 취급 방식과 취약점 신고
- 예제 모음: [examples/01_basic](./examples/01_basic) (hello_world, 시세/잔고, 주문, 실시간 체결가)

> **찾는 기능이 없나요?** 이 라이브러리는 KIS OpenAPI 중 **주식 현물만** 구현합니다.
> 선물옵션·채권·ELW·순위분석 등은 전용 메서드가 없습니다. 그래도
> [`fetch()` 로 직접 호출](./docs/user/EXTENDING_API.md)할 수 있습니다 —
> 토큰 갱신·도메인 라우팅·Rate Limiting·재시도가 그대로 적용됩니다.
> 전량 codegen 이관은 하지 않습니다 (`#100` **B**: 수요 기반 TR, 이슈 한 건 = TR 하나).

> **시세 재배포.** 받은 시세는 본인 업무 범위 안에서만 쓰세요. 제3자 제공·외부
> 서비스화는 약관(고객) 제5조 ③으로 금지되며 이용 중지 사유입니다. 전문은
> [KIS Developers](https://apiportal.koreainvestment.com/) 약관을 보세요.
> ([USER_GUIDE](./docs/user/USER_GUIDE.md#시세-조회))

### 1.1. 라이브러리 특징

<details>
<summary>📐 모든 객체에 대한 Type hint</summary>
<ul>
<li>모든 함수와 클래스에 대해 추상화 및 Typing을 적용하여, 파이썬의 동적 타이핑을 보완합니다.</li>
<li>IDE의 자동완성을 100% 활용할 수 있으며, 공식 문서 없이 정확하고 버그 없는 개발이 가능합니다.</li>
</ul>
</details>

<details>
<summary>🔗 복구 가능한 웹소켓 클라이언트</summary>
<ul>
<li>실시간 시세, 호가, 체결 등의 실시간 데이터를 받아오는 과정에서 네트워크 문제 등으로 인해 연결이 끊겼을 때, 완벽히 복구할 수 있도록 만들어졌습니다.</li>
<li>재연결 이전에 등록된 조회도 자동으로 다시 등록하여 유실을 방지합니다.</li>
<li>한국투자증권의 웹소켓 조회 시스템을 파이썬의 메모리 관리 시스템과 완벽히 통합하여, GC에 의해 이벤트 구독이 관리됩니다.</li>
</details>

<details>
<summary>🖋️ 표준 영어 네이밍</summary>
<ul>
<li>한국투자증권의 API의 경우, 한글 발음이나 비표준 약어를 사용하는 경우가 많습니다.</li>
<li>이 라이브러리는 모든 객체에 대해 표준 영어 네이밍을 적용하여, 이해하기 쉽도록 만들었습니다.</li>
</details>

<hr>

## 2. 사용 설명 ⚙️

<details>
<summary>OpenAPI 서비스 신청 방법</summary>

1. 한국투자증권 계좌와 아이디가 필요합니다. KIS 트레이딩 서비스는 [KIS Developers 서비스](https://apiportal.koreainvestment.com/)를 통해 신청 할 수 있습니다.

![image](https://user-images.githubusercontent.com/34199905/193738291-c9c663fd-8ab4-43da-acb6-6a2f7846a79d.png)

1. 서비스를 신청이 완료되면, 아래와 같이 앱 키를 발급 받을 수 있습니다.

![image](https://user-images.githubusercontent.com/34199905/193740291-53f282ee-c40c-40b9-874e-2df39543cb66.png)
</details>

### 2.1. 라이브러리 설치 📦

파이썬 3.10 이상이 필요합니다.

```zsh
pip install vm-stock-kis
```

<details>
<summary>사용된 모듈 보기</summary>

```text
requests>=2.32.3
websocket-client>=1.8.0
cryptography>=43.0.0
colorlog>=6.8.2
```

</details>

<hr>

### 2.2. 라이브러리 사용 📚

#### 2.2.1. VmKis 객체 생성

1. 시크릿 키를 파일로 관리하는 방법 (권장)

   먼저 시크릿 키를 파일로 저장합니다.

   ```python
    from vmkis import KisAuth

    auth = KisAuth(
        # HTS 로그인 ID  예) soju06
        id="YOUR_HTS_ID",
        # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
        appkey="YOUR_APP_KEY",
        # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
        secretkey="YOUR_APP_SECRET",
        # 앱 키와 연결된 계좌번호  예) 00000000-01
        account="00000000-01",
        # 모의투자 여부
        paper=False,
    )

    # 안전한 경로에 시크릿 키를 파일로 저장합니다.
    auth.save("secret.json")
    ```

    그 후, 저장된 시크릿 키를 사용하여 VmKis 객체를 생성합니다.

    ```python
    from vmkis import VmKis, KisAuth

    # 실전투자용 VmKis 객체를 생성합니다.
    kis = VmKis("secret.json", keep_token=True)
    kis = VmKis(KisAuth.load("secret.json"), keep_token=True)

    # 모의투자용 VmKis 객체를 생성합니다.
    kis = VmKis("secret.json", "paper_secret.json", keep_token=True)
    kis = VmKis(KisAuth.load("secret.json"), KisAuth.load("paper_secret.json"), keep_token=True)
    ```

2. 시크릿 키를 직접 입력하는 방법

    ```python
    from vmkis import VmKis

    # 실전투자용 한국투자증권 API를 생성합니다.
    kis = VmKis(
        id="soju06",  # HTS 로그인 ID
        account="00000000-01",  # 계좌번호
        appkey="PSED321z...",  # AppKey 36자리
        secretkey="RR0sFMVB...",  # SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )

    # 모의투자용 한국투자증권 API를 생성합니다.
    kis = VmKis(
        id="soju06",  # HTS 로그인 ID
        account="00000000-01",  # 모의투자 계좌번호
        appkey="PSED321z...",  # 실전투자 AppKey 36자리
        secretkey="RR0sFMVB...",  # 실전투자 SecretKey 180자리
        paper_id="soju06",  # 모의투자 HTS 로그인 ID
        paper_appkey="PSED321z...",  # 모의투자 AppKey 36자리
        paper_secretkey="RR0sFMVB...",  # 모의투자 SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )
    ```

#### 2.2.2. 시세 조회

`stock.quote()` 함수를 이용하여 국내주식 및 해외주식의 시세를 조회할 수 있습니다.

```python
from vmkis import Quote

# 엔비디아의 상품 객체를 가져옵니다.
stock = kis.stock("NVDA")

quote: Quote = stock.quote()
quote: Quote = stock.quote(extended=True) # 주간거래 시세

# VmKis의 모든 객체는 repr을 통해 주요 내용을 확인할 수 있습니다.
# 데이터를 확인하는 용도이므로 실제 프로퍼티 타입과 다를 수 있습니다.
print(quote)
```

```python
KisForeignQuote(
    symbol='NVDA',
    market='NASDAQ',
    name='엔비디아',
    sector_name='반도체 및 반도체장비',
    volume=1506310,
    amount=160791125,
    market_cap=2593332000000,
    indicator=KisForeignIndicator(
        eps=1.71,
        bps=2,
        per=63.88,
        pbr=54.65,
        week52_high=140.76,
        week52_low=39.2215,
        week52_high_date='2024-06-20',
        week52_low_date='2023-10-31'
    ),
    open=109.21,
    high=109.38,
    low=104.37,
    close=105.42,
    change=-3.79,
    unit=1,
    tick=0.01,
    risk='none',
    halt=False,
    overbought=False
)
```

#### 2.2.3. 잔고 조회

`account.balance()` 함수를 이용하여 예수금 및 보유 종목을 조회할 수 있습니다.

```python
from vmkis import Balance

# 주 계좌 객체를 가져옵니다.
account = kis.account()

balance: Balance = account.balance()

print(repr(balance)) # repr을 통해 객체의 주요 내용을 확인할 수 있습니다.
```

```python
KisIntegrationBalance(
    account_number=KisAccountNumber('50113500-01'),
    deposits={
        'KRW': KisDomesticDeposit(account_number=KisAccountNumber('50113500-01'), currency='KRW', amount=2447692, exchange_rate=1),
        'USD': KisForeignPresentDeposit(account_number=KisAccountNumber('50113500-01'), currency='USD', amount=0, exchange_rate=1384.6),
    },
    stocks=[
        KisDomesticBalanceStock(account_number=KisAccountNumber('50113500-01'), market='KRX', symbol='000660', qty=14, price=192600, amount=2696400, profit=22900, profit_rate=0.856555077613615111277351786),
        KisDomesticBalanceStock(account_number=KisAccountNumber('50113500-01'), market='KRX', symbol='039200', qty=118, price=39600, amount=4672800, profit=-199500, profit_rate=-4.094575457176282248630010467)
    ],
    purchase_amount=7545800,
    current_amount=7369200,
    profit=-176600,
    profit_rate=-2.340374778022211031302181346
)
```

#### 2.2.4. 매도/매수 주문

`stock.order()`, `stock.buy()`, `stock.sell()`, `stock.modify()`, `stock.cancel()` 함수를 이용하여 매수/매도 주문 및 정정/취소를 할 수 있습니다.

```python
from vmkis import Order

hynix = kis.stock("000660")
account = kis.account()

# SK하이닉스 1주 시장가 매수 주문
order: Order = hynix.buy(qty=1)
# SK하이닉스 1주 지정가 매수 주문
order: Order = hynix.buy(price=194700, qty=1)
# SK하이닉스 전량 시장가 매도 주문
order: Order = hynix.sell()
# SK하이닉스 전량 지정가 매도 주문
order: Order = hynix.sell(price=194700)

print(order.pending) # 미체결 주문인지 여부
print(order.pending_order.pending_qty) # 미체결 수량

order: Order = order.modify(price=195000) # 단가 정정
order: Order = order.modify(qty=10) # 수량 정정

order.cancel() # 주문 취소

# 미체결 주문 전체 취소
for order in account.pending_orders():
    order.cancel()
```

#### 2.2.4. 실시간 체결가 조회

국내주식 및 해외주식의 실시간 체결가 조회는 `stock.on("price", callback)` 함수를 이용하여 수신할 수 있습니다.

```python
from vmkis import VmKis
from vmkis.types import KisRealtimePrice, KisSubscriptionEventArgs, KisWebsocketClient

def on_price(sender: KisWebsocketClient, e: KisSubscriptionEventArgs[KisRealtimePrice]):
    print(e.response)

hynix = kis.stock("000660")
ticket = hynix.on("price", on_price)

print(kis.websocket.subscriptions) # 현재 구독중인 이벤트 목록

input("Press Enter to exit...")

ticket.unsubscribe()
```

```python
{KisWebsocketTR(id='H0STCNT0', key='000660')}
Press Enter to exit...
[08/02 13:50:42] INFO: RTC Connected to live server
[08/02 13:50:42] INFO: RTC Restoring subscriptions... H0STCNT0.000660
[08/02 13:50:42] INFO: RTC Subscribed to H0STCNT0.000660
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:44+09:00', price=174900, change=-18400, volume=8919304, amount=1587870362300)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:44+09:00', price=174800, change=-18500, volume=8919354, amount=1587879102300)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174800, change=-18500, volume=8919358, amount=1587879801500)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174900, change=-18400, volume=8920313, amount=1588046831000)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174800, change=-18500, volume=8920319, amount=1588047879800)

[08/02 13:50:48] INFO: RTC Unsubscribed from H0STCNT0.000660
```

## 3. 사용 문서

- [QUICKSTART.md](./QUICKSTART.md) — 설치부터 첫 조회
- [USER_GUIDE.md](./docs/user/USER_GUIDE.md) — 인증, 시세, 주문, 잔고, 실시간
- [examples/](./examples/) — 현물 예제 (`01_basic/`)
- [EXTENDING_API.md](./docs/user/EXTENDING_API.md) — 없는 TR 은 `fetch()`
- [CHANGELOG.md](./CHANGELOG.md) — 이 배포판의 변경

이 포크는 업스트림 [`python-kis`](https://github.com/Soju06/python-kis) 2.1.6 에서
갈라졌습니다. 두 번호는 비교되지 않습니다 —
[MIGRATION_GUIDE](docs/MIGRATION_GUIDE.md#2-버전-번호가-낮아지는-이유).
업스트림 항목별 이력은
[Releases](https://github.com/Soju06/python-kis/releases) 에 있습니다.

## License

[MIT](./LICENCE)
