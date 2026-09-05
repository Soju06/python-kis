# 2026-09-05 - #143 README 업스트림 Changelog 포인터 개발 일지

## 작업 내용

이슈 [#143](https://github.com/visualmoney/vm-stock-kis/issues/143).
README 4절에 붙여 두던 업스트림 2.1.3–1.0.2 항목을 지웠습니다.
이 배포판 이력은 `CHANGELOG.md`, 갈라진 지점은 한 줄과
MIGRATION_GUIDE, 업스트림 항목은 Releases 링크입니다.

License 는 바닥 절로 남겼습니다. 위키에 본문을 복사하지 않았습니다.

## 밟은 함정

`2.0.0` 문자열 전체를 금하면 안 됩니다. 지운 것은 `### ver ` 항목
머리입니다. `2.1.6` 은 갈라진 지점이라 README 에 남습니다.

우리 버전 숫자(`0.0.1`)를 그 줄에 다시 박지 않았습니다.

결함을 되넣을 때 `git checkout` 으로 복원하지 않습니다. 사본에서
되돌렸습니다. `### ver 2.1.3` 을 되넣으면 검사가 실패합니다.

## 변경 파일

- `README.md`
- `CHANGELOG.md`
- `tests/unit/test_readme_not_upstream_tag.py`
- `docs/prompts/2026-09-05_19_readme_changelog_pointer.md`
- `docs/dev_logs/2026-09-05_19_readme_changelog_pointer.md`

## 테스트 결과

관련 단위 검사는 통과했습니다. `### ver ` 항목을 되넣으면 실패합니다.

## 다음 할 일

커밋·PR 은 요청을 기다립니다. PR 본문에 `Closes #143`.
`#30` 은 그대로입니다.
