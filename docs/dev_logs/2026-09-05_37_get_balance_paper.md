# 2026-09-05 - get_balance 모의 실측 일지

## 작업 내용

이슈 [#157](https://github.com/visualmoney/vm-stock-kis/issues/157).
`examples/01_basic/get_balance.py --config configs/account_profiles.yaml`.
환경변수 `VMKIS_ACCOUNT` 는 비움. YAML `default_account` 사용.

파일에 `acc_paper1` 키는 없고 기본은 `acc_paper_1` 입니다.

## 실측

종료 1. `KisAPIError` `OPSQ2000` `VTTC8434R` `INVALID_CHECK_ACNO`.
stdout 없음. 잔고·계좌번호는 적지 않습니다.

장 닫힘이 아닙니다. 모의 앱이 그 계좌번호를 거부했습니다.
