> **동결 — 2025-12 시점의 스냅샷입니다.** 원래 자리는
> `docs/generated/prompts_guide.md` 였습니다.
>
> 생성기가 만들지 않는 일회성 산출물입니다. 생성기가 만드는 것은
> `docs/generated/API_REFERENCE.md` 하나입니다.
>
> 지금 무엇을 볼 것인가 — `docs/generated/API_REFERENCE.md`, `gh issue list`.

---

**가이드 (Guide)**

- 개발 환경 준비
  - 가상환경: `python -m venv .venv` 또는 `poetry install`
  - 의존성 설치: `poetry run pip install -r requirements-dev.txt` 또는 `python -m poetry install --no-interaction --with=test`

- 테스트 실행 (권장)
  - 전체 테스트: `poetry run pytest`
  - 특정 파일: `poetry run pytest tests/integration/test_mock_api_simulation.py -q`
  - 커버리지 포함: `poetry run pytest --cov=pykis --cov-report=xml:reports/coverage.xml --cov-report=html:reports/coverage_html`

- 변경사항 적용 요령
  - 테스트가 실패하면 먼저 테스트 코드를 확인하고 PyKis API 변경(예: `virtual_auth`, `primary_token`) 반영
  - 모의 HTTP: `requests-mock`을 사용하여 응답을 모킹

- 파일/경로 요약
  - 프로젝트 루트: `pyproject.toml`, `poetry.toml`
  - 테스트 리포트: `reports/test_report.html`, `reports/coverage.xml`, `reports/coverage_html`

(필요하면 이 가이드를 상세하게 확장합니다.)
