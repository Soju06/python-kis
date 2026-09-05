# SimpleKIS: 초보자용 얇은 파사드

일반적인 `VmKis` 사용법 외에, 더 간단한 인터페이스를 원한다면 **`SimpleKIS`** 를
쓰세요. 이것은 Tutorial 정본이 아닙니다. 정본은 `create_client` 와
`kis.stock` / `kis.account` 입니다. `SimpleKIS` 는 그 위 선택이고
시세·잔고·매수·취소만 있습니다. 차트·호가·매도는 `stock` / `account` 를 보세요.
구현은 [`src/vmkis/simple.py`](../src/vmkis/simple.py) 가 정본입니다.

## 1. 기본 사용법

### 1.1 방법 1: create_client 헬퍼 사용 (권장)

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

# configs/account_profiles.yaml 에서 자동 로드하여 클라이언트 생성
kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)

# 사용
price = simple.get_price("005930")
print(f"삼성전자: {price.price:,}원")
```

### 1.2 방법 2: 직접 생성

```python
from vmkis import VmKis, KisAuth
from vmkis.simple import SimpleKIS

auth = KisAuth(
    id="YOUR_ID",
    appkey="YOUR_APPKEY",
    secretkey="YOUR_SECRET",
    account="00000000-01",
    paper=True  # 모의투자 모드
)

kis = VmKis(None, auth)
simple = SimpleKIS(kis)
```

### 1.3 방법 3: 대화형 설정 저장 후 사용

```python
from vmkis.helpers import save_config_interactive, create_client
from vmkis.simple import SimpleKIS

# 처음 한 번만: 대화형으로 설정 저장
config = save_config_interactive("configs/account_profiles.yaml")

kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)
```

---

## 2. 주요 메서드

시그니처는 `simple.py` 와 같습니다.

| 메서드 | 하는 일 |
|---|---|
| `get_price(symbol)` | `kis.stock(symbol).quote()` |
| `get_balance()` | `kis.account().balance()` |
| `place_order(symbol, qty, price=None)` | 항상 **매수**. `price` 없으면 시장가 |
| `cancel_order(order_obj)` | `order_obj.cancel()` — 주문 **객체**를 넘김 |

매도·정정·차트·호가는 `SimpleKIS` 에 없습니다. `kis.stock(symbol).sell(...)` 등을 쓰세요.

### 2.1 시세 조회

```python
price = simple.get_price("005930")  # 삼성전자
print(f"종목: {price.name}")
print(f"현재가: {price.price:,}원")
print(f"등락률: {price.rate}%")       # change_rate 가 아님
print(f"거래량: {price.volume:,}")

symbols = ["005930", "000660", "051910"]
prices = {sym: simple.get_price(sym) for sym in symbols}
for sym, quote in prices.items():
    print(f"{sym}: {quote.price:,}원")
```

### 2.2 잔고 조회

`deposits` 는 통화별 dict 입니다. 총자산은 `amount`(또는 `total`) 입니다.

```python
balance = simple.get_balance()
krw = balance.deposits["KRW"]
print(f"예수금: {krw.amount:,}원")
print(f"총자산: {balance.amount:,}원")
print(f"평가손익: {balance.profit:,}원")
print(f"수익률: {balance.profit_rate}%")
```

### 2.3 매수 주문

`side=` 인자는 없습니다. 매수만 됩니다.

```python
# 지정가 매수
order = simple.place_order("005930", qty=1, price=65000)
print(f"주문 번호: {order.number}")   # order_id 가 아님

# 시장가 매수 (price 생략)
order = simple.place_order("005930", qty=1)

# 매도 — SimpleKIS 밖
# kis.stock("005930").sell(qty=1, price=70000)
```

### 2.4 주문 취소

문자열 `order_id` 가 아니라 **`place_order` 가 돌려 준 주문 객체**를 넘깁니다.

```python
order = simple.place_order("005930", qty=1, price=65000)
simple.cancel_order(order)
```

---

## 3. 헬퍼 함수

### 3.1 설정 읽기

```python
from vmkis.config import load_kis_config

config = load_kis_config("configs/account_profiles.yaml")

print(config.default_account)         # "acc_paper1"
account = config.account()            # default_account 를 씁니다
print(account.hts_id, account.account, account.is_paper)
```

> `vmkis.helpers.load_config` 는 **없습니다.** 0.0.x 중간에 `vmkis.config` 로
>옮기면서 `load_kis_config` 로 바뀌었고, 반환값도 평평한 `dict` 가 아니라
> `KisConfig` 입니다. 사양은 [CONFIG_SCHEMA.md](./guidelines/CONFIG_SCHEMA.md).

대부분의 경우 이 함수를 직접 부를 일은 없습니다 — 3.3 의 `create_client` 가
안에서 부릅니다.

### 3.2 대화형 설정 저장 (보안)

```python
from vmkis.helpers import save_config_interactive

config = save_config_interactive("configs/account_profiles.yaml")
```

앱과 계좌를 **하나씩** 만듭니다. 둘 이상이 필요하면 만들어진 파일을 손으로
늘리세요.

**환경변수로 확인 단계 건너뛰기 (CI/CD용):**

```bash
export VMKIS_CONFIRM_SKIP=1
python your_script.py
```

### 3.3 자동 클라이언트 생성

```python
from vmkis.helpers import create_client
from vmkis.simple import SimpleKIS

kis = create_client("configs/account_profiles.yaml", keep_token=True)
simple = SimpleKIS(kis)
```

---

## 4. SimpleKIS vs VmKis 비교

| 기능 | SimpleKIS | VmKis (`stock` / `account`) |
|------|-----------|------------------------------|
| 학습곡선 | 낮음 | 중급+ |
| 메서드 | 4개 (시세·잔고·매수·취소) | 넓음 |
| WebSocket | 없음 | 있음 |
| 차트·호가 | 없음 | 있음 |
| 매도·정정 | 없음 | 있음 |

**언제 SimpleKIS를 쓸까?** 시세·잔고·단순 매수·취소만 필요할 때.
**언제 stock/account를 쓸까?** 매도·차트·호가·웹소켓·고급 계좌 조회.

---

## 5. 짧은 예제

### 5.1 시세와 잔고

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)

quote = simple.get_price("005930")
print(f"{quote.name}: {quote.price:,}원 ({quote.rate:+.2f}%)")

balance = simple.get_balance()
print(f"총자산: {balance.amount:,}원")
print(f"예수금(KRW): {balance.deposits['KRW'].amount:,}원")
```

### 5.2 조건부 매수

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)

quote = simple.get_price("005930")
if quote.price <= 65000:
    order = simple.place_order("005930", qty=1, price=65000)
    print(f"매수 주문: {order.number}")
else:
    print(f"현재가 {quote.price:,}원이 목표가 이상입니다.")
```

### 5.3 매수 후 취소

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

kis = create_client("configs/account_profiles.yaml")
simple = SimpleKIS(kis)

order = simple.place_order("005930", qty=1, price=65000)
simple.cancel_order(order)
```

---

## 6. 주의사항

### 6.1 실계좌 주문

```python
# paper=True (모의투자)
auth = KisAuth(..., paper=True)
kis = VmKis(None, auth)
simple = SimpleKIS(kis)
order = simple.place_order("005930", qty=1)  # 모의

# paper=False (실계좌) — 실제 주문
auth = KisAuth(..., paper=False)
kis = VmKis(auth)
simple = SimpleKIS(kis)
order = simple.place_order("005930", qty=1)
```

**테스트 프로세스:**

1. `paper=True`로 모의투자에서 전부 검증
2. `ALLOW_LIVE_TRADES=1` 환경변수 설정 필수
3. 실계좌에서 소액으로 테스트
4. 정상 작동 확인 후 본격 사용

### 6.2 보안 (설정 저장)

```python
# 나쁜 예: 코드에 비밀키
# 좋은 예: 파일에서 로드
from vmkis.helpers import create_client
kis = create_client("configs/account_profiles.yaml")

# 더 나은 예: 대화형 저장
from vmkis.helpers import save_config_interactive
config = save_config_interactive("configs/account_profiles.yaml")
```

### 6.3 에러 처리

```python
from vmkis import create_client
from vmkis.simple import SimpleKIS

try:
    kis = create_client("configs/account_profiles.yaml")
    simple = SimpleKIS(kis)
    price = simple.get_price("005930")
    print(f"현재가: {price.price:,}원")
except FileNotFoundError:
    print("configs/account_profiles.yaml 이 없습니다.")
except Exception as e:
    print(f"오류: {e}")
```

---

## 7. 다음 단계

- **VmKis로 업그레이드**: `kis.stock` / `kis.account` — 매도, 웹소켓, 차트, 호가
- **없는 TR**: [`fetch()`](./user/EXTENDING_API.md)

**예제:**

- `examples/01_basic/` — **VmKis** 현물 예제입니다. SimpleKIS 전용 파일은 없습니다.
  위 스니펫을 그대로 쓰면 `simple.py` 와 맞습니다.
