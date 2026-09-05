# 버저닝

## 원칙

버전의 유일한 출처는 **git 태그**입니다. 소스에도 `pyproject.toml`에도 버전
문자열을 적지 않습니다.

```text
git tag ──hatch-vcs──► 휠/sdist METADATA "Version:"
                            └──importlib.metadata──► vmkis.__version__ ──► USER_AGENT
```

## 구성

| 위치 | 설정 |
|---|---|
| `pyproject.toml` `[project]` | `dynamic = ["version"]` |
| `[tool.hatch.version]` | `source = "vcs"`, `fallback-version = "0.0.0"` |
| `[tool.hatch.version.raw-options]` | `version_scheme = "no-guess-dev"` |
| `[tool.uv] cache-keys` | `{ git = { commit = true, tags = true } }` |
| `src/vmkis/__env__.py` | `importlib.metadata.version("vm-stock-kis")` |

세 가지가 조용히 깨지기 쉬우니 바꾸지 마세요.

- **`_dist_version()`의 인자는 배포명(`vm-stock-kis`)입니다.** 모듈명(`vmkis`)을
  넘기면 `PackageNotFoundError`가 나고 fallback이 가짜 버전을 노출합니다.
- **`cache-keys`에 git이 없으면** 태그를 새로 만들어도 editable 설치의 버전이
  갱신되지 않습니다. uv 기본값에는 git 상태가 없습니다.
- **CI checkout에 `fetch-depth: 0`이 없으면** 태그가 없는 shallow clone이 되어
  버전이 `0.0.0`이 됩니다. `ci.yml`의 `Version sanity` 스텝이 이를 잡습니다.

## 버전 해석표

| 상황 | 버전 | 출처 |
|---|---|---|
| 태그된 커밋에서 빌드 | `0.0.1` | `git describe` |
| `v0.0.1` 이후 4커밋 | `0.0.2.dev4+g<sha>` | `no-guess-dev` |
| sdist에서 설치 (git 없음) | 태그 버전 | 빌드 시점 `PKG-INFO`에 baked |
| git 없고 미설치 | `0.0.0+unknown` | `fallback-version` / `PackageNotFoundError` |

`no-guess-dev`를 쓰는 이유는 태그 없는 커밋에서 **다음 버전을 추측하지 않기**
위해서입니다. `2.1.7.dev4+g<sha>`처럼 그럴듯한 값을 만들면 아직 존재하지 않는
릴리스를 가리키게 됩니다.

## 태그 규칙

### ① 태그는 `v` + PEP 440 정규형이며, 글자 그대로 일치해야 합니다

`publish.yml`은 태그에서 `v`만 떼어내고, 빌드된 휠 파일명에서 파싱한 버전과
**문자열 비교**를 합니다. 후자는 PEP 440 정규화를 거친 값입니다.

```bash
tag="${GITHUB_REF_NAME#v}"
if [ "$tag" != "$BUILT_VERSION" ]; then ... fi
```

정규화는 여러 표기를 같은 값으로 모으므로, 사람이 자연스럽게 쓰는 표기가
대부분 여기서 어긋납니다.

| 태그 | 정규형 | 결과 |
|---|---|---|
| `v0.0.1` | `0.0.1` | ✅ |
| `v0.0.1rc1` | `0.0.1rc1` | ✅ |
| `v0.0.1b1` | `0.0.1b1` | ✅ |
| `v0.0.1-rc1` | `0.0.1rc1` | ❌ 빌드 잡 실패 |
| `v0.0.1.rc1` | `0.0.1rc1` | ❌ |
| `v0.0.1RC1` | `0.0.1rc1` | ❌ |
| `v0.0.1-beta.1` | `0.0.1b1` | ❌ |

**`rc`/`a`/`b` 뒤에 구분자 없이 숫자만 붙이세요.** 어긋나면 게시 *전* 잡에서
막히므로 잘못된 아티팩트가 올라가지는 않지만, 태그를 지우고 다시 만들어야 합니다.

직접 확인하려면:

```console
$ uv run --with packaging python -c "from packaging.version import Version; t='0.0.1rc1'; print(str(Version(t))==t)"
True
```

### ② 사전 릴리스는 태그 표기만으로 갈립니다

`publish.yml`이 휠 버전을 `packaging` 으로 파싱해 `is_prerelease or is_devrelease`
를 판정하고, 그 결과로 업로드 대상이 정해집니다.

| 태그 | 업로드 | GitHub Release |
|---|---|---|
| `v0.0.1rc1` / `v0.0.1a1` / `v0.0.1b1` | TestPyPI | 만들지 않음 |
| `v0.0.1` | PyPI | 만듦 |

### ③ 번호는 되돌리지 않고 올립니다

PyPI도 TestPyPI도 **같은 버전의 재업로드를 영구히 거부합니다.** 파일을 지워도
그 버전 이름은 되살아나지 않습니다. 리허설을 다시 하려면 `rc2`, `rc3` 으로
올리세요.

### ④ 밀어버린 태그는 옮기지 않습니다

이미 빌드된 아티팩트와 어긋나고, 받은 사람의 `git describe` 결과가 조용히
달라집니다. 잘못 만들었으면 지우고 다시 붙이지 말고 번호를 올리세요.

### ⑤ `main` 의 CI 초록 커밋에만, annotated 로 붙입니다

```bash
git tag -a v0.0.1 -m "v0.0.1"     # -a 로 작성자와 날짜를 남깁니다
```

## 릴리스 절차

```bash
git switch main && git pull
uv run pytest -m 'not requires_api' --cov     # 로컬 확인

# 1) 리허설 — TestPyPI 로 갑니다
git tag -a v0.0.1rc1 -m "v0.0.1rc1"
git push origin v0.0.1rc1

# 2) 통과를 확인한 뒤 정식 배포 — 되돌릴 수 없습니다
git tag -a v0.0.1 -m "v0.0.1"
git push origin v0.0.1                        # publish.yml 이 실행됩니다
```

**배포물에 들어가는 파일이 바뀌었다면 리허설을 다시 하세요.** 문서만 바뀌었다면
필요 없습니다. `[tool.hatch.build.targets.sdist] include` 와
`[tool.hatch.build.targets.wheel] packages` 가 실제로 실리는 범위입니다.

```bash
git diff --stat <직전-rc-태그>..main -- src/ pyproject.toml uv.lock
```

`publish.yml`은 게시 전에 다음을 검증합니다. 하나라도 실패하면 PyPI에 올라가지
않습니다.

1. 태그와 빌드된 버전 일치
2. `twine check --strict`
3. 휠 내용 — `vmkis/py.typed` 포함, `pykis/` 부재, `tests/` 미포함
4. 격리 환경 스모크 테스트 — import, 버전, `helpers` 노출

자세한 배포 준비(계정, Trusted Publishing 등록, TestPyPI 리허설)는
[PYPI_RELEASE.md](../guidelines/PYPI_RELEASE.md)를 보세요.

## 비태그 커밋 정책

태그가 없는 커밋의 버전에는 로컬 버전 식별자(`+g<sha>`)가 붙습니다.
**PyPI는 로컬 버전이 붙은 파일을 거부합니다.** 따라서 배포는 태그가 정확히
찍힌 커밋에서만 가능합니다. 이는 의도된 제약입니다.

## 문제 해결

### 버전이 `0.0.0`으로 나온다

git 메타데이터 없이 빌드된 것입니다.

- CI라면 `actions/checkout`에 `fetch-depth: 0`이 있는지 확인하세요.
- 로컬이라면 `git tag --list`로 태그가 있는지, shallow clone(`git rev-parse --is-shallow-repository`)이
  아닌지 확인하세요.

### 태그를 만들었는데 버전이 그대로다

editable 설치의 캐시입니다. `[tool.uv] cache-keys`에 git 항목이 있는지
확인하고 `uv sync --reinstall-package vm-stock-kis`를 실행하세요.

---

이 문서는 2026-08-27에 500줄에서 축소되었습니다. 당시 삭제한 내용은
A/B/C/D 옵션 비교와, 실제로 동작한 적 없는 "현행 설계" 서술이었습니다.
의사결정 기록은 `docs/reports/`의 버저닝 검토 문서에 남아 있습니다.
