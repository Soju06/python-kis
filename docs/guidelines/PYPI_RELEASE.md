# PyPI 배포 가이드 (vm-stock-kis)

**작성일**: 2026-08-27 · **갱신**: 2026-09-05 (`0.3.0` 게시 이후)
**대상**: 릴리스 담당자
**전제**: 이 저장소는 `hatchling` + `hatch-vcs` 로 빌드하며, **버전은 git 태그에서 자동 생성**됩니다.

---

## 0. 사전 확인 (현재 저장소 상태)

| 항목 | 상태 |
|------|------|
| 배포명 | `vm-stock-kis` — PyPI·TestPyPI **등록됨** ([PyPI](https://pypi.org/project/vm-stock-kis/)) |
| 임포트명 | `vmkis` (`src/vmkis`) |
| 빌드 백엔드 | `hatchling` (`pyproject.toml`) |
| 버전 소스 | git 태그 (`[tool.hatch.version] source = "vcs"`) |
| 배포 워크플로 | `.github/workflows/publish.yml` (태그 `v*.*.*` push 시 실행) |
| 인증 방식 | Trusted Publishing (OIDC) — `pypa/gh-action-pypi-publish`, `permissions: id-token: write` |

> **중요**: 버전이 태그에서 나오므로, **태그가 정확히 찍힌 커밋에서만** PyPI에 올릴 수 있는
> 버전(`1.0.0`)이 나옵니다. 태그 이후 커밋에서 빌드하면
> `0.3.0.post1.dev5+g11ea7787f` 처럼 **로컬 버전 식별자(`+...`)** 가 붙고,
> **PyPI는 로컬 버전이 붙은 파일을 거부**합니다.

게시된 태그·노트는 GitHub Releases 와 [CHANGELOG.md](../../CHANGELOG.md) 를 보세요.
다음 major 는 `v1.0.0` 태그 세션에서 찍습니다 ([PYPI skill](../../.cursor/skills/pypi-release/SKILL.md)).

---

## 1. 계정 준비 (최초 1회)

1. **PyPI 계정 생성**: <https://pypi.org/account/register/>
2. **TestPyPI 계정 생성**: <https://test.pypi.org/account/register/>
   - PyPI와 **별개 계정**입니다. 비밀번호/2FA를 따로 설정해야 합니다.
3. **2FA 활성화 (필수)**: PyPI는 모든 업로드 계정에 2FA를 요구합니다.
   - Account settings → Two factor authentication → TOTP 앱(예: Google Authenticator) 등록
   - **복구 코드는 반드시 별도 보관**하세요. 분실 시 계정 복구가 매우 번거롭습니다.

---

## 2. Trusted Publishing 등록 (권장, 토큰 불필요)

API 토큰을 저장소 시크릿에 넣지 않고, GitHub Actions가 OIDC로 신원을 증명하는 방식입니다.
이 저장소의 `publish.yml`은 이미 이 방식으로 작성되어 있습니다.

### 2-1. PyPI 쪽 (이미 등록된 프로젝트)

프로젝트가 **없을 때만** pending publisher 를 씁니다. `vm-stock-kis` 는 이미
게시됐으므로 <https://pypi.org/manage/project/vm-stock-kis/settings/publishing/>
에서 Trusted Publisher 가 `visualmoney/vm-stock-kis` · `publish.yml` · `pypi`
환경과 맞는지 확인하면 됩니다.

최초 선점 때 쓰던 pending 표 (참고):

| 필드 | 값 |
|------|-----|
| PyPI Project Name | `vm-stock-kis` |
| Owner | `visualmoney` |
| Repository name | `vm-stock-kis` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

> Environment name은 워크플로의 `environment: name: pypi` 와 **문자 그대로 일치**해야 합니다.

### 2-2. TestPyPI 쪽

TestPyPI는 PyPI와 완전히 분리된 시스템입니다. 계정·2FA·게시자 등록을 모두 따로 해야 합니다.

<https://test.pypi.org/manage/account/publishing/> → GitHub 탭 → **Add a new pending publisher**:

| 필드 | 값 |
|------|-----|
| PyPI Project Name | `vm-stock-kis` |
| Owner | `visualmoney` |
| Repository name | `vm-stock-kis` |
| Workflow name | `publish.yml` |
| Environment name | `testpypi` |

Workflow name은 **파일명만** 넣습니다(`.github/workflows/publish.yml` 아님).
네 값은 GitHub Actions가 OIDC 토큰에 담아 보내는 값과 글자 단위로 대조되며,
하나라도 어긋나면 업로드 시 `403 Forbidden`이 납니다.

> "대기(pending)" 등록은 **이름을 예약해 주지 않습니다.** PyPI 안내문에 명시돼 있습니다 —
> *"Configuring a 'pending' publisher for a project name does not reserve that name."*

### 2-3. GitHub 저장소 쪽

Settings → Environments → **New environment** 로 **두 개**를 만듭니다.

| 환경 이름 | 용도 | 워크플로 잡 |
|-----------|------|-------------|
| `testpypi` | 리허설 | `publish-testpypi` |
| `pypi` | 실제 배포 | `publish` |

- (선택) Deployment branches/tags 를 `v*` 태그로 제한
- (선택) `pypi` 에 Required reviewers 를 지정하면 태그 push 후 수동 승인 단계가 생깁니다.
  첫 배포라면 권장합니다. `testpypi` 는 리허설이므로 승인 없이 두는 편이 편합니다.

---

## 3. 로컬에서 빌드 검증 (업로드 전 필수)

```bash
# 작업 트리를 깨끗하게
git status --porcelain     # 출력이 비어 있어야 함

rm -rf dist/
uv build                   # 또는: python -m build
ls dist/
# vm_stock_kis-<version>-py3-none-any.whl
# vm_stock_kis-<version>.tar.gz

# 메타데이터 검증
uvx twine check dist/*     # PASSED 두 줄이 나와야 함
```

### 설치 스모크 테스트 (격리 환경)

```bash
uv venv /tmp/vmkis-smoke
VIRTUAL_ENV=/tmp/vmkis-smoke uv pip install dist/vm_stock_kis-*.whl
VIRTUAL_ENV=/tmp/vmkis-smoke /tmp/vmkis-smoke/bin/python -c \
  "import vmkis; print(vmkis.__version__)"
```

sdist가 실제로 빌드되는지도 확인합니다(누락된 파일 탐지):

```bash
uv venv /tmp/vmkis-sdist
VIRTUAL_ENV=/tmp/vmkis-sdist uv pip install dist/vm_stock_kis-*.tar.gz
```

---

## 4. TestPyPI 리허설 (강력 권장)

PyPI는 **같은 버전 번호를 재업로드할 수 없고, 삭제해도 그 번호는 영구히 재사용 불가**입니다.
그래서 실수를 여기서 다 소진합니다.

### 어떻게 갈리는가

`publish.yml` 은 빌드된 버전이 PEP 440 사전 릴리스인지 보고 업로드 대상을 결정합니다.

| 태그 | 판정 | 업로드 대상 | GitHub Release |
|------|------|-------------|----------------|
| `v1.0.0rc1`, `v1.0.0a1`, `v1.0.0b1` | 사전 릴리스 | **TestPyPI** | 생성 안 함 |
| `v1.0.0` | 정식 | **PyPI** | 생성 |

두 잡 모두 `startsWith(github.ref, 'refs/tags/')` 조건이 있습니다. 브랜치에서 빌드하면
hatch-vcs가 로컬 버전 식별자(`+g1234abc`)를 붙이고 인덱스가 그런 파일을 거부하므로,
**태그가 있어야만** 업로드가 일어납니다.

### 실행

```bash
git tag -a v1.0.0rc1 -m "TestPyPI rehearsal"
git push origin v1.0.0rc1
```

Actions 탭에서 `Build & verify` → `Publish to TestPyPI` 가 도는 것을 확인합니다.
실제 배포와 **완전히 같은 경로**(빌드 → 태그/버전 일치 검사 → `twine check --strict` →
휠 내용 검사 → 격리 스모크 테스트 → OIDC 업로드)를 밟으므로, 여기서 통과하면
정식 태그에서 새로 실패할 여지가 거의 없습니다.

### 설치 확인

의존성은 **실제 PyPI에서** 받아야 합니다(TestPyPI에는 없음):

```bash
uv venv /tmp/vmkis-test
VIRTUAL_ENV=/tmp/vmkis-test uv pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  vm-stock-kis
```

프로젝트 페이지에서 README 렌더링을 눈으로 확인합니다:
<https://test.pypi.org/project/vm-stock-kis/>

### 정리

리허설 태그는 남겨도 무해하지만, 지우려면 원격까지 지웁니다:

```bash
git push --delete origin v1.0.0rc1
git tag -d v1.0.0rc1
```

> 태그 형식 주의: `v1.0.0-rc1` 처럼 붙임표를 쓰면 PEP 440 정규화 결과가 `1.0.0rc1` 이 되어
> "Tag matches built version" 검사에서 문자열 비교가 실패합니다. **`v1.0.0rc1`** 형태로 쓰세요.

## 5. 실제 배포

```bash
# 1) main 최신화
git checkout main && git pull

# 2) CI 통과 확인 (테스트/린트/커버리지)

# 3) 태그 생성 및 push  → publish.yml 이 자동 실행됨
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

이후 GitHub → Actions → **"Publish"** 워크플로에서 진행 상황을 봅니다.
잡은 `Build & verify` → `Publish to PyPI` → `GitHub Release` 순으로 이어집니다.
`pypi` 환경에 승인자를 걸어 두었다면 `Publish to PyPI` 앞에서 멈추므로 **Approve** 를 눌러야 합니다.

`GitHub Release` 잡이 릴리스 노트를 자동 생성하고 sdist/wheel을 첨부하므로,
6절의 "GitHub Releases 에 릴리스 노트 작성"은 자동으로 처리됩니다.

수동 업로드가 필요한 경우(워크플로를 못 쓰는 상황):

```bash
uvx twine upload dist/*     # username: __token__ / password: pypi-...
```

---

## 6. 배포 후 확인

```bash
uv venv /tmp/vmkis-prod
VIRTUAL_ENV=/tmp/vmkis-prod uv pip install vm-stock-kis
VIRTUAL_ENV=/tmp/vmkis-prod /tmp/vmkis-prod/bin/python -c \
  "import vmkis; print(vmkis.__version__)"
```

- 프로젝트 페이지: <https://pypi.org/project/vm-stock-kis/>
- GitHub Releases 에 릴리스 노트 작성
- `docs/dev_logs/` 에 배포 일지 기록

---

## 7. 자주 걸리는 함정

| 증상 | 원인 / 해결 |
|------|-------------|
| `400 Bad Request: ... local version label` | 태그가 안 찍힌 커밋에서 빌드함. 정확한 태그 커밋에서 다시 빌드 |
| `403 Forbidden` (Trusted Publishing) | pending publisher의 owner/repo/workflow/environment 중 하나가 불일치 |
| `400 File already exists` | 그 버전은 영구히 사용 불가. 버전을 올려서 다시 배포 |
| README가 깨짐 | `twine check` 로 사전 검증. `readme = "README.md"` 이므로 GFM 확장 문법 주의 |
| 버전이 `0.0.0` | git 메타데이터 없이 빌드됨(shallow clone/tarball). `fetch-depth: 0` 필요 |
| 이름이 선점됨 | 다른 배포명을 쓰거나 소유권 이전을 협의 |

---

## 8. 워크플로 잡 구성 요약

`.github/workflows/publish.yml`

| 잡 | 조건 | 하는 일 |
|----|------|---------|
| `Build & verify` | 항상 | `uv build` → 태그/버전 일치 검사 → `twine check --strict` → 휠 내용 검사(`py.typed` 존재, 옛 `pykis/`·`tests/` 미포함) → 격리 환경 import 스모크 테스트 → 아티팩트 업로드 |
| `Publish to TestPyPI` | 태그 **and** 사전 릴리스 | environment `testpypi`, OIDC로 TestPyPI 업로드 |
| `Publish to PyPI` | 태그 **and** 정식 릴리스 | environment `pypi`, OIDC로 PyPI 업로드 |
| `GitHub Release` | `Publish to PyPI` 성공 시 | 릴리스 생성 + dist 첨부 (`--generate-notes`) |

사전 릴리스 판정은 `Version info` 스텝이 휠 파일명을 PEP 440으로 파싱해
`is_prerelease or is_devrelease` 로 결정하고, 잡 출력 `prerelease` 로 전달합니다.
문자열 매칭이 아니므로 `rc`/`a`/`b`/`dev` 표기를 모두 정확히 구분합니다.
