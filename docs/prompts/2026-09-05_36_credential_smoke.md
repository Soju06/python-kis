# 2026-09-05 - 예제 자격증명 연기 실측

## 사용자 요청
> 계획 승인하고 이슈 작업 착수. 장중과 무관한 모의 조회만.

## 분석
- `#154` 겉면은 머지됨. 남은 것은 `RUN_INTEGRATION=1` 실측.
- 모의 `acc_paper_1`. 주문·웹소켓은 시도하지 않는다.
- `_filled_config` 가 파일 문자열의 `YOUR_HTS_ID` 로 skip 할 수 있다.
- `#33`–`#36` 안 염. 시크릿을 이슈·커밋에 넣지 않는다.

## 계획
1. 부모 `#30` 이슈를 연다
2. `load_kis_config` 사전검사 (값 인쇄 금지)
3. skip 휴리스틱을 필드 값으로 고친다
4. 장중 무관 모의 읽기를 돌리고 종료 코드만 남긴다

## 결과
`#157`. 사전검사 통과. skip·mkdir 고침. 2차: hello_world · trading_hours · keep_token · get_quote · get_chart · get_orderbook 0.
get_balance · account_lookups 1 — `OPSQ2000` `INVALID_CHECK_ACNO` (장 닫힘 아님). 주문·웹소켓 안 함. `#33`–`#36` 안 염.
