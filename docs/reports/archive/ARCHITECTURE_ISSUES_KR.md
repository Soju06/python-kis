# ARCHITECTURE_ISSUES_KR.md - 이슈 및 개선 계획

**작성일**: 2025년 12월 20일
**대상**: 개발자, 아키텍트, 프로젝트 매니저
**주제**: 현재 문제점, 개선 방안, 우선순위 로드맵

---

## 4.1 해결된 이슈 (Phase 1-3 완료) ✅

### 4.1.1 ✅ 공개 API 정리 (완료됨)

**문제 (과거)**:

- 154개 export로 인한 혼란
- IDE 자동완성 노이즈
- 사용자 진입장벽 높음

**해결 (현재)**:

- ✅ `__init__.py`: 154개 → 11개로 축소 (93% 감소)
- ✅ `public_types.py`: 7개 공개 타입 별칭 생성
- ✅ Deprecation 메커니즘: `__getattr__` 구현
- ✅ 테스트: `test_public_api_imports.py` 100% 통과

**결과**: Phase 1 완료 ✅

---

### 4.1.2 ✅ types.py 중복 제거 (완료됨)

**문제 (과거)**:

- `__init__.py`와 `types.py` 중복
- 유지보수 부담 증가

**해결 (현재)**:

- ✅ `public_types.py` 신규 생성으로 구조 명확화
- ✅ 공개/내부 API 명확히 분리
- ✅ 싱크 오류 제거

**결과**: Phase 1 완료 ✅

---

### 4.1.3 ✅ 초보자 진입장벽 (완료됨)

**문제 (과거)**:

- 1-2시간 필요한 복잡한 초기 설정
- Protocol/Mixin 학습 부담

**해결 (현재)**:

- ✅ `SimpleKIS` 클래스: 딕셔너리 기반 API
- ✅ `helpers.py`: 자동 설정 함수
- ✅ QUICKSTART.md: 5분 가이드
- ✅ 예제: 8+개 (기본/중급/고급)

**결과**: Phase 2-3 완료 ✅

---

## 4.2 진행 중인 이슈 (Phase 4 진행) 🔄

### 4.2.1 🔄 모듈식 아키텍처 문서화

**진행도**: 70% (7/10 완료)

**완료된 부분**:

- ✅ ARCHITECTURE_README_KR.md (네비게이션)
- ✅ ARCHITECTURE_CURRENT_KR.md (현황)
- ✅ ARCHITECTURE_DESIGN_KR.md (설계)
- ✅ ARCHITECTURE_QUALITY_KR.md (품질)
- ✅ ARCHITECTURE_ISSUES_KR.md (이슈)
- ✅ ARCHITECTURE_ROADMAP_KR.md (로드맵)
- ✅ ARCHITECTURE_EVOLUTION_KR.md (진화)

**진행 중인 부분**:

- 🔄 GitHub Discussions 활성화
- 🔄 docs/architecture/ARCHITECTURE.md 최신화

**예정**: Phase 4 완료 시 (1주 내)

### 4.2.2 🔄 GitHub Discussions 구축

**완료됨**:

- ✅ 템플릿 3개 (question.yml, feature-request.yml, general.yml)
- ✅ 설정 가이드 (GITHUB_DISCUSSIONS_SETUP.md)

**진행 중**:

- 🔄 GitHub 저장소에서 실제 활성화
- 🔄 첫 공지 작성

**예정**: 2025-12-25

### 4.2.3 🔄 튜토리얼 영상

**완료됨**:

- ✅ 스크립트 작성 (VIDEO_SCRIPT.md, 600줄)
- ✅ 자막 및 타이밍 설정

**진행 중**:

- 🔄 YouTube 채널 개설
- 🔄 촬영 및 편집

**예정**: 2026-01-15

---

## 4.3 예정된 이슈 (Phase 5) 📅

### 4.3.1 📅 v3.0.0 Breaking Changes

**계획**:

- 공개 API 최종 정리 (20개로 확정)
- 마이그레이션 가이드 완성
- 버전 정책 확정

**기간**: 2025-12-25 ~ 2026-01-15

**담당자**: @maintainer

---

### 4.3.2 📅 dynamic.py 복잡도 개선

**문제점**:

```python
# pykis/responses/dynamic.py (400줄)
# CC=15 (권장: ≤7)
```

**개선 방안**: Strategy 패턴 도입

**우선순위**: P1 - 높음
**예상 시간**: 6-8시간
**기간**: Phase 5 (2026-01-15~)

---

### 4.3.3 📅 WebSocket 이벤트 테스트

```text

**우선순위**: P2 - 중요
**예상 시간**: 4-6시간

---

### 4.2.3 🟡 보안: 로컬 파일 권한 검증 부재

**현황**:
```python
# config.json 읽을 때
with open("config.json") as f:
    config = json.load(f)
# ⚠️ 파일 권한 검증 없음 (Windows/Linux 모두)
```

**개선 방안**:

```python
import os
import stat

# Windows
if os.name == 'nt':
    st = os.stat("config.json")
    if st.st_mode & stat.S_IRWXO:  # other 권한 있으면 경고
        logger.warning("config.json has world-readable permissions")

# Unix/Linux
else:
    st = os.stat("config.json")
    mode = st.st_mode & 0o777
    if mode != 0o600:  # 소유자 read/write만 허용
        os.chmod("config.json", 0o600)
```

**우선순위**: P2 - 중요
**예상 시간**: 1-2시간

---

## 4.3 권장 개선 사항 (Phase 6+ 고려)

### 4.3.1 🟢 Docstring 완성도 향상 (70% → 95%)

**현황**: 내부 함수 docstring 부족

**개선 방안**:

```python
# 모든 public + protected 메서드에 docstring 추가
# Google style 통일
```

**우선순위**: P3 - 권장
**예상 시간**: 2-3시간

---

### 4.3.2 🟢 엣지 케이스 테스트 강화

**추가할 테스트**:

```text
├── 네트워크 중단 시나리오
├── 부분 응답 처리
├── 대용량 데이터 처리 (100만 봉)
├── 동시성 스트레스 테스트
└── 메모리 누수 감지
```

**우선순위**: P3 - 권장
**예상 시간**: 8-12시간

---

## 4.4 개선 순서도 (Phase별)

```text
┌─────────────────────────────────────────────────────┐
│ Phase 4 (현재, 완료)                                │
│ ✅ 테스트 커버리지 92% 달성                          │
│ ✅ 타입 힌트 98% 달성                               │
│ ✅ 아키텍처 문서화 완성                             │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ Phase 5 (긴급 - v3.0.0 준비)                       │
│ ⏳ 공개 API 축소 (154 → 20개)                       │
│ ⏳ dynamic.py 리팩토링 (CC=15 → 5)                  │
│ ⏳ 주문 메서드 분해 (82줄 → 20줄 x 4)              │
│ ⏳ types.py 중복 제거                               │
│ 예상 시간: 12-16시간                               │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ Phase 6 (중요 - v3.0.1)                            │
│ ⏳ WebSocket 테스트 완성 (85% → 92%)               │
│ ⏳ 보안 강화 (파일 권한)                            │
│ ⏳ Docstring 완성 (70% → 95%)                      │
│ 예상 시간: 8-12시간                                │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ Phase 7 (최적화 - 장기)                            │
│ ⏳ 엣지 케이스 테스트                               │
│ ⏳ 성능 최적화                                      │
│ ⏳ 예제 튜토리얼 확대                               │
│ 예상 시간: 16-24시간                               │
└─────────────────────────────────────────────────────┘
```

---

## 4.5 의존성 매트릭스

```text
리팩토링 의존성:
┌──────────────────────┐
│ 공개 API 축소        │ (P0)
│ (154 → 20개)         │
└──────┬───────────────┘
       │ depends on
       ↓
┌──────────────────────┐
│ types.py 중복 제거   │ (P1)
└──────┬───────────────┘
       │ enables
       ↓
┌──────────────────────┐
│ Dynamic 리팩토링    │ (P1)
│ (CC: 15 → 5)        │
└──────────────────────┘
```

---

## 다음 단계

➡️ [로드맵 및 실행 계획 보기](ARCHITECTURE_ROADMAP_KR.md)
