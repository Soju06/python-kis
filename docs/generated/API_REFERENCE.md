# API Reference

자동 생성된 API 레퍼런스 문서입니다.

---

## 목차

- [vmkis.client.auth](#vmkis-client-auth)
- [vmkis.helpers](#vmkis-helpers)
- [vmkis.kis](#vmkis-kis)
- [vmkis.public_types](#vmkis-public_types)
- [vmkis.simple](#vmkis-simple)

---

## vmkis.client.auth

### Classes

#### `KisAuth`

한국투자증권 OpenAPI 계좌 및 인증 정보

Examples:
    >>> auth = KisAuth(
    ...     # HTS 아이디  예) soju06
    ...     id="YOUR_HTS_ID",
    ...     # 앱 키  예) Pa0knAM6JLAjIa93Miajz7ykJIXXXXXXXXXX
    ...     appkey="YOUR_APP_KEY",
    ...     # 앱 시크릿 키  예) V9J3YGPE5q2ZRG5EgqnLHn7XqbJjzwXcNpvY . . .
    ...     secretkey="YOUR_APP_SECRET",
    ...     # 앱 키와 연결된 계좌번호  예) 00000000-01
    ...     account="00000000-01",
    ...     # 모의투자 여부
    ...     paper=False,
    ... )

    안전한 경로에 시크릿 키를 파일로 저장합니다.

    >>> auth.save("secret.json")

**Methods:**

- `key()`: 앱 키
- `account_number()`: 계좌번호
- `save()`: 계좌 및 인증 정보를 JSON 파일로 저장합니다.
- `load()`: JSON 파일에서 계좌 및 인증 정보를 불러옵니다.

### Functions

#### `key()`

앱 키

#### `account_number()`

계좌번호

#### `save()`

계좌 및 인증 정보를 JSON 파일로 저장합니다.

#### `load()`

JSON 파일에서 계좌 및 인증 정보를 불러옵니다.

---

## vmkis.helpers

### Functions

#### `create_client()`

설정 파일로부터 `VmKis` 클라이언트를 생성합니다.

모의투자 계좌면 `KisAuth` 를 `VmKis` 의 `paper_auth` 인자로 전달합니다.
모의도메인 전용 인증 정보를 실전 인증 정보로 잘못 다루는 것을 막기 위함입니다.

토큰 저장 경로는 설정이 정합니다 — 앱 이름에서 파생되므로 앱이 다르면 토큰
파일도 반드시 다릅니다. `keep_token=False` 를 주면 저장하지 않습니다.

Args:
    config_path: 설정 파일 경로
    keep_token: 토큰 저장 여부. 생략하면 설정이 정한 경로에 저장합니다
    account: 쓸 계좌 이름. 생략하면 `VMKIS_ACCOUNT`, 그다음 `default_account`

Returns:
    생성된 `VmKis` 클라이언트

Raises:
    ValueError: 설정이 스키마를 어긴 경우 (`docs/guidelines/CONFIG_SCHEMA.md`)

#### `save_config_interactive()`

대화형으로 설정 값을 입력받아 YAML로 저장합니다.

비밀키는 입력 시 화면에 표시하지 않으며, 파일을 쓰기 전에 확인을 받습니다.
환경변수 `VMKIS_CONFIRM_SKIP=1`을 설정하면 확인 절차를 건너뜁니다
(CI 스크립트용).

앱과 계좌를 하나씩만 만듭니다. 둘 이상이 필요하면 만들어진 파일을 손으로
늘리세요 — 대화형으로 N개를 받는 것은 템플릿을 고치는 것보다 번거롭습니다.

Args:
    path: 저장할 설정 파일 경로

Returns:
    저장된 설정 딕셔너리

Raises:
    SystemExit: 사용자가 쓰기를 취소한 경우

---

## vmkis.kis

### Classes

#### `VmKis`

한국투자증권 API

**Methods:**

- `paper()`: 모의도메인 여부
- `keep_token()`: API 접속 토큰 자동 저장 여부
- `base_url()`: REST 서버 주소. 설정에 재정의가 있으면 그것을, 없으면 기본값을 씁니다.
- `ws_url()`: 웹소켓 서버 주소. `base_url` 과 같은 규칙입니다.
- `request()`
- `fetch()`
- `call()`: 엔드포인트 스펙으로 API 를 호출합니다.
- `fetch_pages()`: 연속조회를 끝까지 따라가며 결과를 하나로 합칩니다.
- `token()`: 실전도메인 API 접속 토큰을 반환합니다.
- `token()`: API 접속 토큰을 설정합니다.
- `primary_token()`: API 접속 토큰을 반환합니다.
- `primary_token()`: API 접속 토큰을 설정합니다.
- `discard()`: API 접속 토큰을 폐기합니다.
- `primary()`: 기본 계좌 정보를 반환합니다.
- `websocket()`: 웹소켓 클라이언트를 반환합니다.
- `close()`: API 세션을 종료합니다.

### Functions

#### `paper()`

모의도메인 여부

#### `keep_token()`

API 접속 토큰 자동 저장 여부

#### `base_url()`

REST 서버 주소. 설정에 재정의가 있으면 그것을, 없으면 기본값을 씁니다.

벤더가 주소를 바꿔도 사용자가 설정만 고쳐 복구할 수 있게 하는 것이 목적입니다.
상수를 `from ... import` 로 가져오면 값이 복사되므로, 사용자가 `__env__` 를
고쳐도 이 모듈은 옛 값을 봅니다 — 그래서 재정의 경로가 필요합니다.

#### `ws_url()`

웹소켓 서버 주소. `base_url` 과 같은 규칙입니다.

#### `request()`

(No docstring)

#### `fetch()`

(No docstring)

#### `call()`

엔드포인트 스펙으로 API 를 호출합니다.

`fetch()` 위에 얹은 얇은 층입니다. 흩어져 있던 세 가지 규칙을 여기서만
처리합니다.

1. **실전/모의 TR ID 선택** — 예전에는 호출부마다
   `api="VTTC8434R" if self.paper else "TTTC8434R"` 를 적었습니다
2. **도메인 라우팅** — 모의 미지원 TR 은 실전으로 보냅니다.
   예전에는 `domain="live"` 을 손으로 붙였고, **빠뜨리면 모의 계정에서만
   터지는 버그**가 됐습니다
3. **커서 길이와 연속조회** — `page.to(100)` / `continuous=not page.is_first`

Args:
    endpoint: 엔드포인트 스펙
    page: 연속조회 커서. 주면 `endpoint.page_size` 로 길이를 맞추고
        `form` 뒤에 붙입니다. 첫 페이지가 아니면 `continuous=True`.

`fetch()` 의 나머지 인자는 `**kwargs` 로 그대로 넘어갑니다.

#### `fetch_pages()`

연속조회를 끝까지 따라가며 결과를 하나로 합칩니다.

예전에는 이 루프를 엔드포인트마다 각자 복사했습니다(이슈 #44 착수 시점
8곳). 골격이 전부 같고 **다른 것은 "어느 필드에 누적하는가" 한 줄뿐**
이었습니다. `continuous` / `is_last` / `next_page` 를 잘못 다루면
**무한 루프이거나 첫 페이지만 반환**하는데, 둘 다 조용히 틀립니다.

Args:
    response_type: 응답 객체를 만드는 **팩토리**. 인스턴스가 아닙니다
        (아래 참고).
    merge: `merge(첫_페이지, 다음_페이지)` — 첫 페이지에 누적합니다.
        예: `lambda first, more: first.stocks.extend(more.stocks)`
    continuous: `False` 면 첫 페이지만 가져옵니다.
    max_pages: 상한. 서버가 `is_last` 를 끝내 주지 않아도 여기서 멈춥니다.

Raises:
    TypeError: `response_type` 에 팩토리가 아니라 인스턴스를 준 경우
    RuntimeError: `max_pages` 를 넘긴 경우

**왜 팩토리인가.** `KisObject.transform_` 은 인스턴스를 받으면 **그
인스턴스에 그대로 파싱**합니다. 하나를 돌려 쓰면 모든 페이지가 같은
객체가 되고, `merge(first, result)` 가 자기 자신을 이어붙여 결과가
불어납니다. 예전 루프들이 매 반복마다 응답 객체를 새로 만든 이유가
이것입니다.

#### `token()`

실전도메인 API 접속 토큰을 반환합니다.

#### `token()`

API 접속 토큰을 설정합니다.

#### `primary_token()`

API 접속 토큰을 반환합니다.

#### `primary_token()`

API 접속 토큰을 설정합니다.

#### `discard()`

API 접속 토큰을 폐기합니다.

#### `primary()`

기본 계좌 정보를 반환합니다.

Raises:
    ValueError: 기본 계좌 정보가 없을 경우

#### `websocket()`

웹소켓 클라이언트를 반환합니다.

#### `close()`

API 세션을 종료합니다.

---

## vmkis.public_types

---

## vmkis.simple

### Classes

#### `SimpleKIS`

A very small facade for common user flows.

This class intentionally implements a tiny, beginner-friendly API that
delegates to a `VmKis` instance.

**Methods:**

- `from_client()`
- `get_price()`: Return the quote for `symbol`.
- `get_balance()`: Return account balance object.
- `place_order()`: Place a basic order. If `price` is None, market order is used.
- `cancel_order()`: Cancel an existing order object (delegates to order.cancel()).

### Functions

#### `from_client()`

(No docstring)

#### `get_price()`

Return the quote for `symbol`.

#### `get_balance()`

Return account balance object.

#### `place_order()`

Place a basic order. If `price` is None, market order is used.

#### `cancel_order()`

Cancel an existing order object (delegates to order.cancel()).

---
