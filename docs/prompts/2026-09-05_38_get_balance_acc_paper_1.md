# 2026-09-05 - get_balance acc_paper_1 재실측

## 사용자 요청
> acc_paper_1 로 해서 실측 다시

## 분석
- `get_balance.py --config configs/account_profiles.yaml --account acc_paper_1`
- 값·잔고는 인쇄하지 않는다. 종료 코드와 오류 이름만.

## 계획
1. 위 명령으로 실행한다
2. 종료 코드만 기록한다

## 결과
`--account acc_paper_1` 종료 1. `KisAPIError` `OPSQ2000` `VTTC8434R` `INVALID_CHECK_ACNO`. 잔고 없음.
