# 2026-09-05 - get_balance 모의 실측

## 사용자 요청
> get_balance를 configs/account_profiles.yaml 파일을 이용하여 실측하며 (기본모드 : acc_paper1)

## 분석
- YAML 기본 계좌 이름은 `acc_paper_1` 이다. `acc_paper1` 키는 없다.
- 값은 인쇄하지 않는다. 종료 코드와 오류 이름만 남긴다.
- 주문·웹소켓·실전 잔고는 하지 않는다.

## 계획
1. `get_balance.py --config configs/account_profiles.yaml` 를 YAML 기본 계좌로 실행한다
2. 종료 코드만 기록한다

## 결과
YAML 기본 계좌는 `acc_paper_1` (`acc_paper1` 키 없음).
`get_balance.py --config configs/account_profiles.yaml` 종료 1.
`KisAPIError` `OPSQ2000` `VTTC8434R` `INVALID_CHECK_ACNO`. 값·잔고는 안 찍음.
