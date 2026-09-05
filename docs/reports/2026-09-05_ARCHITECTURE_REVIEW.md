# 아키텍트 검토 — 문서, 코드 구조, 소프트웨어 아키텍처

**작성일**: 2026-09-05
**관점**: 소프트웨어 아키텍트. 전용 architect 서브에이전트는 이 환경에 없어
`ARCHITECTURE.md` §1.1 과 코드 트리를 대조했습니다.
**범위**: 살아 있는 문서와 `src/vmkis/`. `#30` 게이트는 당기지 않습니다.
**하지 않은 것**: 커버리지·테스트 개수·PyPI 버전을 여기에 박지 않습니다.

이 문서는 동결 분석입니다. 작업 목록은 GitHub Issues 입니다.

---

## 요약

구조의 핵은 건강합니다. `VmKis` 허브, scope → adapter → api, 의도적 순환
두 쌍, import-linter 가 해소된 간선을 다시 못 만들게 합니다. 공개 표면은
사용자(`create_client` · `kis.stock` / `kis.account`)와 개발자(`fetch()` ·
EXTENDING_API)로 나뉘어 있고, codegen 파일럿은 휠 밖입니다 (`#100` B).

약한 곳은 코드가 아니라 **문서가 두 개의 그림을 동시에 그리는 것**입니다.
§1.1 은 "계층이 아니다"인데, 그 아래 데이터 흐름도는 다시 Scope → Adapter →
Client 하향 계층입니다. `event → api` 는 같은 절에서 "미판정"과 "의도적"이
함께 있습니다. 사용자 온보딩은 JSON `KisAuth` 와 YAML `create_client` 가
가이드마다 갈라집니다 — `#141` 은 둘 다 유효하다고 적었으나 아키텍처 문서는
그 선택을 설계로 말하지 않습니다.

지금 고칠 일은 폴백 제거(`#30`)가 아닙니다. **ARCHITECTURE 를 코드와 한
그림으로 맞추고**, 살아 있는 가이드에 남은 호출 거짓말(`chart` 인자,
`VmKis("config.yaml")`, `virtual_secret.json`)을 지우는 일입니다.

---

## 1. 구조 — 코드가 지키는 것

### 허브

`src/vmkis/kis.py` 가 조립점입니다. scope 의 `stock` / `account` 와
`trading_hours` 를 클래스 본문 import 로 붙입니다. 스포크는 허브를
`TYPE_CHECKING` 으로만 봅니다. 모듈 레벨 `import vmkis.kis` 는 금지이고
기계가 지킵니다 (`[tool.importlinter]`, `tests/unit/test_import_contracts.py`).

### 그룹

| 그룹 | 역할 |
|---|---|
| `scope/` | 사용자 진입. `kis.stock` / `kis.account` |
| `adapter/` | Mixin. quote · order · websocket |
| `api/` | TR 구현과 응답 타입 |
| `client/` | HTTP · 웹소켓 · 토큰 · 엔드포인트 |
| `responses/` | 동적 응답 변환. client 타입 위에 성립 |
| `event/` | 구독 티켓 · 필터 |
| `utils/` | 상위 그룹을 import 하지 않음 (`#18`) |
| `config.py` · `helpers.py` | YAML → `KisAuth` 번역 |
| `simple.py` | `VmKis` 위 얇은 파사드 (시세·잔고·매수·취소) |
| `public_types.py` | 루트가 재export 하는 별칭 |
| `types.py` | 고급 경로. 루트 deprecated `__getattr__` |

`api ↔ adapter`, `api ↔ event`, `responses → client` 는 의도적입니다.
`client → api` 와 `utils → client` 는 해소됐고 계약이 감시합니다.

`event → api` 는 `#63` 에서 의도적으로 판정했습니다. `MARKET_TYPE` 을
하위 계층으로 내리는 일만 판정을 뒤집습니다. 그것은 `#30` · `#34` 와
함께 갈 공개 API 정리이지, 지금 열 일이 아닙니다.

### 공개 표면

루트 `__all__` 은 `ARCHITECTURE.md` 에 적힌 목록과
`src/vmkis/__init__.py` 가 같습니다. `public_types.py` 는 `MarketType` 을
더 들고 있고 루트는 재export 하지 않습니다. 문서 스니펫은 그 이름을
빠뜨리고 "9개"라고 적습니다 — 코드와 다릅니다.

`SimpleKIS` 는 Tutorial 표면이 아닙니다. `get_price` / `get_balance` /
`place_order`(매수) / `cancel_order` 만 있습니다. 중급 예제가 이것을
써도 `stock.chart()` · `orderbook()` 을 커버하지 않습니다 (`#136`).

`fetch()` 와 `scripts/codegen/pilot/` 은 휠 밖입니다. 새 TR 은 이슈 한 건
= TR 하나, 본문 첫 줄 `TR: <id>` (`#100` B). `create_client` 가 돌려 주는
것은 `VmKis` 이지 `SimpleKIS` 가 아닙니다. 예외는 `from vmkis.exceptions
import *` 로 루트에 올라오나 `__all__` 에는 없습니다 — 암묵적 공개 표면입니다.

### 구조 냄새 (지금 쪼개지 말 것)

스포크 디렉터리는 다이어그램과 맞습니다. 다이어그램에 없는 것은 루트의
파사드(`helpers`, `simple`, `config`, `types`, `exceptions`)입니다.
의도적입니다.

커지는 파일은 `kis.py` 만이 아닙니다. `api/account/order.py` 와
`api/account/balance.py` 가 응답 타입·엔드포인트·mixin 기반을 한 모듈에
둡니다. 의도적 `api ↔ adapter` 순환의 한쪽이 여기입니다. 지금 파일을
가르면 순환만 더 드러납니다. 허브를 계층으로 되돌리는 리팩터와 같이
보지 마십시오.

`event/__init__.py` 만 핸들러 타입을 재export 합니다. 다른 스포크
`__init__.py` 는 `#64` 이후 빈 표식입니다. `types.py` 는 `VmKis` 를
모듈 레벨로 import 합니다 — 루트 `__getattr__` 이 늦게 로드하므로
불변식 1을 피합니다. 일찍 import 하면 깨집니다.

---

## 2. 문서 — 두 그림

### 정본이 서로 모순

`ARCHITECTURE.md` §1.1 은 런타임 역방향 import 가 있어서 하향 계층이
아니라고 합니다. 같은 파일의 「전체 데이터 흐름도」는 Scope Layer →
Adapter Layer → VmKis Client 로 다시 그립니다. 다이어그램의
`on_price()` 는 사용자 API 가 아닙니다. 사용자는 `stock.on("price", …)`
입니다.

같은 §1.1 170행: `event → api` 는 아직 판정되지 않았다.
201행: 2026-08-29 에 의도적으로 판정했다 (`#63`).
`pyproject.toml` 주석도 170행과 같은 옛 문장을 들고 있습니다.

### 온보딩이 두 갈래

| 경로 | 가르치는 곳 | 코드 |
|---|---|---|
| `KisAuth.save` → `VmKis("secret.json")` | USER_GUIDE, EXTENDING_API, ARCHITECTURE 예제 | JSON. `KisAuth.load` |
| `create_client` + `account_profiles.yaml` | QUICKSTART, examples, CONFIG_SCHEMA | YAML → helpers 가 `KisAuth` 로 번역 |

`#141` 은 둘 다 유효하다고 했습니다. 아키텍처 문서는 그 이중 경로를
설계로 적지 않습니다. `MIGRATION_GUIDE` 와 `API_STABILITY_POLICY` 는 여전히
`VmKis("config.yaml")` 을 보여 줍니다. `VmKis` 는 JSON 만 읽습니다.

### 살아 있는 가이드에 남은 거짓말

`#139` 가 Tutorial 이름(`profits`, `daily_orders`, `orderable`,
`trading_hours(market)`)은 맞췄습니다. 아직 실행하면 깨지는 조각:

- USER_GUIDE 차트: `period="D"` / `end_date=` — 코드는 `period="day"` 와 `end`
- FAQ 차트: `chart("D")` — timex 는 숫자로 시작
- DEVELOPER_GUIDE: `virtual_secret.json` — README 만 `#141` 이 고침
- `API_STABILITY_POLICY`: `vmkis._internal` — 그런 패키지가 없습니다

Wiki 는 포인터입니다 (`#145`). README 는 업스트림 위키 스냅샷만 가리키며
이 배포판 Docs 로 읽히지 않습니다.

---

## 3. 리스크 (우선순위)

1. **ARCHITECTURE 가 두 그림을 가르친다.** 다음 기여자가 하향 계층을
   복원하거나, `event → api` 를 미판정으로 보고 계약을 넣으려 합니다.
2. **온보딩 분기.** QUICKSTART 사용자는 YAML, USER_GUIDE 사용자는 JSON.
   둘을 섞으면 `VmKis("….yaml")` 로 죽습니다.
3. **차트 스니펫.** `#139` 범위 밖이라 이름만 맞고 인자가 틀립니다.
4. **허브와 `api/account/*` 가 커진다.** 허브인 것은 맞습니다.
   "계층을 되살리는" 리팩터가 유혹입니다. 불변식 1번을 깨면 import
   단계에서 죽습니다. `types.py` 의 허브 import 도 늦은 로드에만
   안전합니다.
5. **`#30` 을 지금 열면** 폴백 제거와 문서 정리가 한 이슈에 섞입니다.
   게이트는 `tests/unit/test_release_gate.py` 의 날짜입니다. 당기지
   않습니다.

---

## 4. 권고 — 하지 말 것 / 해도 되는 것

하지 말 것:

- 위키에 Tutorial 본문이나 상세 목차를 다시 쓰기 (`#145`)
- 현물 밖 TR 을 전용 메서드로 넣기 (`#100` B)
- `#33`–`#36` 의 `blocked` 를 떼기
- ARCHITECTURE 에 커버리지 목표를 "현재 값"처럼 적기

해도 되는 것 (후속 이슈, 이 보고서가 열지 않음):

- ARCHITECTURE 흐름도를 §1.1 그림에 맞추고, 170행과
  `pyproject.toml` 주석의 "미판정"을 지운다
- `public_types` 스니펫을 코드와 같게
- USER_GUIDE/FAQ 차트 인자, DEVELOPER_GUIDE `virtual_secret`,
  `VmKis("config.yaml")` 를 고친다
- ARCHITECTURE 또는 USER_GUIDE 첫 인증 절에 "JSON 과 YAML 둘 다
  유효, `VmKis` 경로는 JSON" 한 줄을 넣는다

---

## 5. 판정

이 라이브러리는 **허브-스포크 + 얇은 사용자 파사드 + `fetch()` 탈출구**
로 이미 읽힙니다. 아키텍처 부채의 대부분은 순환을 더 만드는 일이 아니라
문서가 옛 계층 이야기와 새 불변식을 한 파일에 쌓아 둔 일입니다.

코드 구조를 크게 바꾸지 마십시오. 문서를 한 그림으로 맞추십시오.
