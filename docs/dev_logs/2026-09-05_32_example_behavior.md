# 2026-09-05 - 예제 동작 테스트 개발 일지

## 작업 내용

`#30` 의 「동작」을 검사로 나눴습니다.

- 단위: 컴파일, `01_basic` 의 `create_client`, `--help` 0, 없는 설정은
  경로를 말하고 0 이 아님
- 통합: 채운 `account_profiles.yaml` + `RUN_INTEGRATION=1`. 템플릿으로
  돌리던 연기를 없앰

스텁을 되넣으면 `test_basic_example_calls_create_client` 가 실패합니다.
옛 연기 경로 `template_account_profiles.yaml` 을 되넣으면
`test_integration_smoke_does_not_point_at_the_template` 가 실패합니다.

## 밟은 함정

통합 연기가 추적 템플릿을 `--config` 로 넘기고 있었습니다. 자리표시자라
연기가 아닙니다.

`--help` 가 argparse 보다 먼저 끝나므로 시그니처 결함은 못 잡습니다.
그건 기존 AST 검사가 합니다.

## 변경 파일

- `tests/unit/test_examples_behavior.py`
- `tests/integration/test_examples_run_smoke.py`
- `docs/prompts/2026-09-05_32_example_behavior.md`
- `docs/dev_logs/2026-09-05_32_example_behavior.md`

## 테스트 결과

단위 통과. 통합 읽기 8건은 `RUN_INTEGRATION` 없어 skip.

## 다음 할 일

`#30` 은 엽니다. 자격증명 연기는 로컬에서 `RUN_INTEGRATION=1`.
`#33`–`#36` 은 그대로.
