# 2026-09-05 - 예제 자격증명 연기 실측 일지

## 작업 내용

이슈 [#157](https://github.com/visualmoney/vm-stock-kis/issues/157).
모의 `acc_paper_1`. 장중 무관 조회만. 주문·웹소켓은 시도하지 않았습니다.
시크릿은 이슈에 붙이지 않았습니다.

사전검사: `load_kis_config` 통과. paper 기본 계좌. 토큰 파일 존재.
자리표시자 아님.

## 실측 종료 코드 (출력 없음)

1차 (mkdir 고치기 전):

- `hello_world.py` 0
- `trading_hours.py` 0
- `keep_token.py` 1 — `FileExistsError` (`keep_token` 이 파일인데 `mkdir`)
- `get_balance.py` 1 — 같은 `FileExistsError`
- `get_quote.py` · `get_chart.py` · `get_orderbook.py` · `account_lookups.py` 1
  — live 토큰 발급 `EGW00133` (1분당 1회). 장 닫힘이 아님

2차 (mkdir 고친 뒤, 해시 토큰이 부모에 저장됨):

- `hello_world.py` · `trading_hours.py` · `keep_token.py` 0
- `get_quote.py` · `get_chart.py` · `get_orderbook.py` 0
- `get_balance.py` 1 — `KisAPIError` `OPSQ2000` `VTTC8434R` `INVALID_CHECK_ACNO`
- `account_lookups.py` 1 — 같은 코드, `VTTC8001R` (일별체결). `profits()` 까지 못 감

`configs/token/app_*.json` 키는 `authorization` / `expires_at` 입니다.
라이브러리 적재 형식(`access_token` …)과 다릅니다. 캐시를 못 읽고 재발급합니다.
mkdir 고친 뒤에는 해시 파일(`token_{live,paper}_*.json`)을 써서 시세는 재발급 없이 통과했습니다.

모의 `account_no` 는 8자리·`01`·실전과 다릅니다. 라이브러리는 paper `CANO` 를 씁니다.
KIS 가 그 번호를 앱과 맞지 않다고 거부했습니다. 장 닫힘이 아닙니다.

## 고친 것

- skip: `load_kis_config` 필드가 `YOUR_` 인지. 주석 `YOUR_HTS_ID` 는 무시
- `_token_cache_dir`: `.json` 파일이면 부모 디렉터리에 저장

결함 재현: 파일이 있는 자리에 `mkdir` 하면 `FileExistsError`.
고친 뒤 `test_save_cached_token_when_keep_token_is_an_existing_file` 통과.

## 변경 파일

- `tests/integration/test_examples_run_smoke.py`
- `tests/unit/test_examples_behavior.py`
- `src/vmkis/kis.py`
- `tests/unit/test_kis.py`
- `CHANGELOG.md`
- `docs/prompts/2026-09-05_36_credential_smoke.md`
- `docs/dev_logs/2026-09-05_36_credential_smoke.md`

## 다음 할 일

잔고·계좌 조회는 이 기기의 모의 `CANO` 가 KIS 검사에 걸립니다 (`OPSQ2000`).
`#157` 은 엽니다. `#33`–`#36` 은 그대로.
