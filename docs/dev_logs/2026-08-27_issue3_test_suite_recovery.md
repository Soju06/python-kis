# 2026-08-27 - Issue #3 테스트 스위트 부채 정리 개발 일지

**대상 이슈**: [visualmoney/vm-stock-kis#3](https://github.com/visualmoney/vm-stock-kis/issues/3)
**프롬프트 문서**: [2026-08-27_issue3_test_suite_recovery.md](../prompts/2026-08-27_issue3_test_suite_recovery.md)

---

## 요약

| 항목 | 베이스라인 | 완료 후 |
|---|---|---|
| 테스트 | 3 failed, 870 passed | **0 failed, 943 passed** |
| 커버리지 | 89.01% | **90.63%** |
| `fail_under` | 70 (한시 인하) | **90 (복원)** |
| `pykis/helpers.py` | 27% | **100%** |
| CI 실행 | 0초 만에 failure ×7 | 유효한 워크플로로 재작성 |
| pre-commit | 미설치 | 설치 + 가드 훅 검증 완료 |

---

## 작업 내용

### 1. 로깅 통합 테스트 2건 — 이슈의 제안(`capfd`)으로는 해결되지 않았음

이슈는 `capsys` → `capfd` 교체를 제안했으나 **실제로 적용해 보니 여전히 실패**했다.

원인은 한 단계 더 깊었다. `pykis/logging.py`의 기본 핸들러는 모듈 import 시점에
`logging.StreamHandler(stream=sys.stdout)`으로 만들어지며 그 시점의 `sys.stdout`
객체를 붙잡는다. pytest 실행 중 그 객체는 **pytest가 세션 시작 시 설치한 전역
캡처 스트림**이다. 따라서

* `capsys`는 나중에 `sys.stdout`을 교체하므로 이미 붙잡힌 스트림을 보지 못하고,
* `capfd`도 fd 1을 새로 리다이렉트할 뿐이라 전역 캡처 스트림으로 나가는 출력을
  보지 못한다.

pytest의 캡처 계층에 기대는 대신 **핸들러의 스트림을 `StringIO`로 직접 교체**하는
`log_output` 픽스처를 도입했다. 포매팅과 레벨 필터링을 결정적으로 검증하며 pytest
캡처 구현에 의존하지 않는다. (해당 테스트 파일에 `from io import StringIO`가
import만 되고 미사용 상태로 남아 있었다 — 원저자도 이 방식을 의도했던 것으로 보인다.)

전역 로거 레벨이 테스트 사이로 새는 문제도 `restore_log_level` 픽스처로 막았다.

### 2. Rate limit 동시성 테스트 — 라이브러리가 아니라 픽스처의 시한폭탄

`mock_token_response` 픽스처가 만료 시각을 `"2025-12-31 23:59:59"`로 **하드코딩**
하고 있었다. 작업일(2026-08-27) 기준 이미 지난 값이다.

`PyKis.primary_token`은 `remaining < 10분`이면 재발급하므로 만료된 토큰은 매 요청마다
재발급된다. 그리고 `token_issue()`는 `self.fetch()` → `self.request()` 경로를 타므로
**동일 rate limiter 쿼터를 소비**한다.

실측으로 확인했다:

| 토큰 만료 시각 | 요청 10회 시 총 HTTP | 토큰 발급 | 소요 |
|---|---|---|---|
| 하드코딩(만료됨) | 20 | 10회 | 9.47초 |
| 상대 시각(유효) | 11 | 1회 | 5.25초 |

`RateLimiter(rate=2, period=1)`의 대기 횟수는 `(획득 횟수 - 1) // rate`이다.
20회 → 9회 대기 → 9.45초로, 이슈 본문의 "유량 대기 경고 9회"와 정확히 일치한다.

**판정**: 토큰 발급이 쿼터를 소비하는 것은 실제 API 호출이므로 보수적으로 옳다.
구현은 바꾸지 않고 픽스처를 상대 시각으로 고쳤다.

단언도 재작성했다. 시간 상한 대신 **HTTP 요청 횟수**를 단언한다(`토큰 1회 + 요청 10회`).
쿼터가 새는 회귀를 머신 속도와 무관하게 잡아내며, 원인도 정확히 지목한다.
시간은 하한만 엄격히 보고(유량 제한이 실제로 걸렸는지) 상한은 느린 머신을 감안해
넉넉히 뒀다. 예외를 삼키던 `except Exception: pass`도 제거하고 스레드 밖으로 전달해
단언한다.

### 3. 커버리지 89.01% → 90.63%

#### `pykis/helpers.py` 27% → 100% — 커버리지 문제가 아니라 버그였다

`save_config_interactive()`의 본문(81~162행)이 **모듈 전체의 복사본**이었다.
`import`, `__all__`, 세 함수의 중복 정의가 함수 안에 중첩되어 있었고, 바깥 함수는
그것들을 호출하지도 반환하지도 않았다. 즉 이 함수는 **아무 일도 하지 않고 `None`을
반환**했다. 선언된 반환 타입은 `dict[str, Any]`이고 `pykis/__init__.py`가 공개
API로 export하므로 실사용 시 오동작하는 버그였다.

죽은 코드를 제거하고 중첩되어 있던 실제 구현을 복원했다(구문 수 66 → 48).

#### 그 외 보강

이슈가 지목한 저커버리지 모듈과, 확인 중 발견한 자기순환 테스트를 함께 정리했다.

* `pykis/adapter/websocket/price.py` 64% — 기존 테스트가 `on`/`once` **자체를
  페이크로 교체한 뒤 그 페이크를 검증**하고 있어 실제 분기 코드를 한 줄도 실행하지
  않았다. 지연 import되는 하위 함수를 대체해 진짜 디스패치를 타는 테스트를 추가했다.
* `pykis/adapter/websocket/execution.py` — 네 곳의 "알 수 없는 이벤트" 거부 경로 중
  한 곳만 검증되고 있었다.
* `pykis/responses/types.py` — `transform()`의 두 공통 경로(이미 변환된 값의 멱등성,
  빈 문자열 → `KisNoneValueError`)가 전부 미검증이었다.
* `pykis/utils/repr.py` — 여러 줄 모드, 생략 표기, 빈 컨테이너, 깊이 컷오프.
* `pykis/simple.py` — `SimpleKIS`의 시장가/지정가 분기와 취소 위임.

`[tool.coverage.report] fail_under`를 **70 → 90으로 복원**했다.

### 4. 재발 방지 — 이슈의 전제가 사실과 달랐다

이슈는 "CI는 `--maxfail=1`로 돌고 있어 아무도 눈치채지 못했다"고 기술했다.
**확인 결과 CI는 단 한 번도 실행된 적이 없다.**

`.github/workflows/ci.yml`은 74행에서 YAML 파싱에 실패한다. `build` 잡의 heredoc
본문이 컬럼 0에 있어 `run: |` 블록 스칼라가 조기 종료되고 문서 전체가 깨진다.

증거:

| 확인 항목 | 결과 |
|---|---|
| 워크플로 등록 이름 | `CI`가 아니라 `.github/workflows/ci.yml` (경로 그대로) |
| ci.yml 실행 이력 | 7회, **전부 `failure` / `0s`** |
| 최신 실행의 job 수 | **0개** |
| 브랜치 보호 | `404 Branch not protected` |
| `.git/hooks/pre-commit` | **없음** |

워크플로 이름이 파일 경로로 등록됐다는 것은 GitHub가 이 파일을 한 번도 파싱하지
못했다는 뜻이다. 그리고 `--maxfail=1`은 아무것도 가리지 않았다 — pytest는 수집
오류 시 exit 2로 죽으며 파일명과 `SyntaxError`를 그대로 출력한다(재현 확인).

**즉 8개월 침묵의 원인은 "`--maxfail=1`이 가렸다"가 아니라 "CI가 존재하지 않았다"이다.**
그리고 `.pre-commit-config.yaml`에는 이미 `check-yaml`이 있었다. 설치만 되어
있었다면 깨진 ci.yml의 커밋 자체가 차단됐다. **규칙이 부족한 게 아니라 규칙이
실행되지 않고 있었다.**

#### 이슈의 3개 제안에 대한 판정

| 제안 | 판정 | 근거 |
|---|---|---|
| main 브랜치 보호에 필수 체크 등록 | **기각** | 등록할 체크 런이 0개라 물리적으로 불가능. 1인 프로젝트(PR 1건, main 직푸시)에서 본인이 admin이라 우회 2클릭 |
| `check-ast` 훅 추가 | **채택** | 아래 참고 |
| `--collect-only` 별도 스텝 | **채택(축소)** | 아래 참고 |

`check-ast`는 처음에 "ruff가 이미 구문 오류를 잡으므로 중복"으로 판단했다(실측:
깨진 파일에 ruff가 5건 보고). 그러나 **ruff를 pre-commit에서 빼기로 결정하면서
판정을 뒤집었다.** 현재 코드베이스에 ruff 오류 1003건, 미포맷 파일 120개가 남아
있어 지금 ruff 훅을 넣으면 거의 모든 커밋이 막힌다. ruff가 훅에 없는 이상 파이썬
구문 오류를 막을 장치가 필요하고, `check-ast`는 스타일 의견 없이 그 일만 한다.

`--collect-only`는 별도 스텝으로 넣었다. 수집 오류는 exit 2로 이미 표면화되지만,
스텝을 나눠 두면 실행 목록에서 어느 단계에서 터졌는지 바로 보인다.
`--maxfail=1`은 **제거**했다 — 1인 프로젝트에서는 한 번의 red로 전체 피해 범위를
봐야 왕복이 줄고, 타이밍 의존 테스트가 있어 무관한 실패로 런이 잘릴 수 있다.

#### 실제 적용

* **`.github/workflows/ci.yml` 전면 재작성**: 유효한 YAML, Poetry → uv,
  `build` 잡 삭제(치명적 heredoc이 있던 곳이고, `{{VERSION_PLACEHOLDER}}`가 이미
  없어져 죽은 코드였다 — hatch-vcs가 태그에서 버전을 만든다).
  매트릭스는 6잡(3 OS × 2 버전) → 2잡(`3.10`, `3.13`)으로 축소했다.
  `requires-python = ">=3.10"`인데 **하한 3.10이 검증되지 않고 있었다.**
  두 버전 모두 로컬에서 943 passed 확인.
* **커버리지 게이트 일원화**: CI에서 `--fail-under=90`을 따로 주지 않고
  `pyproject.toml`의 `fail_under`를 따르게 했다. 두 곳에 두면 갈라진다.
* **`lint-workflows` 잡 추가**: `actionlint`. CI는 자기 파일이 깨졌는지 스스로 알
  수 없으므로(파싱 실패 시 잡이 생성되지 않음) pre-commit 훅과 이중으로 뒀다.
* **`.pre-commit-config.yaml` 정리**: `check-ast`, `actionlint` 추가.
  `black`/`isort` 제거 — black의 기본 88자가 `[tool.ruff] line-length = 120`과
  충돌해 두 포매터가 서로의 결과를 되돌렸고(`[tool.black]`도 `[tool.isort]`도
  없었다), isort는 ruff의 `I` 규칙과 중복이었다.
  ruff/pyupgrade/docformatter는 일괄 정리 전까지 보류.
* **`pre-commit install` 실행** — 이번 재발 방지의 실질적 핵심.
* **`publish.yml`**: actionlint가 지적한 낡은 액션 버전만 갱신
  (`checkout@v3` → `v4`, `setup-python@v3` → `v5`). 나머지 문제는 손대지 않았다.
* **README에 CI 배지 추가**.

#### 가드 동작 검증

두 사고를 실제로 재현해 훅이 막는지 확인했다.

```text
check-ast  ← git show 9a75692:tests/unit/test_logging.py
  SyntaxError: unmatched ']'                         (차단됨)

check-yaml ← git show 9a75692:.github/workflows/ci.yml
  could not find expected ':' ... line 74            (차단됨)
```

---

## 변경 파일

### 라이브러리

* `pykis/helpers.py` — 중첩된 죽은 코드 제거, `save_config_interactive()` 복원

### 테스트

* `tests/unit/test_logging.py` — `log_output`/`restore_log_level` 픽스처 도입
* `tests/integration/test_rate_limit_compliance.py` — 토큰 픽스처 상대 시각화,
  요청 횟수 기반 단언으로 재작성
* `tests/unit/test_helpers.py` — 신규 (22건)
* `tests/unit/test_simple.py` — 신규 (6건)
* `tests/unit/adapter/websocket/test_price.py` — 실제 디스패치 테스트 추가
* `tests/unit/adapter/websocket/test_execution.py` — 이벤트 거부 경로 추가
* `tests/unit/responses/test_types.py` — `transform()` 공통 경로 추가
* `tests/unit/utils/test_repr.py` — 여러 줄/생략/경계 동작 추가

### 인프라

* `.github/workflows/ci.yml` — 전면 재작성
* `.github/workflows/publish.yml` — 액션 버전 갱신
* `.pre-commit-config.yaml` — 가드 훅 중심으로 재구성
* `pyproject.toml` — `fail_under` 90 복원, ruff 상한 지정
* `uv.lock` — ruff 제약 변경 반영
* `README.md` — CI 배지

### 문서

* `docs/prompts/2026-08-27_issue3_test_suite_recovery.md` — 신규
* `docs/dev_logs/2026-08-27_issue3_test_suite_recovery.md` — 이 문서

---

## 테스트 결과

```text
943 passed, 8 skipped, 17 deselected in 51.46s
Required test coverage of 90.0% reached. Total coverage: 90.63%
```

Python 3.10 / 3.13 양쪽에서 확인.

---

## 남은 일

### 이 이슈에서 의도적으로 제외한 것

* **`pyyaml`이 런타임 의존성에 없음**. `pykis/helpers.py`가 `import yaml`을 하는데
  `[project].dependencies`에 `pyyaml`이 없다. 현재 환경에 있는 이유는 **lint 그룹의
  `pre-commit`이 전이 의존으로 끌어오기 때문**이다. `pykis/__init__.py`가 helpers
  import를 `try/except Exception`으로 감싸고 있어, PyPI에서 설치한 사용자는
  `create_client`와 `save_config_interactive`가 조용히 `None`이 된다.
  → 패키징 이슈(#2)에서 다룰 것.

* **ruff 정리**: 오류 1003건, 미포맷 파일 120개. `[tool.ruff]`에 `select`가 없어
  ruff 버전에 따라 판정이 요동친다(v0.14.10에서 228건, v0.16.4에서 1003건).
  일괄 포맷 커밋 후 pre-commit과 CI에 ruff를 다시 넣을 것.

* **`publish.yml`이 깨져 있음**: `v2.1.6` 태그 실행이 PyPI 신뢰 게시자 미설정으로
  실패했다(`invalid-publisher`). `sed`로 `{{VERSION_PLACEHOLDER}}`를 치환하는
  스텝은 그 placeholder가 이미 없어 조용한 no-op이고, `python -m build`는
  hatchling/hatch-vcs 전환이 반영되지 않았다. → 별도 이슈로 분리 필요.

### 수동 조치 필요 (코드로 할 수 없음)

* **GitHub 실패 알림 켜기**: Settings → Notifications → Actions →
  `Email` + "Send notifications for failed workflows only".
  8개월 침묵에 대한 유일한 직접적 처방이다. 위의 어떤 코드 변경도
  "빨간 X를 아무도 안 봤다"는 문제 자체는 고치지 못한다.
