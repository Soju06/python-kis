# 2026-08-27 - PyPI 배포 절차

## 사용자 요청
>
> PyPI에 vm-stock-kis를 등록하는 절차를 알려줘, 처음이라서 자세하게 알려줘야해.

## 분석

- 성격: 절차 안내(문서화). 코드 변경 없음.
- 확인 사항
  - `vm-stock-kis` 이름은 PyPI/TestPyPI 모두 미등록(404) → 선점 가능
  - 빌드: hatchling + hatch-vcs, 버전은 git 태그 기반 (`v*.*.*`)
  - `.github/workflows/publish.yml` 이 이미 Trusted Publishing(OIDC) 구성
  - 현재 최신 태그 `v2.1.6`, HEAD는 태그 이후 12커밋 → 로컬 버전(`+g...`)이 붙어 PyPI 업로드 불가

## 결과

- `docs/guidelines/PYPI_RELEASE.md` 작성 (계정 준비 → Trusted Publishing 등록 →
  로컬 빌드 검증 → TestPyPI 리허설 → 태그 배포 → 사후 확인 → 함정 목록)
- 후속 정리 대상 발견: `publish.yml` 의 `{{VERSION_PLACEHOLDER}}` sed 스텝이 무의미(no-op)
