# 2026-09-05 - 머지된 PR 원격 브랜치 삭제

## 사용자 요청
> 원격 저장소에서 PR 머지된 브랜치 삭제하는 작업을 이슈로 등록하고
> 브랜치 삭제하는 작업 진행하기

## 분석
- 작업 범위: 이슈 등록 + `origin` 에서 머지된 PR 헤드 브랜치 삭제.
- `delete_branch_on_merge` 는 이미 `true`. 최근 PR(#116 `docs/issue104-i18n`)은
  fetch 시 원격에서 이미 사라졌다. 남은 것은 설정 이전 잔여분이다.
- 스쿼시 머지 브랜치는 `git branch --merged` 에 안 잡힌다. 판정은
  **머지된 PR 의 `headRefName` 이 아직 `origin` 에 있는가** 이다.
- 남길 것: `main`, 열린 PR #118 (`cursor/setup-cloud-agent-env-a721`),
  PR 이 없는 `draft/config-schema-v2`.

## 계획
1. 잔여 브랜치 목록으로 이슈를 연다
2. `git push origin --delete` 로 원격 잔여분을 지운다
3. 같은 이름의 로컬 브랜치도 정리한다
4. 이슈를 닫고 개발 일지를 남긴다

## 결과
이슈 #119 를 열고 원격 14개를 삭제했다. 남은 원격은 `main`,
`cursor/setup-cloud-agent-env-a721`(#118), `draft/config-schema-v2` 뿐이다.
로컬 잔여 9개도 지웠다. 일지: `docs/dev_logs/2026-09-05_01_delete_merged_pr_branches.md`.
