# 2026-09-05 - #125 머지된 PR 헤드 검사

## 사용자 요청
> #125 착수

## 분석
- 닫는 조건은 잔여를 지우는 것이 아니라 검사다.
- `git branch -r --merged` 와 로컬 `git branch -r` 은 쓰지 않는다.
- `draft/config-schema-v2` 는 머지된 PR 이 아니라서 교집합에 안 들어온다.

## 계획
1. 머지된 `headRefName` ∩ `git ls-remote --heads` 를 비교하는 검사를 넣는다
2. 결함을 집합으로 먹여 실패하는지 본다
3. 기존 test job 에서 돌게 한다 (`requires_api` 아님)

## 결과
`tests/unit/test_merged_pr_heads.py`. 오늘 보이던 5개를 먹이면 실패. 살아 있는 origin 은 통과.
