# VM-Stock-KIS - 사용자 문서

## 목차

1. [설치 및 초기 설정](#설치-및-초기-설정)
2. [빠른 시작](#빠른-시작)
3. [인증 관리](#인증-관리)
4. [시세 조회](#시세-조회)
5. [주문 관리](#주문-관리)
6. [잔고 및 계좌](#잔고-및-계좌)
7. [실시간 데이터](#실시간-데이터)
8. [고급 기능](#고급-기능)
9. [FAQ](#faq)
10. [문제 해결](#문제-해결)

---

## 설치 및 초기 설정

### 설치

```bash
# pip을 이용한 설치
pip install vm-stock-kis

# 또는 git에서 직접 설치
pip install git+https://github.com/visualmoney/vm-stock-kis.git
```

### 사전 준비

1. **한국투자증권 계좌** 필요
2. **OpenAPI 신청**
   - [KIS Developers](https://apiportal.koreainvestment.com/) 접속
   - 서비스 신청
   - App Key 발급받기

3. **필요한 정보**
   - HTS 로그인 ID
   - App Key (36자리)
   - Secret Key (180자리)
   - 계좌번호 (예: 00000000-01)

### 첫 번째 실행

```python
from vmkis import VmKis, KisAuth

# 방법 1: 직접 입력
kis = VmKis(
    id="YOUR_HTS_ID",           # HTS 로그인 ID
    account="00000000-01",       # 계좌번호
    appkey="YOUR_APP_KEY",       # App Key 36자
    secretkey="YOUR_SECRET_KEY", # Secret Key 180자
)

# 테스트
stock = kis.stock("000660")      # SK하이닉스
print(stock.quote())             # 시세 조회

kis.close()  # 또는 with 문 사용
```

---

## 빠른 시작

### 가장 간단한 예제

```python
from vmkis import VmKis

# 1. VmKis 객체 생성
kis = VmKis("secret.json", keep_token=True)

# 2. 주식 시세 조회
stock = kis.stock("000660")      # SK하이닉스
quote = stock.quote()
print(f"가격: {quote.price}, 변동: {quote.change}")

# 3. 계좌 잔고 조회
account = kis.account()
balance = account.balance()
print(f"예수금: {balance.deposits['KRW'].amount}")

# 4. 매수 주문
order = stock.buy(qty=1, price=100000)
print(f"주문: {order.order_number}")

# 5. 정리
kis.close()
```

### Context Manager 사용 (권장)

```python
from vmkis import VmKis

with VmKis("secret.json", keep_token=True) as kis:
    # 자동으로 정리됨
    stock = kis.stock("000660")
    quote = stock.quote()
    print(quote)
```

---

## 인증 관리

사용자가 알 면은 `create_client` 와 `kis.stock` / `kis.account` 입니다.
`SimpleKIS` 는 그 위 선택입니다. 없는 TR 은
[EXTENDING_API](EXTENDING_API.md) 의 `fetch()` 로 엽니다. 모듈 구조는
[ARCHITECTURE](../architecture/ARCHITECTURE.md) §1 허브-스포크 하나입니다.

JSON(`KisAuth` → `VmKis("secret.json")`)과 YAML(`create_client`) 둘 다
유효합니다. `VmKis` 경로에는 JSON만 넘깁니다. YAML 설정은
[QUICKSTART](../../QUICKSTART.md) 의 `create_client` 를 보세요.

### 1. 파일 기반 인증 (권장)

#### Step 1: 인증 정보 파일 생성

```python
from vmkis import KisAuth

# 인증 정보 생성
auth = KisAuth(
    id="soju06",
    appkey="Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX",
    secretkey="V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY...",
    account="50113500-01"
)

# 파일로 저장 (평문 JSON입니다. 본인만 읽도록 권한을 제한하세요)
auth.save("secret.json")
```

#### Step 2: 저장된 파일 불러오기

```python
from vmkis import VmKis

# 저장된 파일 불러오기
kis = VmKis("secret.json", keep_token=True)

# 또는
from vmkis import KisAuth
auth = KisAuth.load("secret.json")
kis = VmKis(auth)
```

### 2. 환경 변수 사용

`.env` 파일을 읽으려면 **python-dotenv 를 따로 설치해야 합니다.**

```console
$ pip install python-dotenv
```

vm-stock-kis 는 이것을 끌어오지 않습니다. `load_dotenv()` 는 프로세스 전역
`os.environ` 을 변형하므로, `import vmkis` 만으로 환경이 바뀔지는 라이브러리가
아니라 **애플리케이션이 정할 일**이기 때문입니다.

> `.env` 를 쓰지 않는다면 설치할 필요가 없습니다. 아래 코드에서
> `load_dotenv()` 두 줄을 빼고 셸에서 환경 변수를 지정해도 동일하게 동작합니다.

```python
# .env 파일 생성
KIS_ID=your_hts_id
KIS_APPKEY=your_app_key
KIS_SECRETKEY=your_secret_key
KIS_ACCOUNT=your_account

# Python 코드
from vmkis import VmKis
import os
from dotenv import load_dotenv

load_dotenv()

kis = VmKis(
    id=os.getenv("KIS_ID"),
    appkey=os.getenv("KIS_APPKEY"),
    secretkey=os.getenv("KIS_SECRETKEY"),
    account=os.getenv("KIS_ACCOUNT"),
)
```

### 3. 모의투자 설정

```python
from vmkis import VmKis

# 실전 인증과 모의 인증을 함께 넘기면 **모의 클라이언트**가 됩니다.
kis = VmKis(
    "live_secret.json",     # 실전 계정 (첫 번째 위치 인자)
    "paper_secret.json",    # 모의 계정 (두 번째 위치 인자)
    keep_token=True,
)

assert kis.paper is True    # 읽기 전용 프로퍼티입니다

account = kis.account()
balance = account.balance()
```

`kis.paper` 는 **대입할 수 없습니다.** 하나의 클라이언트를 실전과 모의 사이에서
전환하는 방법은 없습니다 — 실전으로 호출하려면 실전 인증만 넘긴 별도의
클라이언트를 만드세요.

```python
live_kis = VmKis("live_secret.json", keep_token=True)
assert live_kis.paper is False
```

### 4. 토큰 관리

```python
from vmkis import VmKis

# 토큰 자동 저장 (권장)
kis = VmKis("secret.json", keep_token=True)

# 토큰 자동 저장 비활성화
kis = VmKis("secret.json", keep_token=False)

# 커스텀 저장 경로
kis = VmKis("secret.json", keep_token="~/.my_kis_tokens/")
```

---

## 시세 조회

받은 시세는 **본인 업무 범위 안에서만** 쓰세요. 제3자에게 제공하거나 외부
서비스로 재배포하면 오픈 API 이용 약관(고객) 제5조 ③에 어긋나고, 이용
중지·해지 사유가 됩니다 (제9조 ①, 제10조 ①). 약관 전문은 여기 옮기지
않습니다 — 개정되기 때문입니다. 원문은
[KIS Developers](https://apiportal.koreainvestment.com/) 포털의 약관에서
확인하세요.

앱키·시크릿키 관리 책임도 고객에게 있습니다 (제5조 ②, 제17조 ②). 이
저장소는 `configs/*` 를 무시하고 템플릿만 추적합니다. 유량 제어는
라이브러리가 겁니다 (실전 19/s · 모의 2/s). 직접 루프를 돌릴 때는 본인 몫입니다.

### 1. 국내 주식 시세

```python
from vmkis import VmKis

kis = VmKis("secret.json")
stock = kis.stock("000660")  # SK하이닉스

# 현재 시세
quote = stock.quote()
print(f"종목: {quote.name}")
print(f"시가: {quote.open}")
print(f"고가: {quote.high}")
print(f"저가: {quote.low}")
print(f"종가: {quote.close}")
print(f"거래량: {quote.volume}")
print(f"변동: {quote.change}")
print(f"변동률: {quote.change_rate}")

# 주간 거래
quote_ext = stock.quote(extended=True)
print(f"주간 시세: {quote_ext}")
```

### 2. 해외 주식 시세

```python
# 미국 나스닥
apple = kis.stock("AAPL", market="NASDAQ")
quote = apple.quote()

# 미국 뉴욕
msft = kis.stock("MSFT", market="NYSE")
quote = msft.quote()

# 베이징 거래소
baidu = kis.stock("9618", market="BEIJING")
quote = baidu.quote()
```

### 3. 호가 조회

```python
stock = kis.stock("000660")

# 호가 조회
orderbook = stock.orderbook()
print(f"매도호가: {orderbook.ask_price}")
print(f"매수호가: {orderbook.bid_price}")
print(f"매도량: {orderbook.ask_volume}")
print(f"매수량: {orderbook.bid_volume}")
```

### 4. 차트 조회

```python
from datetime import date

stock = kis.stock("000660")

# 일봉
daily_chart = stock.chart(period="day", end=date(2024, 12, 10))
for bar in daily_chart:
    print(f"{bar.date}: {bar.open} -> {bar.close}")

# 주봉
weekly_chart = stock.chart(period="week")

# 월봉
monthly_chart = stock.chart(period="month")
```

---

## 주문 관리

### 1. 매수 주문

```python
from decimal import Decimal

stock = kis.stock("000660")

# 시장가 매수 (1주)
order = stock.buy(qty=1)

# 지정가 매수 (100주, 가격 지정)
order = stock.buy(qty=100, price=100000)

# 상세 정보
print(f"주문번호: {order.order_number}")
print(f"주문상태: {order.state}")
print(f"미체결수량: {order.pending_qty if order.pending else 0}")
```

### 2. 매도 주문

```python
stock = kis.stock("000660")

# 시장가 매도 (전량)
order = stock.sell()

# 지정가 매도
order = stock.sell(qty=50, price=105000)

# 부분 매도
order = stock.sell(qty=10, price=101000)
```

### 3. 주문 정정

```python
order = stock.buy(qty=10, price=100000)

# 가격 정정
new_order = order.modify(price=101000)

# 수량 정정
new_order = order.modify(qty=15)

# 가격과 수량 동시 정정
new_order = order.modify(qty=20, price=102000)
```

### 4. 주문 취소

```python
order = stock.buy(qty=10)

# 주문 취소
order.cancel()

# 또는
account = kis.account()
for pending_order in account.pending_orders():
    pending_order.cancel()
```

### 5. 주문 현황 조회

```python
account = kis.account()

# 미체결 주문 조회
pending_orders = account.pending_orders()
for order in pending_orders:
    print(f"{order.symbol}: {order.pending_qty} 주 미체결")

# 또는 특정 종목만
orders = account.pending_orders()
order_660 = next((o for o in orders if o.symbol == "000660"), None)
```

---

## 잔고 및 계좌

### 1. 잔고 조회

```python
account = kis.account()

# 통합 잔고 조회
balance = account.balance()

# 예수금
krw = balance.deposits['KRW']
print(f"원화 예수금: {krw.amount}")

# 외화 잔고
if 'USD' in balance.deposits:
    usd = balance.deposits['USD']
    print(f"달러 잔고: {usd.amount}")

# 주식 보유 현황
for stock in balance.stocks:
    print(f"{stock.symbol}: {stock.qty}주 @ {stock.price}")
    print(f"  평가금액: {stock.amount}")
    print(f"  손익: {stock.profit} ({stock.profit_rate}%)")

# 전체 손익
print(f"총 손익: {balance.profit} ({balance.profit_rate}%)")
```

### 2. 매수 가능 금액

```python
account = kis.account()
stock = kis.stock("000660")

# 계좌에서 종목·시장을 지정
orderable_amount = account.orderable_amount(market="KRX", symbol="000660")
print(repr(orderable_amount))

# 종목 스코프 (지정가)
orderable_amount = stock.orderable_amount(price=40950)
print(repr(orderable_amount))
```

### 3. 매도 가능 수량

```python
stock = kis.stock("000660")

# 해당 종목 매도 가능 수량
print(stock.orderable)
```

### 4. 일별 손익 조회

```python
account = kis.account()

from datetime import date

profits = account.profits(start=date(2024, 1, 1))
print(repr(profits))
```

### 5. 체결 내역 조회

```python
account = kis.account()

from datetime import date

orders = account.daily_orders(start=date(2024, 4, 2), end=date(2024, 6, 1))
print(repr(orders))
```

---

## 실시간 데이터

### 1. 실시간 시세

```python
from vmkis.types import KisSubscriptionEventArgs, KisRealtimePrice

stock = kis.stock("000660")

def on_price(sender, e: KisSubscriptionEventArgs[KisRealtimePrice]):
    """시세 업데이트"""
    price = e.response
    print(f"시간: {price.time}")
    print(f"가격: {price.price}")
    print(f"거래량: {price.volume}")
    print(f"변동: {price.change}")

# 구독
ticket = stock.on("price", on_price)

# 프로그램 실행 중 계속 수신
# input("Press Enter to exit...")

# 구독 해제
ticket.unsubscribe()
```

### 2. 실시간 호가

```python
def on_orderbook(sender, e):
    """호가 업데이트"""
    ob = e.response
    print(f"매도호가1: {ob.ask_price}")
    print(f"매수호가1: {ob.bid_price}")
    print(f"매도량1: {ob.ask_volume}")
    print(f"매수량1: {ob.bid_volume}")

ticket = stock.on("orderbook", on_orderbook)
```

### 3. 실시간 체결

```python
account = kis.account()

def on_execution(sender, e):
    """체결 알림"""
    execution = e.response
    print(f"체결: {execution.symbol}")
    print(f"가격: {execution.price}")
    print(f"수량: {execution.qty}")
    print(f"시각: {execution.time}")

# 계좌 전체 체결 알림
ticket = account.on("execution", on_execution)
```

### 4. 여러 종목 구독

```python
import asyncio
from time import sleep

symbols = ["000660", "005930", "035420"]

def on_price(sender, e):
    price = e.response
    print(f"{price.symbol}: {price.price}")

# 최대 40개까지 동시 구독 가능
tickets = []
for symbol in symbols:
    stock = kis.stock(symbol)
    ticket = stock.on("price", on_price)
    tickets.append(ticket)

# 실행 중...
# sleep(60)

# 정리
for ticket in tickets:
    ticket.unsubscribe()
```

---

## 고급 기능

### 1. 로깅 설정

```python
from vmkis import logging

# 로그 레벨 설정
logging.setLevel("DEBUG")  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# 상세 에러 정보 표시
from vmkis.__env__ import TRACE_DETAIL_ERROR
# TRACE_DETAIL_ERROR = True  # 주의: 앱키 노출될 수 있음
```

### 2. 에러 처리

```python
from vmkis.client.exceptions import KisAPIError, KisHTTPError
from vmkis.responses.exceptions import KisMarketNotOpenedError

try:
    stock = kis.stock("000660")
    quote = stock.quote()
except KisMarketNotOpenedError:
    print("시장이 미개장입니다")
except KisAPIError as e:
    print(f"API 에러: {e.msg1}")
    print(f"에러 코드: {e.msg_cd}")
except KisHTTPError as e:
    print(f"HTTP 에러: {e.status_code}")
except Exception as e:
    print(f"기타 에러: {e}")
finally:
    kis.close()
```

### 3. 배치 처리

```python
from time import sleep

# 여러 종목 조회
symbols = ["000660", "005930", "035420"]

for symbol in symbols:
    stock = kis.stock(symbol)
    quote = stock.quote()
    print(f"{symbol}: {quote.price}")
    # Rate limiting이 자동으로 처리됨
```

### 4. 성능 최적화

```python
# 동일한 VmKis 인스턴스 재사용
kis = VmKis("secret.json")

# 여러 요청에서 재사용
for symbol in symbols:
    stock = kis.stock(symbol)
    quote = stock.quote()  # 같은 세션 재사용
```

---

## FAQ

### Q1: "시장이 미개장" 에러가 발생합니다

**A:** 한국투자증권의 거래 시간에만 시세 조회가 가능합니다.

- 평일 09:00 - 15:30 (점심 시간 11:30-12:30 제외)
- 장 시작 시간을 확인하세요:

```python
from vmkis import VmKis
kis = VmKis("secret.json")

# 장 운영 시간 확인. market 은 필수입니다 (국가 코드도 됩니다).
hours = kis.trading_hours("KR")
print(hours.open, hours.close)
```

### Q2: 인증 에러가 발생합니다

**A:** 인증 정보를 확인하세요:

```python
# 1. 파일 경로 확인
import os
assert os.path.exists("secret.json"), "파일 없음"

# 2. 파일 내용 확인
from vmkis import KisAuth
auth = KisAuth.load("secret.json")
print(auth)  # id, account 확인

# 3. 직접 입력
kis = VmKis(
    id="your_id",           # 확인
    appkey="..." * 2 + "...",  # 36자 확인
    secretkey="..." * 6,    # 180자 확인
    account="00000000-01"   # 확인
)
```

### Q3: Rate limit 에러가 발생합니다

**A:** 요청 속도를 줄이세요:

```python
# 자동 rate limiting 확인
from vmkis import logging
logging.setLevel("DEBUG")  # 대기 시간 확인

# 대량 요청은 시간 간격을 두고
from time import sleep
for symbol in symbols:
    quote = kis.stock(symbol).quote()
    # sleep(0.5)  # 필요시 추가 대기
```

### Q4: 주문이 자동으로 취소됩니다

**A:** 주문 객체 참조 유지:

```python
# ❌ 잘못된 예
order = stock.buy(qty=10)  # 참조 유지 필요
# order 객체가 삭제되면 자동 취소됨

# ✅ 올바른 예
order = stock.buy(qty=10)
print(order.order_number)
# 또는
orders = account.pending_orders()  # 미체결 주문 재조회
```

### Q5: 비밀키는 어디에서 얻나요?

**A:** KIS Developers 포털에서:

1. <https://apiportal.koreainvestment.com/> 접속
2. 앱 관리 → 앱 상세
3. App Key, Secret Key 확인

---

## 문제 해결

### 1. 모듈 임포트 실패

```python
# ImportError: cannot import name 'VmKis'
# 해결: 설치 확인
pip list | grep vm-stock-kis

# 재설치
pip install --upgrade vm-stock-kis
```

### 2. 토큰 관련 에러

```python
# 토큰 파일 수동 삭제
import os
import shutil

token_dir = os.path.expanduser("~/.vmkis/")
if os.path.exists(token_dir):
    shutil.rmtree(token_dir)

# 다시 실행하면 새로 발급됨
```

### 3. WebSocket 연결 실패

```python
# WebSocket 비활성화로 테스트
kis = VmKis("secret.json", use_websocket=False)

# 또는 나중에 웹소켓 사용
websocket = kis.websocket  # 필요시만
```

### 4. 로그 파일 위치

```python
from vmkis.utils.workspace import get_cache_path

cache_dir = get_cache_path()
print(f"캐시 경로: {cache_dir}")
```

### 5. 성능 문제

```python
# 1. 불필요한 요청 제거
quote = stock.quote()  # 1회

# 2. 실시간 구독 활용
ticket = stock.on("price", callback)  # 연속 수신

# 3. 배치 처리로 rate limit 활용
for symbol in symbols:
    quote = kis.stock(symbol).quote()  # 자동 대기
```

---

## 추가 자료

- 🔗 [GitHub Repository](https://github.com/visualmoney/vm-stock-kis)
- 📖 [API 아키텍처 문서](../architecture/ARCHITECTURE.md)
- 👨‍💻 [개발자 가이드](../developer/DEVELOPER_GUIDE.md)
- 📋 [한국투자증권 공식 API](https://apiportal.koreainvestment.com/)

---

이 문서가 도움이 되었기를 바랍니다!
질문이나 피드백은 GitHub Issues에 제출해주세요.
