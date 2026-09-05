# vm-stock-kis 개발환경 설정 가이드

이 프로젝트는 [uv](https://docs.astral.sh/uv/)를 씁니다. Poetry는 더 이상
사용하지 않습니다.

기여 절차 전반은 [CONTRIBUTING.md](../../CONTRIBUTING.md)를 보세요.
이 문서는 환경 구축만 다룹니다.

## 1. 필수 소프트웨어

- **Python 3.10 이상** (`requires-python = ">=3.10"`).
  직접 설치하지 않아도 됩니다 — uv가 `.python-version`을 보고 알아서 받아옵니다.
- **Git**
- VS Code (권장)

## 2. uv 설치

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 3. 저장소 복제 및 의존성 설치

```bash
git clone https://github.com/visualmoney/vm-stock-kis.git
cd vm-stock-kis
uv sync --group dev
```

`uv sync`가 `.venv`를 만들고 Python 인터프리터까지 챙깁니다.
`.python-version`(현재 `3.10`)이 기본 인터프리터를 정합니다.

> **얕은 복제(shallow clone)를 하지 마세요.** 버전을 git 태그에서 만들기 때문에
> 태그가 없으면 `0.0.0`이 됩니다. 자세한 내용은
> [VERSIONING.md](../developer/VERSIONING.md)를 보세요.

## 4. pre-commit 훅 설치 (필수)

```bash
uv run pre-commit install
```

**선택이 아닙니다.** 구문 오류가 있는 파일과 파싱되지 않는 워크플로가 커밋되어
CI가 8개월간 단 한 잡도 실행하지 못한 적이 있습니다. 훅이 그것을 막습니다.

## 5. VS Code 설정

- 권장 확장은 `.vscode/extensions.json`에 있습니다.
- `Python: Select Interpreter` → `.venv` 경로 선택
- `.vscode/tasks.json`에 sync / test / coverage / build / pre-commit 태스크가 있습니다.

## 6. 테스트 실행

```bash
# CI와 동일한 조건 (실 API 자격증명이 필요한 테스트 제외)
uv run pytest -m 'not requires_api'

# 커버리지 포함
uv run pytest -m 'not requires_api' --cov --cov-report=html:htmlcov

# 특정 파일만
uv run pytest tests/unit/responses/test_dynamic_transform.py -q

# 이름으로 좁히기
uv run pytest -k <testname> -q
```

커버리지 임계값은 `pyproject.toml`의 `[tool.coverage.report] fail_under`를 따릅니다.

## 7. 코드 스타일

`ruff`가 린트와 포맷을 모두 담당합니다. `black`과 `isort`는 제거했습니다 —
black의 기본 88자가 `[tool.ruff] line-length = 120`과 충돌했습니다.

```bash
uv run ruff check --fix .
uv run ruff format .
```

pre-commit을 설치했다면 커밋 시 자동으로 실행됩니다.

## 8. 빌드

```bash
uv build
```

버전은 git 태그에서 나옵니다. 배포 절차는
[PYPI_RELEASE.md](./PYPI_RELEASE.md)를 보세요.

## 9. 문제 해결

| 증상 | 조치 |
|---|---|
| 의존성이 꼬임 | `.venv` 삭제 후 `uv sync --group dev` |
| `uv.lock`이 어긋남 | `uv lock` (CI는 `uv lock --check`로 검증합니다) |
| 버전이 `0.0.0` | 태그 없이 빌드된 것. `git fetch --tags` 후 재시도 |
| 태그를 만들었는데 버전이 그대로 | `uv sync --reinstall-package vm-stock-kis` |
