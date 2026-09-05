# 2026-09-05 - 머지된 PR 원격 브랜치 삭제 개발 일지

## 작업 내용

이슈 #119. `origin` 에 남아 있던 머지된 PR 헤드 14개를 지웠다.

`delete_branch_on_merge` 는 이미 `true` 였다. #116
(`docs/issue104-i18n`)은 fetch 시점에 원격에서 이미 사라져 있었다.
남은 14개는 그 설정 이전 잔여분이다.

## 밟은 함정

`git branch -r --merged origin/main` 만 보면 스쿼시 머지 브랜치가
빠진다. 그 목록에는 6개만 나왔고, 실제 잔여분은 머지된 PR
`headRefName` 대조로 14개였다. `ahead=1` 인 브랜치가 전형적인
스쿼시 잔여다.

## 남긴 것

- `main`
- `cursor/setup-cloud-agent-env-a721` — 열린 PR #118
- `draft/config-schema-v2` — 머지된 PR 없음

로컬에서 같은 이름 잔여와, 원격은 이미 없던
`chore/pypi-testpypi-job` · `docs/issue104-i18n` 도 지웠다.

## 변경 파일

- `docs/prompts/2026-09-05_01_delete_merged_pr_branches.md`
- `docs/dev_logs/2026-09-05_01_delete_merged_pr_branches.md`

코드 변경 없음.

## 테스트 결과

해당 없음. 원격 브랜치 목록으로 확인했다.

## 다음 할 일

- `next-up` 이 비어 있다. 대기열을 다시 짜는 것이 다음 세션의 첫 작업이다.
- 이 일지·프롬프트는 아직 커밋하지 않았다.
