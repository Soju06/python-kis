# 2026-08-28 - Issue #25 배포 전 마이그레이션 재검토 개발 일지

**대상 이슈**: [#25](https://github.com/visualmoney/vm-stock-kis/issues/25)
**프롬프트 문서**: [2026-08-28_issue25_migration_review.md](../prompts/2026-08-28_issue25_migration_review.md)
**범위**: 배포 전 문서 정합성 + 버전 체계 재정의. `v0.0.1` 태그는 붙이지 않았다.

---

## 요약

정식 배포 직전 마이그레이션 산출물을 재검토했다. **배포를 막아야 하는 결함 1건**과,
문서 여러 편이 **일어난 적 없는 릴리스 이력을 서술**하는 문제가 나왔다.

동시에 버전 체계를 재정의했다: `v3.0.0` → **`0.0.1`**, shim 제거는 **`1.0.0`**.

```text
959 passed, 8 skipped (벤치마크 flake 제외 — 사전 결함 #23)
ruff check / ruff format --check 통과
휠 메타데이터 검증 통과 (Metadata-Version 2.4, License-Expression MIT,
                         Development Status :: 4 - Beta, py.typed 포함)
twine check --strict 통과 (whl, tar.gz)
```

---

## 1. Blocker — 설치 안내가 존재하지 않는 배포명을 가리켰다

문서 11곳이 `pip install vmkis` 라고 안내하고 있었다. `vmkis` 는 **모듈명**이고
배포명은 `vm-stock-kis` 다.

```console
$ curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/vmkis/json
404
```

지금은 실패하지만 **누구나 그 이름을 선점할 수 있다.** 선점되는 순간 우리 공식
문서가 제3자 패키지 설치를 안내하게 된다. 증권 API 자격증명을 다루는
라이브러리에서 가벼운 문제가 아니다.

| 파일 | 곳 |
|---|---|
| `docs/user/en/{FAQ,QUICKSTART,README}.md` | 4 |
| `docs/guidelines/VIDEO_SCRIPT.md` | 3 |
| `docs/guidelines/API_STABILITY_POLICY.md` | 2 |
| `examples/tutorial_basic.ipynb` | 2 |

한국어 문서는 전부 올바랐다. **영문 문서·영상 대본·노트북만 틀렸다.**

### 원인 — 스윕이 산문과 코드를 구분하지 못했다

이슈 #2의 `\bpykis\b` → `vmkis` 규칙은 import 문에서는 옳지만 설치 명령에서는
틀린다. 게다가 이 규칙은 **틀린 것을 그럴듯하게 만들었다.** 스윕 전에는
`pip install pykis`(명백히 남의 패키지)였는데, 스윕 후 `pip install vmkis`가 되어
우리 모듈명과 같아졌다.

`VIDEO_SCRIPT.md` 의 ASCII 상자는 문자열이 길어지며 테두리가 깨져, 한중일
문자를 2칸으로 계산해 다시 그렸다.

---

## 2. 버전 체계 재정의 — 3.0.0 → 0.0.1

`vm-stock-kis` 는 PyPI에 **존재한 적이 없다**(404). 이번이 이 이름의 첫
릴리스다. `3.0.0` 은 업스트림 2.1.6을 이어받아 "Breaking Change니 major를
올린다"는 논리로 정한 숫자였지만, **배포명이 다르면 pip은 두 버전을 비교하지
않는다.** 이어받을 이유가 없고, 첫 릴리스가 3.0.0인 것은 실제보다 성숙해 보이게
만든다.

| | 이전 | 확정 |
|---|---|---|
| 1차 정식 | `v3.0.0` | `0.0.1` |
| shim 제거 | `v4.0.0` | `1.0.0` |
| `Development Status` | `5 - Production/Stable` | `4 - Beta` |

`Development Status` 를 함께 내린 이유는 `0.0.1` 과 `Production/Stable` 이 함께
설 수 없기 때문이다. 어긋나면 PyPI 프로젝트 페이지에서 바로 드러난다.
`1.0.0` 에서 되돌린다.

### 배포되는 코드 안의 문자열

버전 표기는 문서에만 있는 게 아니었다.

| 위치 | 내용 |
|---|---|
| `src/vmkis/__init__.py:84` | `PyKis` 별칭 `DeprecationWarning` 문구 |
| `src/vmkis/helpers.py:31` | `PYKIS_*` 폴백 경고 문구 |
| `src/vmkis/utils/workspace.py:28` | `~/.pykis` 폴백 경고 문구 |
| `src/vmkis/types.py:62-70` | 모듈 docstring의 버전 정책 표 |
| `tests/unit/**` | 위 문구를 단언하는 테스트 |

사용자가 실제로 읽는 것은 이 문자열이므로 문서보다 우선한다.

### 버전이 낮아지는 것에 대한 안내

`MIGRATION_GUIDE.md` 에 [2절](../MIGRATION_GUIDE.md#2-버전-번호가-낮아지는-이유)을
새로 넣었다. 설명이 없으면 사용자는 되돌아간 것으로 오해한다. `README.md` 의
Changelog 절(업스트림 2.1.x 이력)에도 같은 취지의 안내를 달았다 — 그 절만 읽으면
이 포크가 2.1.3에 머물러 있는 것처럼 보인다.

---

## 3. `MIGRATION_GUIDE.md` 는 부분 수정이 아니라 재작성

문서가 `v2.1.7 → v2.2.0 → v3.0.0` 3단 구성으로 쓰여 있었는데 **그런 릴리스는
존재하지 않았다.** 이 포크는 아무것도 게시한 적이 없고, "v2.2.0 변경사항"으로
서술된 작업(공개 API 축소, `public_types`, `SimpleKIS`)은 전부 미배포 상태로
`0.0.1` 에 함께 실린다.

게다가 이슈 #2의 스윕이 "v2.x 시절" 예제까지 새 이름으로 바꿔 놓아 문서가 스스로를
반박하고 있었다.

```python
**이전 (v2.1.7)**:

from vmkis import (          # v2.1.7에는 vmkis 가 존재하지 않았다
    VmKis, KisAuth,          # VmKis 도 없었다
```

특히 "Import 경로 변경" 비교표는 `v2.1.7 | v2.2.0+ | v3.0.0+` 세 열이 전부
`from vmkis import ...` 라 **표가 아무것도 비교하지 못했다.**

실제 구조(업스트림 2.1.6 → 이 포크 0.0.1 → 1.0.0)에 맞춰 다시 썼다.

### 재작성 중 발견한 사실 오류

문서를 코드에 대조하다 세 곳이 틀린 것을 찾았다.

| 문서의 서술 | 실제 |
|---|---|
| `SimpleKIS(config_path="config.yaml")` | 생성자는 `VmKis` **인스턴스**를 받는다 (`simple.py:15`) |
| `MarketInfo` = `KisMarketInfo` | `KisMarketType` (`public_types.py:21`) |
| 공개 API "20개" | `__all__` 은 **12개** |

`SimpleKIS` 는 문서대로 따라 하면 `TypeError` 가 난다. 초보자용 도구를 소개하는
절이 초보자를 막고 있었다.

---

## 4. `API_STABILITY_POLICY.md` — 가공된 릴리스 이력

"v1.x END-OF-LIFE / v2.x 12개월 지원 / v3.0-beta 2026-01~2027-01" 같은 표가
있었다. **이 배포판에는 그런 이력도 지원 약속도 없다.**

- 버전 정책 표, 지원 기간 표, Deprecation 3단계, 마이그레이션 타임라인,
  Python 호환성 표, 의존성 표, FAQ를 실제 상태로 교체
- 지원 기간을 "정하지 않았다"고 명시 — **지킬 수 없는 약속을 적는 것보다 낫다**
- 의존성 표의 값이 `pyproject.toml` 과 어긋나 있어(예: `requests>=2.25.0` vs
  실제 `>=2.32.3`) 실제 값으로 고치고 **유일한 출처가 `pyproject.toml`** 임을 명시
- 버전 고정 예시가 `vmkis>=2.0.0,<3.0.0` 이었다 — 배포명·버전 둘 다 틀렸다.
  `vm-stock-kis>=0.0.1,<1.0.0` 으로 고치고 0.x 에서는 minor 도 Breaking 자리라는
  경고를 달았다

---

## 5. `Python KIS` — 스윕이 놓친 브랜딩

이슈 #2의 스윕은 `Python-KIS`(붙임표)만 찾았다. 붙임표 없는 표기가 5곳 남아
있었고 **그중 4곳이 문서의 H1 제목**이었다.

`docs/README.md`, `docs/architecture/ARCHITECTURE.md`,
`docs/developer/DEVELOPER_GUIDE.md`, `docs/user/USER_GUIDE.md`,
그리고 `VIDEO_SCRIPT.md` 의 YouTube 해시태그(`#PythonKIS`).

### 같은 실수를 한 번 더 했다

이 치환을 `-- 'docs/*'` 로 돌려 `docs/dev_logs/` 와 `docs/reports/` 의 기록물
5개까지 건드렸다. 커밋 직전 `git status` 에서 발견해 되돌렸다.

**기록물 제외는 스윕할 때마다 매번 명시해야 한다.** 이슈 #2가 pathspec으로
그 목록을 남겨 둔 이유가 이것이다.

```text
':!docs/dev_logs' ':!docs/reports' ':!docs/prompts'
':!docs/generated' ':!docs/rules' ':!docs/diagrams' ':!archive'
```

---

## 변경 파일

- `docs/MIGRATION_GUIDE.md` — 재작성
- `docs/guidelines/API_STABILITY_POLICY.md` — 버전/지원 정책 전면 갱신
- `src/vmkis/{__init__,helpers,types}.py`, `src/vmkis/utils/workspace.py` — 경고 문구
- `tests/unit/test_compat_aliases.py`, `tests/unit/utils/{test_workspace,test_diagnosis}.py`
- `pyproject.toml` — `Development Status :: 4 - Beta`
- `CHANGELOG.md` — 버전 재시작 절 추가
- `README.md` — Changelog 절에 업스트림 이력 안내
- `docs/FAQ.md`, `docs/user/en/**`, `examples/**`, `docs/guidelines/VIDEO_SCRIPT.md`
- `docs/architecture/ARCHITECTURE.md`, `docs/developer/VERSIONING.md`,
  `docs/NEWSLETTER_TEMPLATE.md`, `docs/README.md`,
  `docs/developer/DEVELOPER_GUIDE.md`, `docs/user/USER_GUIDE.md`
- `.github/workflows/publish.yml` — 태그 예시 주석

---

## 검증

```console
$ uv run ruff check .           All checks passed!
$ uv run ruff format --check .  185 files already formatted
$ uv run pytest -q -m "not requires_api" --deselect tests/performance/test_benchmark.py
  959 passed, 8 skipped, 24 deselected

$ uv build && twine check --strict
  Metadata-Version: 2.4
  Name: vm-stock-kis
  License-Expression: MIT
  License-File: LICENCE
  Classifier: Development Status :: 4 - Beta
  Requires-Python: >=3.10
  py.typed 포함: True / pykis/ 부재: True / tests/ 미포함: True
  PASSED (whl, tar.gz)
```

이슈 #25 완료 기준:

```console
$ git grep -nE '(pip install|uv add) vmkis\b' -- . ':!archive' ...
(빈 출력)
$ git grep -c -E '\bpykis\b|\bPyKis\b' docs/MIGRATION_GUIDE.md
18            # 0보다 커야 정상 — 마이그레이션 문서는 옛 이름을 보여야 한다
$ git grep -n 'migrate_imports' -- . ':!archive' ...
(빈 출력)
```

벤치마크 4건은 시계 해상도 flake로 [#23](https://github.com/visualmoney/vm-stock-kis/issues/23)에
분리돼 있어 `--deselect` 했다. `main` 에서 동일하게 재현된다.

---

## 다음 할 일

- [ ] `v0.0.1rc1` 태그로 TestPyPI 리허설.
      **`v3.0.0rc2` 리허설 결과는 더 이상 유효하지 않다** — 버전과 classifier가
      바뀌었고 배포되는 코드의 경고 문구도 바뀌었다.
- [ ] 통과 후 `v0.0.1` 정식 배포 → 그 뒤 [#2](https://github.com/visualmoney/vm-stock-kis/issues/2) close
- [ ] [#23](https://github.com/visualmoney/vm-stock-kis/issues/23) 벤치마크 flake
- [ ] `docs/INDEX.md` 가 망가져 있다 (트리 블록이 섞이고 없는 `docs/user/ko/` 안내)
- [ ] 1.0.0 시점에 `Development Status` 를 `5 - Production/Stable` 로 되돌릴 것

### TestPyPI 에 남는 것

`vm-stock-kis` 3.0.0rc1 / 3.0.0rc2 가 TestPyPI에 남는다. 삭제해도 이름은
되살아나지 않으므로 그대로 둔다. TestPyPI의 "최신"이 3.0.0rc2 로 보이지만
표시상의 문제이며 PyPI(404, 깨끗함)에는 영향이 없다.
