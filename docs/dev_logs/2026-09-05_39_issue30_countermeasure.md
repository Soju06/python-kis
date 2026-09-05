# 2026-09-05 - #30 미충족 대책 일지

## 작업 내용

`#30` 동작의 자격증명 선을 시세·연결 0 으로 정했습니다.
`get_balance` · `account_lookups` 는 필수 연기에서 뺐습니다. 파일은 둡니다.

`#157` 에 skip 휴리스틱과 `keep_token` 파일 `mkdir` 수정을 같이 올립니다.
`#33`–`#36` 은 열지 않았습니다. `#155` 와 섞지 않았습니다.

## 실측 (종료 코드만)

- `hello_world` · `trading_hours` · `keep_token` 0
- `get_quote` · `get_chart` · `get_orderbook` 0
- `get_balance` · `account_lookups` 1 — `OPSQ2000` leftover. `#30` 을 막지 않음

## 변경 파일

- `tests/integration/test_examples_run_smoke.py`
- `tests/unit/test_examples_behavior.py`
- `src/vmkis/kis.py`
- `tests/unit/test_kis.py`
- `CHANGELOG.md`
- `docs/prompts/2026-09-05_39_issue30_countermeasure.md`
- `docs/dev_logs/2026-09-05_39_issue30_countermeasure.md`

## 다음 할 일

`#30` 재검사 후 닫기. `#33`–`#36` 은 `blocked` 유지.
