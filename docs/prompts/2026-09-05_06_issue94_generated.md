# 2026-09-05 - #94 generated/ 정리

## 사용자 요청
> #94 착수

## 분석
- `API_REFERENCE.md` 는 `#70` 이후 재생성되지 않아 옛 이름을 싣는다.
- `docs/generated/` 11개 중 생성기는 1개만 만든다. 나머지 10개는 동결 기록물.
- 완료 기준에 "현재 버전" 태그 대조가 코멘트로 얹혀 있다. `지난 판` 0.0.x 는 제외.

## 계획
1. 생성기를 돌려 `API_REFERENCE.md` 를 맞춘다
2. 가짜 생성물 10개를 `archive/docs/generated/` 로 옮긴다
3. 재생성 여부와 현재 버전 주장을 CI(pytest)가 보게 한다
4. INDEX · SKIP_PARTS 를 고친다

## 결과
- `API_REFERENCE.md` 재생성. `virtual` / `real_auth` / `PyKis` 0곳
- 가짜 생성물 10개를 `archive/docs/generated/` 로 이동
- pytest 가 생성기 일치와 "현재" 태그 대조를 본다
- `SKIP_PARTS` 에서 `generated` 제거. INDEX 설명을 정정
