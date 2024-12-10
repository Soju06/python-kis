
![header](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=260&section=header&text=%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%ED%95%9C%EA%B5%AD%ED%88%AC%EC%9E%90%EC%A6%9D%EA%B6%8C%20API&fontSize=50&animation=fadeIn&fontAlignY=38&desc=KIS%20Open%20Trading%20API%20Client&descAlignY=51&descAlign=62&customColorList=24)

## 1. 파이썬용 한국투자증권 API 소개 ✨

한국투자증권의 트레이딩 OPEN API 서비스를 파이썬 환경에서 사용할 수 있도록 만든 강력한 커뮤니티 라이브러리입니다.

**2.0.0 버전 이전의 라이브러리는 [여기](https://github.com/Soju06/python-kis/tree/v1.0.6), 문서는 [1](https://github.com/Soju06/python-kis/wiki/Home/d6aaf207dc523b92b52e734908dd6b8084cd36ff), [2](https://github.com/Soju06/python-kis/wiki/Tutorial/d6aaf207dc523b92b52e734908dd6b8084cd36ff), [3](https://github.com/Soju06/python-kis/wiki/Examples/d6aaf207dc523b92b52e734908dd6b8084cd36ff)에서 확인할 수 있습니다.**


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

2. 서비스를 신청이 완료되면, 아래와 같이 앱 키를 발급 받을 수 있습니다.

![image](https://user-images.githubusercontent.com/34199905/193740291-53f282ee-c40c-40b9-874e-2df39543cb66.png)
</details>

### 2.1. 라이브러리 설치 📦

라이브러리는 파이썬 3.11을 기준으로 작성되었습니다.

```zsh
pip install python-kis
```

<details>
<summary>사용된 모듈 보기</summary>

```
requests>=2.32.3
websocket-client>=1.8.0
cryptography>=43.0.0
colorlog>=6.8.2
```
</details>

<hr>

### 2.2. 라이브러리 사용 📚

#### 2.2.1. PyKis 객체 생성

1. 시크릿 키를 파일로 관리하는 방법 (권장)
   
   먼저 시크릿 키를 파일로 저장합니다.
   ```python
    from pykis import KisAuth

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
        virtual=False,
    )

    # 안전한 경로에 시크릿 키를 파일로 저장합니다.
    auth.save("secret.json")
    ```

    그 후, 저장된 시크릿 키를 사용하여 PyKis 객체를 생성합니다.

    ```python
    from pykis import PyKis, KisAuth

    # 실전투자용 PyKis 객체를 생성합니다.
    kis = PyKis("secret.json", keep_token=True)
    kis = PyKis(KisAuth.load("secret.json"), keep_token=True)

    # 모의투자용 PyKis 객체를 생성합니다.
    kis = PyKis("secret.json", "virtual_secret.json", keep_token=True)
    kis = PyKis(KisAuth.load("secret.json"), KisAuth.load("virtual_secret.json"), keep_token=True)
    ```
2. 시크릿 키를 직접 입력하는 방법
    ```python
    from pykis import PyKis

    # 실전투자용 한국투자증권 API를 생성합니다.
    kis = PyKis(
        id="soju06",  # HTS 로그인 ID
        account="00000000-01",  # 계좌번호
        appkey="PSED321z...",  # AppKey 36자리
        secretkey="RR0sFMVB...",  # SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )

    # 모의투자용 한국투자증권 API를 생성합니다.
    kis = PyKis(
        id="soju06",  # HTS 로그인 ID
        account="00000000-01",  # 모의투자 계좌번호
        appkey="PSED321z...",  # 실전투자 AppKey 36자리
        secretkey="RR0sFMVB...",  # 실전투자 SecretKey 180자리
        virtual_id="soju06",  # 모의투자 HTS 로그인 ID
        virtual_appkey="PSED321z...",  # 모의투자 AppKey 36자리
        virtual_secretkey="RR0sFMVB...",  # 모의투자 SecretKey 180자리
        keep_token=True,  # API 접속 토큰 자동 저장
    )
    ```

#### 2.2.2. 시세 조회

`stock.quote()` 함수를 이용하여 국내주식 및 해외주식의 시세를 조회할 수 있습니다.

```python
from pykis import KisQuote

# 엔비디아의 상품 객체를 가져옵니다.
stock = kis.stock("NVDA")

quote: KisQuote = stock.quote()
quote: KisQuote = stock.quote(extended=True) # 주간거래 시세

# PyKis의 모든 객체는 repr을 통해 주요 내용을 확인할 수 있습니다.
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
from pykis import KisBalance

# 주 계좌 객체를 가져옵니다.
account = kis.account()

balance: KisBalance = account.balance()

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
from pykis import KisOrder

# SK하이닉스 1주 시장가 매수 주문
order: KisOrder = hynix.buy(qty=1)
# SK하이닉스 1주 지정가 매수 주문
order: KisOrder = hynix.buy(price=194700, qty=1)
# SK하이닉스 전량 시장가 매도 주문
order: KisOrder = hynix.sell()
# SK하이닉스 전량 지정가 매도 주문
order: KisOrder = hynix.sell(price=194700)

print(order.pending) # 미체결 주문인지 여부
print(order.pending_order.pending_qty) # 미체결 수량

order: KisOrder = order.modify(price=195000) # 단가 정정
order: KisOrder = order.modify(qty=10) # 수량 정정

order.cancel() # 주문 취소

# 미체결 주문 전체 취소
for order in account.pending_orders():
    order.cancel()
```


#### 2.2.4. 실시간 체결가 조회

국내주식 및 해외주식의 실시간 체결가 조회는 `stock.on("price", callback)` 함수를 이용하여 수신할 수 있습니다.

```python
from pykis import KisRealtimePrice, KisSubscriptionEventArgs, KisWebsocketClient, PyKis

def on_price(sender: KisWebsocketClient, e: KisSubscriptionEventArgs[KisRealtimePrice]):
    print(e.response)

ticket = hynix.on("price", on_price)

print(kis.websocket.subscriptions) # 현재 구독중인 이벤트 목록

input("Press Enter to exit...")

ticket.unsubscribe()
```

```python
{KisWebsocketTR(id='H0STCNT0', key='000660')}
Press Enter to exit...
[08/02 13:50:42] INFO: RTC Connected to real server
[08/02 13:50:42] INFO: RTC Restoring subscriptions... H0STCNT0.000660
[08/02 13:50:42] INFO: RTC Subscribed to H0STCNT0.000660
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:44+09:00', price=174900, change=-18400, volume=8919304, amount=1587870362300)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:44+09:00', price=174800, change=-18500, volume=8919354, amount=1587879102300)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174800, change=-18500, volume=8919358, amount=1587879801500)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174900, change=-18400, volume=8920313, amount=1588046831000)
KisDomesticRealtimePrice(market='KRX', symbol='000660', time='2024-08-02T13:50:45+09:00', price=174800, change=-18500, volume=8920319, amount=1588047879800)

[08/02 13:50:48] INFO: RTC Unsubscribed from H0STCNT0.000660
```

## 3. 튜토리얼 목록 📖
   
- [1. PyKis 인증 관리](https://github.com/Soju06/python-kis/wiki/Tutorial#1-pykis-인증-관리)
  - [1.1. 시크릿 키 관리](https://github.com/Soju06/python-kis/wiki/Tutorial#11-시크릿-키-관리)
  - [1.2. 엑세스 토큰 관리](https://github.com/Soju06/python-kis/wiki/Tutorial#12-엑세스-토큰-관리)
- [2. 종목 시세 및 차트 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#2-종목-시세-및-차트-조회)
  - [2.1. 시세 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#21-시세-조회)
  - [2.2. 차트 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#22-차트-조회)
  - [2.3. 호가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#23-호가-조회)
  - [2.4. 장운영 시간 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#24-장운영-시간-조회)
- [3. 주문 및 잔고 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#3-주문-및-잔고-조회)
  - [3.1. 예수금 및 보유 종목 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#31-예수금-및-보유-종목-조회)
  - [3.2. 기간 손익 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#32-기간-손익-조회)
  - [3.3. 일별 체결 내역 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#33-일별-체결-내역-조회)
  - [3.4. 매수 가능 금액/수량 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#34-매수-가능-금액수량-조회)
  - [3.5. 매도 가능 수량 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#35-매도-가능-수량-조회)
  - [3.6. 미체결 주문 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#36-미체결-주문-조회)
  - [3.7. 매도/매수 주문 및 정정/취소](https://github.com/Soju06/python-kis/wiki/Tutorial#37-매도매수-주문-및-정정취소)
    - [3.7.1. 매수/매도 주문](https://github.com/Soju06/python-kis/wiki/Tutorial#371-매수매도-주문)
    - [3.7.2. 주문 정정](https://github.com/Soju06/python-kis/wiki/Tutorial#372-주문-정정)
- [4. 실시간 이벤트 수신](https://github.com/Soju06/python-kis/wiki/Tutorial#4-실시간-이벤트-수신)
  - [4.1. 이벤트 수신을 했는데, 바로 취소됩니다.](https://github.com/Soju06/python-kis/wiki/Tutorial#41-이벤트-수신을-했는데-바로-취소됩니다)
  - [4.2. 실시간 체결가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#42-실시간-체결가-조회)
  - [4.3. 실시간 호가 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#43-실시간-호가-조회)
  - [4.4. 실시간 체결내역 조회](https://github.com/Soju06/python-kis/wiki/Tutorial#44-실시간-체결내역-조회)


## 4. Changelog ✨

### ver 2.1.3

- [HTTPSConnectionPool이 제대로 닫히지 않는 것 같습니다.](https://github.com/Soju06/python-kis/issues/58) [fixed #58: session 추가](https://github.com/Soju06/python-kis/pull/59) by @tasoo-oos
- [Refector/decorator keeping function information](https://github.com/Soju06/python-kis/pull/60) `KisChartBar`의 타이핑 문제를 해결했습니다.

### ver 2.1.2

- [fix: SyntaxError: f-string: expecting '}' but got "}"](https://github.com/Soju06/python-kis/pull/57) 파이썬 3.11 이하에서 SyntaxError 오류가 발생하는 문제를 해결했습니다. by @tasoo-oos


### ver 2.1.1

- [해외주식 실시간 체결 이벤트 버그 수정](https://github.com/Soju06/python-kis/pull/53) 해외주식 실시간 체결 이벤트를 받을 수 없는 버그를 수정했습니다.
- [이벤트 티켓 암시적 구독 해지 경고 메시지 추가](https://github.com/Soju06/python-kis/pull/55) 이벤트 티켓이 GC에 의해 해지되었을 때 경고 메시지를 추가했습니다.
- [코드 리펙토링](https://github.com/Soju06/python-kis/pull/56) 기존 `EMPTY`, `EMPTY_TYPE` 대신 `EllipsisType`를 사용하도록 변경하고, `Impl` 타입의 이름을 `Mixin`으로 변경했습니다.

### ver 2.1.0

- [몇몇 종목의 주식 객체 quote, chart 동작 관련 질문](https://github.com/Soju06/python-kis/issues/47) 상품기본정보 조회 시세조회 가능 여부 확인 로직을 추가했습니다.
- [order 객체를 분실했을 때, order 객체를 다시 가져올 수 있는 방법이 있을까요?](https://github.com/Soju06/python-kis/issues/45) 미체결 주문 객체에 KisOrder 프로토콜을 지원하도록 개선했습니다.
- 인증 토큰 만료되었을 때 발생하는 예외를 핸들링하여 재발급을 시도하도록 개선했습니다.

### ver 2.0.4

- [krx 주식 002170 정보를 quote 로 가져올 때 발생하는 버그](https://github.com/Soju06/python-kis/issues/48) 국내주식 시세조회의 업종명이 없을때 발생하는 버그를 수정했습니다.

### ver 2.0.3

- [KisIntegrationBalance에서 해외주식 잔고수량이 0으로 표시됨](https://github.com/Soju06/python-kis/issues/41) 버그를 수정했습니다.

### ver 2.0.2

- `KisBalance`, `KisChart` 등 `__iter__` 메서드의 반환 타입이 누락되어있는 버그를 수정했습니다.
- 주문 수량을 입력할 때 `Decimal` 타입 이외의 `int`, `float` 타입을 입력할 수 있도록 개선했습니다.

### ver 2.0.1

- 초기 웹소켓 이벤트 구독시 클라이언트 접속 후 구독을 요청하는 코드에서 `_connected_event`가 set 되어있지 않아, 요청이 무시되는 버그를 수정했습니다.

### ver 2.0.0

- 라이브러리가 완전히 새롭게 변경되었습니다.
- 모든 객체에 대한 추상화 및 네이밍이 변경되었습니다.
- 한국투자증권의 국내, 해외 API 구분 없이 동일한 인터페이스로 사용할 수 있습니다.
- 실시간 시세 조회는 새로운 이벤트 시스템으로 변경되었습니다.
- 계좌 및 상품 Scope 활용이 극대화되었습니다.

### ver 1.0.6

- 상품기본조회가 추가되었습니다.

- 환경 변수를 분리하였습니다.
  각각의 파일에 나뉘어있던 Version, 접속 URL, API Rate Limit 등의 상수 데이터를 `__env__.py`로 옮겼습니다.

- 예외구조 변경
  기존 HTTP Error, RT_CD Error를 모두 `ValueError`로 처리하던 구조에서 각각의 `KisHTTPError`, `KisAPIError` 예외 객체로 나누었고, `rt_cd`, `msg_cd` 등의 변수를 예외 객체에서 참조할 수 있도록 변경하였습니다.

- 엑세스토큰 발급 Thread Safe
  엑세스 토큰이 발급되어있지 않은 상태에서 멀티스레드로 `KisAccessToken.ensure()` 함수를 호출하면 Thread Lock 되지 않고 다수가 `KisAccessToken.issue()`를 호출하는 문제를 해결하였습니다.

### ver 1.0.5

- `RTClient`에서 웹소켓 연결이 끊어졌을 때, 이벤트 처리가 잘못되는 버그를 수정하였습니다.

- `RTClient`에서 재연결시 실시간 조회가 복구되지 않는 버그를 수정하였습니다.

- 휴장일 조회가 추가되었습니다.

- 해외 주식 주문이 추가되었습니다.

- 해외 미체결 조회가 추가되었습니다.

### ver 1.0.4

- 주식잔고조회_실현손익 조회가 추가되었습니다.

- [실시간 해제요청이 정상적으로 되지 않습니다](https://github.com/Soju06/python-kis/issues/1) 버그를 수정하였습니다.

### ver 1.0.3

- `RTClient` [웹소켓 보안강화를 위한 개선 안내](https://apiportal.koreainvestment.com/community/10000000-0000-0011-0000-000000000001)의 내용에 따라, 앱키 대신 웹소켓 접속키를 발급하여 사용하도록 변경되었습니다.

### ver 1.0.2

- API 초당 요청 제한을 넘어버리는 버그를 수정하였습니다.
- `period_price` 응답 데이터의 `stck_fcam`값 `float`으로 변경하였습니다.
- `utils.KRXMarketOpen` 공휴일 데이터가 1개인 경우 오류 발생하는 버그 수정하였습니다.


### License

[MIT](https://github.com/Soju06/python-kis/blob/main/LICENCE)