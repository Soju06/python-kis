# 2026-09-05 - #125 머지된 PR 헤드 검사 개발 일지

## 작업 내용

머지된 PR head 이름과 `git ls-remote --heads` 의 교집합이 있으면
실패하는 단위 검사를 넣었습니다. `main` 은 빼며, 머지된 PR 이 없는
`draft/config-schema-v2` 는 교집합에 안 들어옵니다.

살아 있는 조회는 GitHub pulls API 와 `ls-remote` 를 씁니다. 로컬에서
둘 다 안 되면 skip 하고, `GITHUB_ACTIONS` 안에서는 skip 하지 않습니다.

## 밟은 함정

검사 파일 전체에 `"git branch" not in text` 를 걸면, 그 단언 줄이
스스로를 실패시킵니다. `_origin_heads` 의 소스만 봅니다.

오늘 아침에 보이던 5개는 이 검사를 돌리는 시점의 origin 에는 없었습니다.
닫는 조건은 지우는 것이 아니라 검사입니다.

## 변경 파일

- `tests/unit/test_merged_pr_heads.py`

## 테스트 결과

관련 단위 검사는 통과했습니다. 오늘 보이던 5개 이름을 집합으로 넣으면
실패합니다. 살아 있는 origin 조회도 통과했습니다.

## 다음 할 일

커밋·PR 은 요청을 기다립니다. PR 본문에 `Closes #125`.
