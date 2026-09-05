# 2026-08-27 - PyPI 배포 파이프라인 정비 개발 일지

## 작업 내용

PyPI 최초 배포를 위한 절차 문서화와, TestPyPI 리허설 경로를 워크플로에 추가했습니다.

### 1. 배포 가이드 작성

`docs/guidelines/PYPI_RELEASE.md` 신규 작성. 계정 준비 → Trusted Publishing 등록 →
로컬 빌드 검증 → TestPyPI 리허설 → 태그 배포 → 사후 확인 → 함정 목록.

작성 과정에서 확인한 사실:

- `vm-stock-kis` 는 PyPI/TestPyPI 모두 미등록(404) → 선점 가능
- PyPI **계정 사용자명**은 ASCII만 허용(영문자·숫자·`.`·`-`·`_`, 시작/끝은 영숫자).
  변경 불가.
- **배포명**도 ASCII만 허용. 한글 배포명은 PyPI 이전에 hatchling이 거부:
  `Not a valid package or extra name: "브이엠주식"`
- **저자명(`authors`)은 UTF-8 자유 형식**이라 한글 가능. 실제로 빌드해 확인:
  `Author-email: "서원호 (Wonho Seo)" <...>` 가 그대로 기록되고 `twine check` 통과,
  표준 이메일 파서로 되읽어도 표시명/주소가 정확히 분리됨.
  (실사례: PyPI의 `pypinyin` 은 `author='mozillazg, 闲耘'`)
- 2FA 활성화는 **복구 코드가 선행 조건**. warehouse 소스 기준
  `RECOVERY_CODE_COUNT = 8` 이고, 8개 중 1개를 입력해 저장 여부를 확인하며
  그 코드는 `burned` 처리되어 재사용 불가(실사용 가능 코드는 7개로 남음).
  `totp_provision` 뷰가 `has_burned_recovery_codes` 를 확인해 미완료면
  복구 코드 화면으로 되돌림.
- "대기(pending)" 게시자 등록은 **이름을 예약하지 않음** (PyPI 안내문 명시).

### 2. TestPyPI 잡 추가

`.github/workflows/publish.yml` 에 사전 릴리스 라우팅을 도입했습니다.

- `build` 잡에 `Version info` 스텝 추가. 휠 파일명을 `packaging.utils.parse_wheel_filename`
  으로 파싱해 `version` / `prerelease` 를 잡 출력으로 노출.
  문자열 매칭 대신 PEP 440 파서를 쓴 이유는 `rc`/`a`/`b`/`.dev` 표기를 모두
  정확히 구분해야 하기 때문입니다.
- `publish-testpypi` 잡 신규. environment `testpypi`, OIDC,
  `repository-url: https://test.pypi.org/legacy/`.
- `publish` 잡 조건에 `needs.build.outputs.prerelease == 'false'` 추가.

결과적으로 태그 하나로 대상이 갈립니다.

| 태그 | 업로드 대상 | GitHub Release |
|------|-------------|----------------|
| `v2.2.0rc1` / `v2.2.0a1` / `v2.2.0b1` | TestPyPI | 생성 안 함 |
| `v2.2.0` | PyPI | 생성 |

두 업로드 잡 모두 `startsWith(github.ref, 'refs/tags/')` 를 유지합니다.
브랜치 빌드는 hatch-vcs가 로컬 버전 식별자(`+g1234abc`)를 붙이고 인덱스가 이를 거부하므로,
태그 없는 업로드 시도 자체를 막습니다.

## 변경 파일

- `.github/workflows/publish.yml` - `Version info` 스텝, `publish-testpypi` 잡 추가,
  `publish` 잡 조건에 정식 릴리스 판정 추가
- `docs/guidelines/PYPI_RELEASE.md` - 신규
- `docs/prompts/2026-08-27_pypi_publish.md` - 신규
- `docs/dev_logs/2026-08-27_pypi_release_pipeline.md` - 신규(본 문서)

## 검증 결과

- `actionlint` (pre-commit): Passed
- `Version info` 스텝을 로컬에서 CI와 동일한 형태로 실행 →
  `version=2.1.6.post1.dev13+ga60f35083.d20260827` / `prerelease=true` 정상 출력
- prerelease 판정 로직 표본 검증

  | 입력 버전 | 판정 |
  |-----------|------|
  | `2.2.0` | false |
  | `2.2.0rc1` / `2.2.0a1` / `2.2.0b2` / `2.2.0.dev1` | true |
  | `2.1.6.post1.dev5+g11ea7787f` | true |
  | `2.2.0.post1` | false |

- 한글 저자명 메타데이터 왕복 검증 (별도 probe 패키지, `twine check` 통과)

## 다음 할 일

- [ ] PyPI / TestPyPI 각각에 대기 게시자 등록
      (Owner `visualmoney`, Repo `vm-stock-kis`, Workflow `publish.yml`,
       Environment `pypi` / `testpypi`)
- [ ] GitHub 저장소에 `pypi`, `testpypi` 환경 생성 (`pypi` 는 승인자 지정 권장)
- [ ] `v2.2.0rc1` 태그로 TestPyPI 리허설
- [ ] 리허설 통과 후 `v2.2.0` 정식 배포
- [ ] (선택) `pyproject.toml` 의 저자명을 `visualmoney` → `서원호` 로 변경할지 결정
