# 변경 이력

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) 형식을 따르며
[유의적 버전](https://semver.org/lang/ko/)을 지킵니다.

버전은 git 태그에서 만들어집니다. [VERSIONING.md](./docs/developer/VERSIONING.md) 참고.

## [미출시]

<!-- 다음 변경을 여기 적으세요. 비어 있어도 절이 남아 있어야 합니다 —
     자리가 없으면 릴리스 때 커밋을 훑게 되고, 훑으면 빠집니다.
     0.1.0 에서 설정 스키마 Breaking 두 건이 실제로 그렇게 빠져 있었습니다. -->

### 추가

### 수정

---

## [1.0.0] — 2026-09-05

### 변경 (Breaking)

- `vmkis.client.exceptions.KisNotFoundError` 별칭을 제거합니다. HTTP 404 는
  `KisHTTPNotFoundError`, 조회 결과 없음은 `vmkis.exceptions.KisNotFoundError`
  만 씁니다 (#164)

### 수정

- `SIMPLEKIS_GUIDE` 를 `simple.py` 시그니처·필드명에 맞춥니다 (#163)
- 0.3.0 Breaking·Stable 내러티브와 SemVer 한 줄을 안정성·마이그레이션 문서에 맞춥니다 (#164)
- 모의 잔고 `OPSQ2000` leftover 를 예제 README 에 안내합니다 (#164)
- `PYPI_RELEASE` 예시를 0.3.0 게시 이후로 고칩니다 (#164)
- README·EXTENDING_API 에 `#100` B(현물 · `fetch()` · 전량 codegen 없음)를 재고지합니다 (#164)

---

## [0.3.0] — 2026-09-05

### 변경 (Breaking)

- `vmkis.PyKis` 별칭, `~/.pykis` 작업공간 폴백, `PYKIS_*` 환경변수 폴백을 제거합니다 (#33)
- 루트에서 내부 타입을 가져오는 deprecated 경로를 제거합니다 (#34)

### 추가

- 예제 동작 겉면을 단위 검사로 고정합니다 (#154)
- Tutorial 목차 중 빠져 있던 초급 예제를 넣었습니다 (#140)

### 수정

- `Development Status` 를 `5 - Production/Stable` 로 올립니다 (#35)
- Breaking 절과 지원 기간 정책을 문서에 맞춥니다 (#36)
- 예제에서 초·중·고 폴더를 접고 `01_basic` 만 남깁니다 (#155)
- `keep_token` 이 앱 이름 json 파일이면 그 자리에 `mkdir` 하지 않습니다 (#157)
- 예제 연기가 주석의 `YOUR_HTS_ID` 만으로 채운 설정을 skip 하지 않습니다 (#157)
- 예제 통합 연기가 추적 템플릿을 `--config` 로 넘기지 않습니다 (#154)
- README 가 업스트림 버전을 이 배포판 태그처럼 읽히게 하던 문장을 고쳤습니다 (#135)
- examples/README 바닥의 고정 버전·날짜를 지웠습니다 (#136)
- USER_GUIDE·FAQ 호출을 업스트림 Tutorial 이름에 맞췄습니다 (#139)
- README 의 `virtual_secret.json` 과 미정의 `hynix` 를 고쳤습니다 (#141)
- README 에 붙여 두던 업스트림 Changelog 항목을 링크로 돌렸습니다 (#143)

---

## [0.2.0] — 2026-09-05

### 추가

- Python 3.14 를 분류기와 CI 끝단에 올렸습니다 (#127)
- 서버에서 발급한 토큰을 로컬로 복사하는 예제 스크립트를 둡니다 (#121)
- 시세 재배포 금지를 사용자 문서에 적었습니다 (#96)

codegen 전량 이관은 이 버전에 없습니다 (#100).

### 수정

- 튜토리얼이 거부되는 평면 설정 스키마를 가르치지 않습니다 (#111)
- 살아 있는 문서의 없는 `config.yaml` 안내를 고쳤습니다 (#95, #112)

---

## [0.1.0] — 2026-08-30

### 변경 (Breaking)

- **설정 파일이 3블록 스키마로 바뀌었습니다 — 하위 호환 없음.** (#75)

  ```yaml
  version: 1
  apps: # 토큰 발급 단위 (KIS 토큰은 app_key 단위)
    app_live1: { mode: "live", hts_id: ..., app_key: ..., app_secret: ... }
    app_paper1: { mode: "paper", ... }
  accounts: # 어느 앱으로 접속할지만 가리킵니다
    acc_live1: { app: "app_live1", account_no: "00000000", product_code: "01" }
    acc_paper1: { app: "app_paper1", ... }
  default_account: "acc_paper1"
  ```

  옛 형식(`default:` + `configs:` + `virtual: true`)은 **읽지 않습니다.**
  `apps` 를 계좌와 분리한 근거는 **토큰 수명 하나**입니다 — 같은 앱키를 쓰는
  계좌 N개가 토큰 1개를 공유하는 것이 KIS 의 실제 제약입니다.

  토큰 파일 경로는 **앱 이름에서 파생**됩니다. 직접 적지 않습니다 — 두 앱이
  같은 파일을 가리키면 "가끔 인증이 풀립니다"가 됩니다.

  사양: [`docs/guidelines/CONFIG_SCHEMA.md`](./docs/guidelines/CONFIG_SCHEMA.md)

- **`vmkis.helpers.load_config` 를 제거했습니다.** (#69, #75)
  `vmkis.config.load_kis_config` 가 대신하며 `dict` 가 아니라 `KisConfig` 를
  돌려줍니다.

  같은 함수가 **5벌**이었고 **4벌이 `examples/`** 였습니다. 그중 하나가
  `cfg.get("virtual", False)` 였는데 **기본값이 실전**이라, `virtaul: true`
  오타 하나로 모의투자 의도가 **경고 없이 실전 주문**이 됐습니다.

  이제 모르는 키·필수 키 누락·모드 키 누락이 전부 예외입니다. **기본값을
  두지 않습니다.**

- **모의 계좌만 적은 설정은 더 이상 유효하지 않습니다.** (#87)

  시세 TR 이 모의도메인에 없어서 모의 계좌로 조회해도 요청이 실전 도메인으로
  나갑니다. 그래서 실전 앱이 설정에 있어야 합니다
  (`CONFIG_SCHEMA.md` 의 R10). `create_client()` 가 무엇을 추가해야 하는지
  알려주며 멈춥니다.

  > 참고로 `create_client` 는 **0.0.1 에서도 모의 계좌면 항상 실패**했습니다
  > (`ValueError: id를 입력해야 합니다`). 그때는 원인을 알 수 없는 메시지였고,
  > 템플릿의 기본 계좌가 모의라 정규 경로가 끝까지 가지 않았습니다.

- **`real`/`virtual` 어휘를 `live`/`paper` 로 바꿨습니다.** (#70, 결정은 #55)

  `real` 은 한국투자증권의 표기가 아닙니다 — KIS 는 **실전/모의**라고 쓰고,
  `real`/`virtual` 은 이 라이브러리가 고른 번역이었습니다. 영어권 표준은
  `paper trading` 이고 영어 문서가 이미 그 말을 쓰고 있었습니다.

  **별칭도 경고도 남기지 않았습니다.** 옛 이름은 `AttributeError` 또는
  `TypeError` 로 즉시 실패합니다. 0.0.1 이 2026-08-28 첫 배포라 지금이 가장
  싼 시점이고, 호환 폴백을 지우려고 열려 있는 이슈(#33·#34)에 한 줄을 더하지
  않기 위해서입니다.

  | 이전 | 이후 |
  |---|---|
  | `KisAuth(virtual=True)` | `KisAuth(paper=True)` |
  | `VmKis(virtual_auth=...)` | `VmKis(paper_auth=...)` |
  | `VmKis(virtual_id=, virtual_appkey=, virtual_secretkey=, virtual_token=)` | `VmKis(paper_id=, paper_appkey=, paper_secretkey=, paper_token=)` |
  | `kis.virtual` | `kis.paper` |
  | `kis.virtual_appkey` | `kis.paper_appkey` |
  | `domain="real"` / `domain="virtual"` | `domain="live"` / `domain="paper"` |
  | `Literal["real", "virtual"]` | `Literal["live", "paper"]` |
  | `KisEndpoint(tr_real=, tr_virtual=)` | `KisEndpoint(tr_live=, tr_paper=)` |
  | `endpoint.resolve(virtual)` | `endpoint.resolve(paper)` |
  | `__env__.REAL_DOMAIN` / `VIRTUAL_DOMAIN` | `LIVE_DOMAIN` / `PAPER_DOMAIN` |
  | `__env__.WEBSOCKET_REAL_DOMAIN` / `WEBSOCKET_VIRTUAL_DOMAIN` | `WEBSOCKET_LIVE_DOMAIN` / `WEBSOCKET_PAPER_DOMAIN` |
  | `__env__.REAL_API_REQUEST_PER_SECOND` / `VIRTUAL_...` | `LIVE_API_REQUEST_PER_SECOND` / `PAPER_...` |

  기여자용 — 테스트 환경변수도 바뀌었습니다. 기존 `.env` 의 키 이름을
  고쳐야 합니다(`tests/.env.sample` 참고). 조용히 깨지지는 않습니다 —
  `pytest` 가 누락된 이름을 그대로 찍고 건너뜁니다.

  | 이전 | 이후 |
  |---|---|
  | `VMKIS_VIRTUAL_ACCOUNT_NUMBER` | `VMKIS_PAPER_ACCOUNT_NUMBER` |
  | `VMKIS_VIRTUAL_HTS_ID` | `VMKIS_PAPER_HTS_ID` |
  | `VMKIS_VIRTUAL_APPKEY` | `VMKIS_PAPER_APPKEY` |
  | `VMKIS_VIRTUAL_SECRETKEY` | `VMKIS_PAPER_SECRETKEY` |

  `Realtime`/`realtime`(실시간)은 **다른 개념이라 건드리지 않았습니다.**
  설정 파일의 어휘는 #75 에서 이미 `mode: live | paper` 가 되어 있었고,
  이 변경으로 설정과 코드가 같은 말을 쓰게 되어 `helpers` 의 번역표가
  사라졌습니다.

### 수정

- **`vmkis.exceptions.KisNotFoundError` 가 한 번도 발생하지 않는 클래스를
  가리키고 있었습니다.** 같은 이름의 서로 다른 클래스가 두 곳에 있었는데,
  공개 모듈이 HTTP 404용(라이브러리가 발생시키지 않음)을 내보내고 있어
  **공개 API 대로 잡은 사용자의 핸들러가 절대 실행되지 않았습니다.**

  ```python
  from vmkis.exceptions import KisNotFoundError
  try:
      kis.stock("005930").quote()
  except KisNotFoundError:   # 이전: 절대 잡히지 않음 → 이제 정상 동작
      ...
  ```

  HTTP 404 쪽을 `KisHTTPNotFoundError` 로 개명했습니다.
  `vmkis.client.exceptions.KisNotFoundError` 는 `DeprecationWarning` 과 함께
  동작하며 1.0.0에서 제거됩니다.

- `with_retry` / `with_async_retry` 가 **전역 `retry_config` 를 제자리에서
  변형**했습니다. 인자를 준 데코레이터를 한 번 쓰면 이후 인자 없는
  `@with_retry()` 까지 그 값을 물려받았습니다.

- `utils/retry.py` 가 `client.exceptions` 를 참조하던 계층 위반을 해소했습니다.
  재시도 판단이 예외의 `retryable` 표식으로 바뀌었습니다.
  사용자 정의 예외에 `retryable = True` 를 선언하면 재시도 대상이 됩니다.

- 벤치마크 테스트가 시계 해상도 때문에 **기계가 빠를수록 실패**했습니다.
  `time.time()` → `time.perf_counter()`.

- 자격증명 없이 `pytest` 를 돌리면 17개가 **error** 로 떴습니다. **skip** 으로
  바꾸고 누락된 환경변수를 사유에 적습니다.

- **`import vmkis` 가 helpers 의 결함을 삼켰습니다.** (#73)
  `ImportError` 를 잡아 `create_client` · `save_config_interactive` ·
  `SimpleKIS` 를 조용히 `None` 으로 만들었고, 사용자는 한참 뒤 호출 지점에서
  `TypeError: 'NoneType' object is not callable` 을 받았습니다 — 원인 모듈
  이름이 어디에도 나오지 않았습니다. 폴백을 없앴습니다.

- **`VmKis.request()` 가 유량 초과 시 영원히 재시도**했습니다. (#37)
  서버가 `EGW00201` 을 계속 반환하면 0.1초 간격으로 무한 반복해 호출이
  반환되지 않았습니다. 자동매매에서는 "느리다"가 아니라 "멈춘다"입니다.
  상한과 지수 백오프를 넣었습니다. 연속조회 커서 접미사 4변형도 함께 지원합니다.

- `VmKis` 생성자가 중간에 실패하면 소멸자가 `AttributeError` 를 냈습니다.

### 추가

- [`docs/user/EXTENDING_API.md`](./docs/user/EXTENDING_API.md) — 미지원 TR 을
  `fetch()` 로 호출하는 방법 (Level 0~3 + 함정 체크리스트)

- [`docs/guidelines/CONFIG_SCHEMA.md`](./docs/guidelines/CONFIG_SCHEMA.md) —
  설정 파일 사양. 규칙 R1~R10 과 따옴표 함정을 담습니다

- `vmkis.config` — 설정 읽기·검증 계층. `load_kis_config()` 가 `KisConfig` 를
  돌려주고, 모르는 키를 **오류로 거부**합니다

### 제거

- **런타임 의존성에서 `python-dotenv` 를 뺐습니다.** `src/` 가 한 줄도 쓰지
  않았습니다 — 테스트용으로 넣은 것이 Poetry → uv 이전 때 런타임 쪽만
  살아남은 것입니다. `load_dotenv()` 는 프로세스 전역 `os.environ` 을
  변형하므로, `import vmkis` 만으로 환경이 바뀔지는 라이브러리가 아니라
  애플리케이션이 정할 일입니다.

  **`.env` 파일을 쓰고 있었다면 직접 설치해야 합니다.**

  ```console
  $ pip install python-dotenv
  ```

  지금까지는 vm-stock-kis 가 딸려서 설치해 주고 있었습니다.
  [USER_GUIDE](./docs/user/USER_GUIDE.md) 의 환경 변수 절이 안내하는
  코드가 여기 해당합니다.

---

## [0.0.1] — 2026-08-28

### 버전 번호 재시작

이 배포판(`vm-stock-kis`)의 **첫 릴리스**입니다. 업스트림 `python-kis` 2.1.6에서
갈라져 나왔지만 배포명이 다르므로 pip이 두 버전을 비교하지 않으며, 번호를
이어받을 이유가 없습니다. `0.0.1`부터 시작합니다.

- 호환 폴백 제거 시점을 `v4.0.0` → **`1.0.0`** 으로 재지정.
- `Development Status` classifier를 `5 - Production/Stable` → **`4 - Beta`** 로
  조정. `0.0.1`과 `Production/Stable`은 함께 설 수 없습니다. `1.0.0`에서
  되돌립니다.

### 변경 (Breaking)

- **배포명·모듈명·클래스명 변경.** `python-kis`/`pykis`/`PyKis` →
  `vm-stock-kis`/`vmkis`/`VmKis`. 환경변수 `PYKIS_*` → `VMKIS_*`,
  작업공간 `~/.pykis` → `~/.vmkis`, User-Agent `PyKis/x.y.z` → `VmKis/x.y.z`.
  마이그레이션은 [MIGRATION_GUIDE.md](./docs/MIGRATION_GUIDE.md) 참고.
- flat 레이아웃에서 src 레이아웃(`src/vmkis/`)으로 이관.

### 추가

- v2.x 호환 폴백 3종. 모두 `DeprecationWarning`을 내며 1.0.0에서 제거합니다.
  - `vmkis.PyKis` — `VmKis`와 동일 객체를 반환하므로 `isinstance` 검사도 동작합니다.
    `__all__`에는 넣지 않았습니다.
  - `~/.pykis` 작업공간 폴백 — 기존 사용자의 토큰 캐시 보존.
  - `PYKIS_*` 환경변수 폴백.
- `SECURITY.md` / `SECURITY.en.md` — 보안 정책 및 자격증명 취급 방식.
- `CHANGELOG.md` (이 파일), `.python-version`, `.github/dependabot.yml`.
- `archive/` — 동결 보관소. 수명이 끝난 문서·코드를 당시 상태 그대로 두는
  자리이며 린트·포맷·이름 스윕·배포 대상에서 제외합니다.
  규칙은 [archive/README.md](./archive/README.md) 참고.
- `publish.yml`에 게시 전 검증 — 태그/버전 일치, `twine check --strict`,
  휠 내용(`py.typed` 포함, `pykis/`·`tests/` 부재), 격리 환경 스모크 테스트.
- `ci.yml`에 `Version sanity`, `uv lock --check`, 브랜치 보호용 `ci-ok` 집계 잡.

### 수정

- **`pyyaml`이 런타임 의존성에 없었습니다.** `vmkis.helpers`가 import하는데
  `[project].dependencies`에 없어, 새로 설치한 사용자는 `create_client`와
  `save_config_interactive`가 조용히 `None`이 됐습니다.
- **`SimpleKIS`가 helpers의 import 실패에 휩쓸려 함께 `None`이 됐습니다.**
  정상 import되는데도 같은 `try` 블록에 묶여 있었습니다. import를 분리하고
  `except`를 `Exception` → `ImportError`로 좁혔습니다.
- `__env__.py`가 `except Exception`으로 모든 오류를 삼키고 하드코딩된
  `"2.1.6+dev"`를 반환했습니다. `PackageNotFoundError`로 좁히고 fallback을
  `"0.0.0+unknown"`으로 바꿨습니다.
- `actions/checkout`의 shallow clone 때문에 hatch-vcs가 태그를 읽지 못해
  버전이 `0.0.0`이 됐습니다. `fetch-depth: 0`을 추가했습니다. 그대로 뒀다면
  태그를 붙여도 버전 `0.0.0`인 휠이 PyPI에 올라갔을 것입니다.
- **테스트 스위트가 약 8개월간 완주한 적이 없었습니다.**
  `tests/unit/test_logging.py`가 구문 오류인 채로 커밋되어 pytest 수집이
  실패하고 있었습니다. 복구 후 드러난 실패 3건을 정리하고 커버리지 게이트를
  70에서 90으로 복원했습니다.
- **CI가 단 한 번도 실행된 적이 없었습니다.** `ci.yml`이 YAML 파싱에 실패해
  (heredoc이 블록 스칼라를 조기 종료) 잡이 생성되지 않았습니다. 재작성했습니다.
- rate limiter 타이밍 테스트가 전체 실행에서만 실패하는 flake였습니다.
- 문서가 자격증명을 "암호화 저장"한다고 서술했으나 실제로는 평문 JSON입니다.
  정정했습니다.
- `.github/ISSUE_TEMPLATE/*`와 `CONTRIBUTING.md`의 링크가 업스트림 저장소를
  가리키고 있었습니다.
- **사용자 문서의 GitHub 링크 19곳이 존재하지 않는 저장소를 가리켰습니다.**
  소유자가 `QuantumOmega`(`docs/FAQ.md`, `examples/tutorial_basic.ipynb`) 또는
  자리표시자 그대로인 `yourusername`(`docs/user/en/**`, `examples/README.md`)
  이었습니다. 이름 스윕이 `python-kis` → `vm-stock-kis`만 바꾸고 소유자는
  그대로 둬서 오히려 그럴듯한 죽은 링크가 됐습니다.
- `docs/NEWSLETTER_TEMPLATE.md`가 서식이 아니라 2025년 12월에 발행된 한 호였고
  옛 이름을 담고 있었습니다. 기록물을 `archive/docs/2025-12_NEWSLETTER.md`로
  분리하고, 그 자리에 실제 빈 서식을 새로 썼습니다.

### 제거

- `publish.yml`의 `{{VERSION_PLACEHOLDER}}` 치환 스텝. 해당 placeholder가
  이미 없어져 조용한 no-op이었습니다.
- `ci.yml`의 죽은 `build` 잡.
- pre-commit의 `black`·`isort` 훅. black의 기본 88자가
  `[tool.ruff] line-length = 120`과 충돌해 두 포매터가 서로의 결과를
  되돌리고 있었습니다.
- 개발 도구 체인에서 Poetry. uv로 통일했습니다.

---

## [2.1.6] 이전

이 포크 이전의 이력은 업스트림
[Soju06/python-kis](https://github.com/Soju06/python-kis)를 참고하세요.
