# API 안정성 정책 (API_STABILITY_POLICY.md)

**작성일**: 2025-12-20
**대상**: 개발자, 사용자, 라이브러리 유지보수자
**버전**: v1.1

---

## 개요

VM-Stock-KIS의 **API 안정성 보장 정책**을 정의합니다. 사용자는 본 정책에 따라 버전 선택 및 업그레이드 계획을 수립할 수 있습니다.

---

## 1. API 안정성 레벨

### 1.1 레벨 정의

VM-Stock-KIS의 모든 공개 API는 다음 중 하나의 안정성 레벨을 갖습니다:

| 레벨 | 기호 | 설명 | 하위 호환성 | 지원 기간 |
|------|------|------|-----------|---------|
| **Stable** | 🟢 | 프로덕션 사용 완벽 안전 | 보장 | 12개월 |
| **Beta** | 🟡 | 곧 안정화될 기능 | 부분 | 6개월 |
| **Deprecated** | 🔴 | 곧 제거될 기능 | 그대로 | 6개월 |
| **Removed** | ⚫ | 이미 제거된 기능 | 불가 | N/A |

---

## 2. 버전별 안정성 보장

### 2.1 의미론적 버전 (Semantic Versioning)

```text
Major.Minor.Patch-PreRelease+Metadata
^      ^     ^
|      |     └─ Patch 증가: 버그 수정 (호환성 보장)
|      └─────── Minor 증가: 기능 추가 (호환성 보장)
└──────────────── Major 증가: Breaking Change (호환성 미보장)
```

### 2.2 Major 버전 정책

| 버전 | 라이프사이클 | 호환성 |
|---|---|---|
| 0.0.x | ⚪ 지난 판 (2026-08-28 ~ 08-29) | 당시 0.x 규칙: minor 도 Breaking 자리 |
| 0.3.0 | ⚪ 지난 판 | 호환 폴백 제거(`#33` · `#34`) + `Production/Stable`(`#35`) |
| **1.0.0** | 🟢 **현재** | SemVer major 라인. 같은 major 안 minor·patch 는 공개 API 를 깨지 않음 |

**1.0.0 이 약속하는 SemVer 한 줄:** 같은 major 안에서 minor·patch 는 공개 API 를
깨지 않습니다. Breaking 은 major 만. (0.x 의 “minor 도 Breaking 자리” 규칙은
`v1.0.0` 태그에서 끝났습니다.)

> Breaking·Stable classifier 는 **0.3.0** 에 들어갔고, **1.0.0** 은 그 SemVer
> 약속을 번호로 고정한 태그입니다. 폴백을 “다시” 지우지 않았습니다.
>
> 이 표는 배포판 `vm-stock-kis` 의 것입니다. 업스트림 `python-kis` 의
> 2.x 계열과는 **번호를 공유하지 않습니다.**

---

## 3. Breaking Change 정책

### 3.1 Breaking Change 정의

Breaking Change는 **기존 코드를 수정하지 않으면 작동하지 않게 하는 변경**입니다.

**예시**:

```python
# ✅ Breaking Change 아님 (Minor 버전)
# 0.0.1: kis.stock("005930").quote()
# 0.0.2: kis.stock("005930").quote(include_extended=True)  # 선택적 파라미터 추가

# ❌ Breaking Change (Major 버전)
# 0.x: kis.stock("005930").quote()
# 1.0.0: kis.stock("005930").get_quote()  # 메서드명 변경
```

### 3.2 Breaking Change 종류

| 종류 | 영향 | 예시 | 버전 |
|------|------|------|------|
| **메서드 삭제** | 매우 높음 | `quote()` 제거 | Major |
| **파라미터 제거** | 높음 | `price` 파라미터 제거 | Major |
| **반환 타입 변경** | 높음 | List → Dict 반환 | Major |
| **예외 처리 변경** | 중간 | 새로운 예외 발생 | Major |
| **기본값 변경** | 중간 | `timeout=30` → `timeout=60` | Minor* |
| **선택적 파라미터 추가** | 낮음 | `quote(include_extended=False)` | Minor |

*기본값 변경은 논쟁의 여지가 있으므로 0.x 에서는 바꾸지 않습니다

---

## 4. 마이그레이션 경로

### 4.1 Deprecation 프로세스

```text
준비    →  경고    →  마이그레이션  →  제거
신규 경로   0.0.x–0.2.x          사용자 작업        0.3.0
```

### 4.2 Deprecation 3단계

#### 1️⃣ 준비 (신규 경로 도입)

- ✅ 신규 기능 제공 (권장)
- 🔴 경고 없음 (기존 코드 정상 작동)

**예시**:

```python
# 신규 경로
from vmkis.types import KisObjectProtocol

# 루트 위임은 0.3.0 에서 제거됨 — 아래는 더 이상 동작하지 않습니다
# from vmkis import KisObjectProtocol
```

#### 2️⃣ 경고 (0.0.x–0.2.x)

- ✅ 신규 기능 권장
- ⚠️ 경고 표시 (DeprecationWarning)
- ✅ 기존 코드 계속 작동

**예시**:

```python
# 0.2.x 까지는 DeprecationWarning, 0.3.0 부터는 ImportError
# from vmkis import KisObjectProtocol

# 올바른 경로
from vmkis.types import KisObjectProtocol
```

#### 3️⃣ 제거 (0.3.0)

- ✅ 신규 기능만 제공
- ❌ 기존 경로 작동 불가

**예시**:

```python
# 0.3.0: 루트 위임 제거 — 아래는 ImportError
# from vmkis import KisObjectProtocol

# ✅ 올바른 방식
from vmkis.types import KisObjectProtocol
```

### 4.3 마이그레이션 타임라인

```text
python-kis 2.1.6        업스트림. 이 포크의 기점
      │
      │  포크 · 이름 변경 · 버전 재시작
      ▼
vm-stock-kis 0.0.1      이 배포명의 첫 릴리스 (2026-08)
      │                 · 루트 deprecated 경로 = 경고와 함께 동작
      │                 · PyKis / ~/.pykis / PYKIS_* 폴백 = 동작
      ▼
vm-stock-kis 0.3.0      위 호환 경로 **완전 제거** (#33 · #34)
                        Development Status → 5 - Production/Stable (#35)
      ▼
vm-stock-kis 1.0.0      SemVer major 라인 선언 (태그). 폴백을 다시 지우지 않음
```

> **버전이 2.1.6보다 낮아지는 것은 다운그레이드가 아닙니다.** 배포명이
> 다르므로(`python-kis` ↔ `vm-stock-kis`) 두 버전은 서로 비교되지 않습니다.
> 자세한 설명은 [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) 를 보세요.

---

## 5. 보장되는 안정성

### 5.1 메이저 버전 내 보장

**0.3.0+ / 1.0.0 라인에서 보장하는 것** (§2.2 SemVer 한 줄):

```python
# ✅ 공개 표면
from vmkis import VmKis, Quote, Balance, Order

kis = VmKis(id="...", account="...", appkey="...", secretkey="...")
quote = kis.stock("005930").quote()
```

**보장 범위**:

- 공개 API 메서드 이름
- 반환 타입 구조
- 파라미터 순서
- 기본 기능

**보장 안 하는 범위**:

- 내부 구현 (`src/vmkis/` 의 비공개 모듈. 루트 `__all__` 밖)
- 성능 특성
- 에러 메시지 정확한 문구
- 시간 초과 값

### 5.2 Minor 버전 내 추가 사항

**호환성 유지 변경**:

- ✅ 선택적 파라미터 추가
- ✅ 새로운 클래스/함수 추가
- ✅ 새로운 예외 타입 추가
- ✅ 성능 최적화
- ✅ 버그 수정

**예시**:

```python
# 0.0.1
quote = kis.stock("005930").quote()
# {'price': 60000, 'volume': 1000000}

# 0.0.2 (호환성 유지)
quote = kis.stock("005930").quote(include_extended=True)
# {'price': 60000, 'volume': 1000000, 'extended': {...}}

# ✅ 0.0.1 코드도 0.0.2에서 계속 작동
quote = kis.stock("005930").quote()
```

---

## 6. 버전 선택 가이드

### 6.1 버전별 권장 사용자

| 배포판 | 버전 | 상태 | 추천 |
|---|---|---|---|
| `python-kis` (업스트림) | 2.1.6 | 🟡 별개 프로젝트 | 이 포크와 무관하게 유지됩니다 |
| `vm-stock-kis` | 0.3.0 | ⚪ 지난 판 | Breaking·Stable 착지 시점 |
| **`vm-stock-kis`** | **1.0.0** | 🟢 **현재** | SemVer major. pip 는 git 태그를 따름 |

### 6.2 업그레이드 계획

```text
✅ python-kis 2.x 를 쓰던 경우:
1. pip uninstall python-kis  (둘 다 설치된 상태가 가장 흔한 실패 모드)
2. pip install vm-stock-kis
3. MIGRATION_GUIDE.md 의 이름 대조표대로 코드 치환

⚠️ 0.2.x 이하에서 0.3.0+ 로:
1. `PyKis` → `VmKis`, `PYKIS_*` → `VMKIS_*`, `~/.pykis` → `~/.vmkis`
2. `from vmkis import <내부타입>` → `from vmkis.types import …`
3. 공개 타입(`Quote` 등)은 루트 그대로

1.0.0 태그는 위 치환을 “다시” 요구하지 않습니다.
```

---

## 7. 지원 정책

### 7.1 버전별 지원 기간

**1.0.0 이후** 지원 대상은 항상 **최신 major** 입니다. 이전 major 로는 백포트하지
않습니다. 보안 패치는 [SECURITY.md](../../SECURITY.md) 절차를 따릅니다.

minor · patch 는 최신 1.x 라인에만 나갑니다. 지원 기간을 “N개월”처럼 날짜로
박지 않습니다 — 약속할 수 있는 것은 **어느 라인을 고치는가**뿐입니다.

업스트림 [`Soju06/python-kis`](https://github.com/Soju06/python-kis) 의 지원
정책은 이 문서의 대상이 아닙니다.

### 7.2 지원 유형

| 지원 유형 | 내용 | 대상 |
|---|---|---|
| **일반 지원** | 버그 수정, 성능 개선 | 최신 1.x |
| **보안 패치** | 보안 취약점 수정 | 최신 1.x ([SECURITY.md](../../SECURITY.md)) |
| **하위 호환성** | 공개 API 시그니처 유지 | 같은 major |
| **질문/이슈** | GitHub Issues | 지속 |

---

## 8. 버전 확인 및 업데이트

### 8.1 현재 버전 확인

```python
import vmkis

print(f"VmKis 버전: {vmkis.__version__}")
# 출력은 설치된 배포판의 태그입니다. 숫자를 여기에 박지 않습니다.
```

### 8.2 최신 버전 확인

```bash
# PyPI에서 최신 버전 확인
pip index versions vm-stock-kis

# 또는
pip list --outdated | grep vm-stock-kis
```

### 8.3 버전 고정 (권장)

```text
# requirements.txt — 배포명은 vm-stock-kis, import 이름은 vmkis 입니다
# major 핀 (권장)
vm-stock-kis>=1.0.0,<2.0.0

# 또는 특정 버전
vm-stock-kis==1.0.0
```

> **Stable 과 “0.x minor Breaking”을 같이 쓰지 않습니다.** 0.3.0 부터
> classifier 는 Stable 이고, 1.0.0 은 그 SemVer 약속을 번호로 고정합니다.
> 공개 API 를 깨는 변경은 major 로만 나갑니다.

### 8.4 안전한 업그레이드

```bash
# 1. 테스트 환경에서 먼저 테스트
pip install --upgrade vm-stock-kis --dry-run

# 2. 충돌 확인
pip check

# 3. 실제 업그레이드
pip install --upgrade vm-stock-kis

# 4. 버전 확인
python -c "import vmkis; print(vmkis.__version__)"

# 5. 테스트 실행
pytest tests/
```

---

## 9. 마이그레이션 가이드

### 9.1 `python-kis` → `vm-stock-kis` (0.0.1)

배포명·모듈명·클래스명이 모두 바뀌었습니다.

```python
# python-kis 2.x
from pykis import PyKis
kis = PyKis("config.yaml")

# vm-stock-kis — YAML 은 create_client. VmKis 경로는 JSON
from vmkis import create_client
kis = create_client("configs/account_profiles.yaml")

# JSON
from vmkis import VmKis
kis = VmKis("secret.json")
```

전체 대조표와 호환 폴백 목록은
[MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) 에 있습니다.

### 9.2 → 0.3.0 (완료)

호환 폴백·Stable classifier 는 **0.3.0** 에 들어갔습니다 (`#33`–`#36`).
`v1.0.0` 태그는 SemVer major 선언용이며, 아래를 다시 지우지 않습니다.

- `vmkis.PyKis` 별칭 제거 (`#33`)
- `~/.pykis` 작업공간 폴백 제거 (`#33`)
- `PYKIS_*` 환경변수 폴백 제거 (`#33`)
- `from vmkis import <내부타입>` 루트 경로 제거 (`#34`)
- `Development Status` → `5 - Production/Stable` (`#35`)

---

## 10. 버전 호환성 매트릭스

### 10.1 Python 버전 지원

`pyproject.toml` 의 `requires-python` 이 하한의 유일한 출처입니다.
CI 는 그 하한과 분류기의 최신 끝단만 검증합니다
(`.github/workflows/ci.yml` 의 test matrix). 중간 버전을 여기 나열하지
않습니다.

| Python | 0.x | 비고 |
|---|---|---|
| **하한 미만** | ❌ | 설치 불가. `__env__.py` 가 명시적으로 거부합니다 |
| **하한 ~ 분류기 최신** | ✅ | 끝단만 CI. 중간은 설치 가능 |

### 10.2 의존성 버전 호환성

실제 값은 `pyproject.toml` 의 `[project] dependencies` 가 유일한 출처입니다.
이 표는 요약이며, 어긋나면 `pyproject.toml` 이 맞습니다.

| 라이브러리 | 하한 |
|---|---|
| **requests** | >=2.32.3 |
| **pyyaml** | >=6.0 |
| **websocket-client** | >=1.8.0 |
| **cryptography** | >=43.0.0 |

---

## 11. 문제 보고 및 보안

### 11.1 보안 취약점 보고

```markdown
# 보안 취약점 발견 시:

1. GitHub Issues에 공개하지 마세요
2. security@vm-stock-kis.org 또는 private message로 보고
3. 48시간 내 응답 (목표)
4. 패치 후 공개 (조율)
```

### 11.2 버그 보고

```markdown
# GitHub Issues에서:

1. [버전 명시] vm-stock-kis==0.0.1
2. [재현 단계] 명확한 코드 예제
3. [예상] 어떻게 작동해야 함
4. [실제] 어떻게 작동하는지
```

---

## 12. FAQ

### Q1: 왜 첫 버전이 0.0.1인가요? 업스트림은 2.1.6인데요.

배포명이 다르므로(`python-kis` ↔ `vm-stock-kis`) 두 버전은 **서로 비교되지
않습니다.** 이 배포명으로는 이번이 첫 릴리스이고, 업스트림 번호를 이어받으면
실제보다 성숙해 보입니다. 다운그레이드가 아닙니다.

### Q2: 0.3.0 이후 업그레이드해도 안전한가요?

🟢 **공개 API 는 Stable 입니다.** Breaking 은 major 로만 나갑니다.
`vm-stock-kis>=1.0.0,<2.0.0` 으로 핀하세요.
0.0.x–0.2.x 구간의 “minor 도 Breaking” 서술은 그 구간에만 해당합니다.

### Q3: 1.0.0은 언제 나오나요?

**나왔습니다.** 호환 폴백 제거와 Stable classifier 는 0.3.0 에 들어갔고,
`v1.0.0` 은 SemVer major 라인을 선언하는 태그입니다.

### Q4: Breaking Change 목록을 어디서 보나요?

📋 **CHANGELOG.md** 또는 **마이그레이션 가이드** 참조

---

## 13. 참고 자료

- [Python PEP 440](https://www.python.org/dev/peps/pep-0440/) - 버전 정책
- [Semantic Versioning](https://semver.org/) - 의미론적 버전
- [Python 릴리스 정책](https://devguide.python.org/versions/) - Python 버전 지원
- [CHANGELOG.md](../../CHANGELOG.md) - 변경 기록

---

**마지막 업데이트**: 2026-09-05
**검토 주기**: 매 메이저 버전
**다음 검토**: 다음 major 준비 시
