# 버전닝 검토 보고서 (2025-12-20)

## 1. 현행 요약

- 단일 소스: `pykis/__env__.__version__` (CI에서 태그로 placeholder 치환)
- 빌드 메타: `[project] dynamic` + `[tool.setuptools.dynamic]`가 `__env__.__version__`를 참조
- Poetry 메타: `tool.poetry.version` 병존(불일치 위험)
- 장점: 런타임/배포 메타 일치, 태그 드리븐 운영 가능
- 단점: 이중 경로(포에트리 vs setuptools), 치환 스크립트 유지, 태그 없을 때 버전 규칙 모호

## 2. 옵션 비교 (A/B/C/D)

- **A: setuptools-scm**
  - Git 태그에서 버전 자동 추론, 런타임 폴백(`get_version`)
  - Pros: 표준적, 단순 / Cons: Poetry 중심 워크플로우와는 별개
- **B: 현행 유지 + CI 검증**
  - Placeholder 주입 유지, 태그=아티팩트 버전 검증, 필요시 Poetry 버전 동기화
  - Pros: 변경 최소 / Cons: 스크립트 유지비, 이중관리 지속
- **C: Poetry 중심(플러그인)**
  - `poetry-dynamic-versioning` 플러그인으로 태그→Poetry 버전 자동
  - Pros: Poetry 단일 경로, 치환 제거 / Cons: 플러그인 의존, 중복 설정 시 충돌
- **D: Poetry 호환(플러그인 없음)**
  - CI에서 태그→PEP 440 정규화→`poetry version` 주입, 런타임은 배포 메타 읽기
  - Pros: 플러그인 무의존, PEP 440 준수, CI 제어 용이 / Cons: 매핑 스크립트 유지, 비태그 정책 필요

## 3. 권고안 (선택 가이드)

- 단기: **B**로 안정 운영(태그 필수, 검증 강화)하며 Phase 2 작업 지속
- 중기: 단일 경로로 정리
  - Poetry 중심이면 **C** 또는 **D** 권장(둘 중 하나만 채택)
  - 도구-중립 패키징 선호 시 **A** 권장
- 원칙: 한 경로만 사용 → 중복 제거

## 4. 구현 체크리스트 (옵션별)

### A(SETUPTOOLS-SCM)

- [ ] `pykis/__env__.py`: placeholder 제거, `importlib.metadata` + `setuptools_scm.get_version()` 폴백
- [ ] `pyproject.toml`: `[project] dynamic` 유지, `[tool.setuptools.dynamic]` 또는 SCM 기본 설정 사용
- [ ] `tool.poetry.version` 제거(또는 비관리 명시)
- [ ] CI: 태그 릴리스만 빌드, 치환 스텝 제거

### B(현행 유지)

- [ ] CI: 태그 파싱→`__env__.py` 치환→빌드
- [ ] CI: 산출물 버전=태그 검증 단계 추가
- [ ] (선택) Poetry 버전 자동 동기화 커밋 또는 비관리 명시

### C(Poetry 플러그인)

- [ ] 플러그인 설치/설정(`poetry-dynamic-versioning`)
- [ ] `pykis/__env__.py`: `importlib.metadata.version("python-kis")`로 단순화
- [ ] `pyproject.toml`: `[tool.poetry]` 버전 placeholder, `[tool.poetry-dynamic-versioning]` 활성
- [ ] 중복 경로 제거: `[tool.setuptools.dynamic]` 제거
- [ ] CI: 태그 릴리스만 빌드, 치환 스텝 제거

### D(Poetry, 플러그인 없음)

- [ ] CI: 태그→PEP 440 정규화→`poetry version` 주입
- [ ] `pykis/__env__.py`: `importlib.metadata.version()`로 단순화
- [ ] 태그 규칙 문서화(PEP 440 매핑표)
- [ ] 비태그 정책 정의(배포 금지 또는 `.devN`)

## 5. 불필요 코드/설정 제거 지침

- **C 채택 시**: `[tool.setuptools.dynamic]` 경로 삭제, placeholder 치환 스크립트 삭제
- **A 채택 시**: `tool.poetry.version` 삭제 또는 비관리 명시, CI 치환 단계 삭제
- **D 채택 시**: placeholder 치환 삭제, SCM 동적 버전 경로 미사용, CI 매핑 스크립트만 유지

## 6. 사용자 선택 후 실행 플로우

- 1) 옵션 선택 (A/B/C/D)
- 1) 체크리스트대로 수정/삭제 수행
- 1) CI 파이프라인 업데이트 및 태그 릴리스 테스트
- 1) 문서 업데이트(VERSIONING.md, RELEASE.md)

## 7. 다음 할 일(To-Do)

- [ ] 옵션 최종 선택 (A/B/C/D)
- [ ] 선택안에 따른 코드/설정 정리 및 CI 업데이트
- [ ] 태그 릴리스 e2e 검증(테스트+아티팩트 확인)
- [ ] 커버리지 임계치 적용(`--cov-fail-under=90`) 및 테스트 확대
