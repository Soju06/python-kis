# 프롬프트 로그: CI/CD 및 테스트 스캐폴딩

## 프롬프트

- GitHub Actions CI/CD 파이프라인 구축, pre-commit 설정, 통합/성능 테스트 확대, 커버리지 90% 유지 계획 수립.

## 조치

- `.github/workflows/ci.yml`: 테스트/커버리지 아티팩트 업로드, 태그 기준 빌드 작업 추가
- `.pre-commit-config.yaml`: 기본 훅 + ruff lint/format 설정
- `tests/integration/test_examples_run_smoke.py`: 예제 스모크 테스트 추가
- `tests/performance/test_perf_dummy.py`: 성능 테스트 샘플 추가 (`pytest-benchmark` 사용)
- `pyproject.toml`: dev deps에 `pre-commit`, `ruff`, `pytest-benchmark` 추가
- `docs/developer/VERSIONING.md`: 옵션 C(포에트리 중심) 추가

## 결과

- CI 기본 파이프라인 동작 준비 완료
- 로컬에서 pre-commit 훅으로 포맷/린트 자동화 가능
- 통합/성능 테스트 확장 기반 마련
- 버저닝 문서에 Poetry 중심 개선안 제시
