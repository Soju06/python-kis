# 설정 파일 스키마

**작성일**: 2026-08-29
**상태**: 구현됨 (#75)
**범위**: `vmkis.config.load_kis_config` 가 읽는 YAML 의 구조와 검증 규칙

---

## 이 문서가 정하는 것

사용자가 손으로 쓰는 설정 파일의 **모양**과, 그것을 읽을 때 **무엇을 거부하는가**.

정하지 않는 것: 주문 흐름, 전략, 자금 배분. 이 라이브러리는 **KIS API 클라이언트**이지
운용 시스템이 아닙니다.

---

## 왜 이렇게 작은가

운용 시스템의 설정 파일을 참고해 설계했지만, 그쪽 항목의 대부분은 옮기지
않았습니다. 자금 배분 정책(그룹·비중·노출), 원장 표시용 이름표, 레거시 브리지용
이중 명명, 다중 브로커 — 전부 **이 라이브러리가 읽지 않는 값**입니다.

**설정 항목을 추가할 때는 "이 라이브러리가 그 값으로 무엇을 하는가"에 답해야 합니다.**
답이 "애플리케이션이 읽는다"이면 여기 두지 않습니다. 그것이 이 파일에 있으면
라이브러리가 검증할 수도, 쓸 수도 없는 채로 스키마만 넓어집니다.

---

## 구조

```yaml
version: 1

# 토큰 발급 단위. KIS 토큰은 app_key 단위로 발급되므로,
# 같은 앱키를 쓰는 계좌 N개가 토큰 1개를 공유합니다.
apps:
  app_live1:
    mode: "live"                 # live | paper — 생략 불가
    hts_id: "YOUR_HTS_ID"
    app_key: "YOUR_LIVE_KEY"     # 36자
    app_secret: "YOUR_LIVE_SECRET"  # 180자
  app_paper1:
    mode: "paper"
    hts_id: "YOUR_HTS_ID"
    app_key: "YOUR_PAPER_KEY"
    app_secret: "YOUR_PAPER_SECRET"

# 계좌. 어느 앱으로 접속할지만 가리킵니다.
accounts:
  acc_live1:
    app: "app_live1"
    account_no: "00000000"       # 종합계좌번호 8자리
    product_code: "01"           # 01 종합 / 22 개인연금 / 29 IRP
  acc_paper1:
    app: "app_paper1"
    account_no: "00000000"
    product_code: "01"

default_account: "acc_paper1"
```

> ### R10 — 실전 계좌가 최소 하나 있어야 합니다
>
> **모의투자만 할 때도 그렇습니다.** 시세 TR 이 모의도메인에 없어서, 모의
> 계좌로 시세를 조회해도 요청은 실전 도메인으로 나가고 그때 실전 앱키와 실전
> 토큰을 씁니다 (`src/vmkis/client/endpoint.py` 의 `tr_paper` 설명).
>
> 모의 앱만 적은 설정으로 `create_client()` 를 부르면 무엇을 추가해야 하는지
> 알려주며 멈춥니다. ([#87](https://github.com/visualmoney/vm-stock-kis/issues/87))

> **문자열은 전부 따옴표로 감쌉니다.** `version` 만 따옴표가 없습니다 — 그것만
> 실제로 정수입니다. 아래 [따옴표](#따옴표) 참고.

블록은 셋뿐입니다. `apps` 를 계좌와 분리하는 근거는 **토큰 수명** 하나입니다 —
그것이 KIS 의 실제 제약이라 라이브러리가 알아야 합니다.

---

## 필드

### 최상위

| 키 | 필수 | 의미 |
|---|---|---|
| `version` | ✅ | 스키마 판. 현재 `1`. 모르는 값이면 거부 |
| `apps` | ✅ | 앱 이름 → 앱 블록 |
| `accounts` | ✅ | 계좌 이름 → 계좌 블록 |
| `default_account` | 계좌가 2개 이상이면 ✅ | `accounts` 의 키 하나 |
| `token_dir` | | 토큰 저장 폴더. 기본은 **설정 파일과 같은 폴더의 `token/`** |
| `user_agent` | | HTTP 요청 헤더. 기본 `VmKis/<version>` |
| `endpoints` | | 서버 주소 재정의. 생략하면 라이브러리 기본값 |

> `default_account` 를 `accounts` **밖에** 둡니다. 안에 두면 `default_account` 라는
> 이름의 계좌를 만들 수 없고, 검증기가 그 키만 특례 처리해야 합니다.

### `apps.<이름>`

| 키 | 필수 | 의미 |
|---|---|---|
| `mode` | ✅ | `live` \| `paper`. **생략을 실전으로 해석하지 않습니다** |
| `app_key` | ✅ | 36자 |
| `app_secret` | ✅ | 180자 |
| `hts_id` | ✅ | KIS 가 요구합니다 |

### `accounts.<이름>`

| 키 | 필수 | 의미 |
|---|---|---|
| `app` | ✅ | `apps` 의 키 하나 |
| `account_no` | ✅ | 8자리 |
| `product_code` | ✅ | 2자리 |

---

## 따옴표

**문자열 값은 전부 따옴표로 감쌉니다.** `version` 만 예외입니다 — 그것만 정수입니다.

이유는 스타일이 아닙니다. YAML 은 따옴표 없는 값을 **추측해서 변환**합니다.

```console
account_no: 00000000    ->  0      (int)      ← 계좌번호가 사라집니다
product_code: 01        ->  1      (int)
mode: paper             ->  'paper' (str)     ← 이건 안전합니다
```

`mode` 는 따옴표가 있으나 없으나 같은 문자열입니다. 그런데 문서에서 `mode: paper`
를 본 사용자는 *"따옴표는 선택"* 으로 읽고 `account_no` 에도 안 씁니다. 그 순간
계좌번호가 **조용히 `0`** 이 됩니다.

> 안전한 값 하나를 따옴표 없이 적는 대가로, 위험한 값에서 따옴표가 빠집니다.
> 그래서 전부 씌웁니다.

YAML 1.1 의 `no`/`off`/`n` 이 `False` 로, `on`/`yes` 가 `True` 로 바뀌는 것도 같은
성질입니다 — 이 스키마에는 해당 값이 없지만, 규칙을 예외 없이 두면 신경 쓸 일이
없습니다.

---

## 토큰 경로

**기본값은 설정 파일이 있는 폴더의 `token/` 입니다.** cwd 기준이 아닙니다.

```text
configs/
├── account_profiles.yaml
└── token/
    ├── app_paper1.json
    └── app_live1.json
```

파일명은 **앱 이름에서 만듭니다**(`token/<app>.json`). 사용자가 앱마다 경로를 직접
적게 하면 안 됩니다 — 두 앱이 같은 경로를 가리켜도 아무도 못 막고, 그때 증상은
"가끔 인증이 풀린다"입니다.

`token_dir` 로 폴더만 바꿀 수 있습니다. 상대경로면 **설정 파일 기준**입니다.

> cwd 기준이면 다른 디렉터리에서 실행할 때마다 새 토큰 파일이 생겨 매번 재발급하거나,
> 엉뚱한 곳에 토큰이 쌓입니다.

---

## 검증 규칙

**모르는 것은 거부합니다.** 조용히 무시하면 오타가 사고가 됩니다 — `virtaul: true` 가
기본값 `False`(실전)로 떨어지던 것이 실제로 있었습니다 (#69).

| # | 규칙 | 위반 시 |
|---|---|---|
| R1 | `version` 이 없거나 아는 값이 아니면 거부 | `ValueError` |
| R2 | 블록에 **모르는 키**가 있으면 거부 | `ValueError` — 어느 블록의 어느 키인지 표시 |
| R3 | 필수 키가 없으면 거부 | `ValueError` |
| R4 | `mode` 가 `live`/`paper` 가 아니면 거부. **생략도 거부** | `ValueError` |
| R5 | `accounts.*.app` 이 `apps` 에 없으면 거부 | `ValueError` |
| R6 | 어떤 앱도 참조하지 않는 `apps` 항목이 있으면 거부 | `ValueError` — 고아 블록이 조용히 남지 않게 |
| R7 | 계좌가 2개 이상인데 `default_account` 가 없으면 거부 | `ValueError` |
| R8 | `default_account` 가 `accounts` 에 없으면 거부 | `ValueError` |
| R9 | 문자열이어야 할 값이 `int`/`bool` 로 들어오면 거부 | `ValueError` — **따옴표를 씌우라고 말해줍니다** |

R9 가 없으면 `account_no: 00000000` 이 정수 `0` 으로 조용히 들어옵니다. YAML 이
추측 변환을 하기 때문이고, 이건 사용자의 오타가 아니라 **형식의 함정**입니다.
오류 메시지가 원인을 바로 말해야 합니다.

```text
accounts.acc_paper1.account_no 가 정수 0 입니다. 계좌번호는 문자열이어야 합니다 —
따옴표를 씌우세요: account_no: "00000000"
```

R5·R6 이 **양방향**인 이유: 한쪽만 검사하면 오타로 만든 블록이 고아로 남습니다.
초안에서 실제로 `default_account: "kis_paper_1"` 이 그 파일에 없는 계좌를 가리키고
있었습니다.

---

## `user_agent`

브라우저 User-Agent 를 그대로 넣어야 할 때가 있어 열어 둡니다. **최상위**입니다 —
클라이언트 전체에 걸리는 값이지 계좌·앱별 값이 아닙니다.

```yaml
user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ..."
```

> 값을 따옴표 **한 겹**으로만 감싸세요. `"'Mozilla/5.0 ...'"` 처럼 이중으로 쓰면
> YAML 이 작은따옴표를 값에 포함시켜 헤더에 그대로 실려 나갑니다.

생략하면 `VmKis/<version>` 입니다 (`src/vmkis/__env__.py`). 지정한 값은
세션 헤더에 그대로 들어갑니다 (`src/vmkis/kis.py`).

---

## `endpoints` — 벤더가 주소를 바꿨을 때의 탈출구

```yaml
endpoints:            # 전부 선택. 적은 것만 덮어씁니다
  live:
    base_url: "https://openapi.koreainvestment.com:9443"
    ws_url:   "ws://ops.koreainvestment.com:21000"
  paper:
    base_url: "https://openapivts.koreainvestment.com:29443"
    ws_url:   "ws://ops.koreainvestment.com:31000"
```

`mode` 로 키를 잡습니다 — 같은 모드의 앱들은 어차피 같은 주소를 씁니다. **부분
지정을 허용합니다.** 벤더가 웹소켓 포트만 바꾸는 일이 흔해서, `paper.ws_url`
하나만 적고 나머지는 기본값을 쓸 수 있어야 합니다.

### 왜 설정 항목인가

이 문서는 "라이브러리가 그 값으로 무엇을 하는가"에 답하지 못하는 항목을 넣지
않는다고 적었습니다. 이건 답합니다 — **접속할 주소**입니다.

넣는 진짜 이유는 스테이징 서버가 아니라 **벤더 주소 변경 시 자력 복구**입니다.
지금 구조에서는 사용자가 손을 쓸 수 없습니다.

```console
$ python -c "import vmkis.__env__ as env, vmkis.kis as k; \
             env.LIVE_DOMAIN='https://patched.example.com'; print(k.LIVE_DOMAIN)"
https://openapi.koreainvestment.com:9443
```

`from vmkis.__env__ import LIVE_DOMAIN` 이 **값을 복사**하므로 `__env__` 를 고쳐도
소비 모듈은 옛 값을 봅니다. 모듈마다(`vmkis.kis`, `vmkis.client.websocket`) 따로
패치해야 하는데 문서에 없고, 나중에 다른 모듈이 그 상수를 import 하면 또 깨집니다.

남는 수단은 **릴리스를 기다리는 것**뿐입니다. 장중이면 그날은 끝입니다.

### 구현 메모

소비 지점 2곳이 이미 객체를 들고 있어 새 배선이 필요 없습니다 —
`kis.py` 는 `self`, `websocket.py` 는 `self.kis`
(`KisWebsocketClient.kis: "VmKis"`).

---

## 하위 호환은 없습니다

옛 형식(`default:` + `configs:` + `virtual: true`)은 **지원하지 않습니다.** 폴백도
자동 변환도 넣지 않습니다. 사용자가 사실상 0명이고 `0.0.1` 이 2026-08-28 첫
배포라, 지금이 깨기 가장 싼 시점입니다 (#55 와 같은 근거).

다만 **조용히 깨지지는 않습니다.** 옛 파일에는 `version` 키가 없으므로 R1 이
먼저 걸립니다.

```text
<설정 파일 경로> 에 `version` 이 없습니다. 이 파일은 0.0.x 형식으로 보입니다 —
지원하지 않습니다. template_account_profiles.yaml 을 참고해 다시 작성하세요.
```

실제 메시지는 읽은 파일 경로를 앞에 붙입니다 (`src/vmkis/config.py` 의 R1).
`config.yaml` 이라는 이름은 메시지에 없습니다.

변환 스크립트를 만들지 않는 이유도 같습니다. 옛 형식은 계좌 1개·앱 1개를 평평하게
적은 것이라 손으로 옮기는 편이 빠르고, 변환기는 그 자체로 유지보수 대상이 됩니다.

---

## 파일 배치

```text
configs/
├── template_account_profiles.yaml   # 저장소가 배포. 유일하게 추적됩니다
├── account_profiles.yaml            # 사용자가 채우는 것. 무시됨
└── token/                           # 토큰. 무시됨
```

템플릿도 `configs/` 안에 둡니다. 복사가 같은 폴더 안에서 끝나고, 첫 클론에
`configs/` 가 이미 존재하며, **토큰 기본 경로가 자동으로 무시 대상**이 됩니다
(토큰 폴더는 설정 파일 기준이라 템플릿이 저장소 루트에 있으면 토큰이 루트에
떨어지고 그건 무시되지 않습니다).

```gitignore
configs/*
!configs/template_account_profiles.yaml
```

> `configs/` 가 아니라 **`configs/*`** 입니다. 디렉터리째 제외하면 git 이 그 안으로
> 내려가지 않아 `!` 예외가 통하지 않습니다. 실측으로 확인한 동작입니다.

---

## 정하지 않은 것

- **환경변수 간접 참조** (`app_key_env`) — CI·컨테이너용. 필요가 확인되면 그때
  넣습니다. 지금은 YAML 을 시크릿에서 써 내려도 됩니다
- **다중 브로커** — 넣지 않습니다. KIS 전용 라이브러리입니다

> 엔드포인트 재정의는 여기 있었다가 `endpoints` 로 **들어왔습니다.** 처음에는
> "스테이징 서버가 없으니 쓸 사람이 없다"고 판단했는데, 사용 사례를 잘못
> 상정한 것이었습니다. 실제 사례는 **벤더가 주소를 바꿨을 때의 자력 복구**이고,
> 그때 사용자에게 남는 수단이 없다는 것을 확인해 넣었습니다.

---

## 관련

- 구현: `src/vmkis/config.py` (규칙 번호가 그대로 대응합니다)
- 진입점: `vmkis.create_client`
- #69 프로필 검증 (`helpers.py` `_validate_profile`) — 이 스키마의 전신
- [API_STABILITY_POLICY.md](./API_STABILITY_POLICY.md)
