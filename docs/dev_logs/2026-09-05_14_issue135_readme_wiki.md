# 2026-09-05 - #135 README·Wiki 포인터 개발 일지

## 작업 내용

이슈 [#135](https://github.com/visualmoney/vm-stock-kis/issues/135).
README 12행의 `2.0.0 버전 이전` 을 업스트림 `python-kis` 1.x 라고
밝혔습니다. 우리 태그 숫자는 그 줄에 박지 않았습니다.

설치 절의 「파이썬 3.11을 기준으로」는 3.10 이상으로 고쳤습니다.
Wiki Tutorial 목차는 `USER_GUIDE` · `QUICKSTART` · `examples/` ·
`EXTENDING_API` 로 바꿨습니다.

이슈 템플릿과 `contact_links` 의 Docs 는 `docs/INDEX.md` 를 가리킵니다.
Wiki Home / Tutorial 은 포인터만 남기고 위키 git 에 올렸습니다.

## 밟은 함정

`2.0.0` 문자열 전체를 금하면 README 4절 업스트림 이력이 전부
걸립니다. 혼동 문장은 `2.0.0 버전 이전` 과 `wiki/Tutorial#` 입니다.

위키에 가이드를 다시 쓰면 `#104` 입니다. 검사는 위키를 못 보므로
README·템플릿만 봅니다.

결함을 되넣을 때 `git checkout` 으로 복원하지 않습니다. 사본에서
되돌렸습니다.

## 변경 파일

- `README.md`
- `.github/ISSUE_TEMPLATE/config.yml`
- `.github/ISSUE_TEMPLATE/bug-report.yml`
- `.github/ISSUE_TEMPLATE/question.yml`
- `.github/ISSUE_TEMPLATE/feature-request.yml`
- `CHANGELOG.md`
- `tests/unit/test_readme_not_upstream_tag.py`

위키: `Home.md`, `Tutorial.md` (`vm-stock-kis.wiki`)

## 테스트 결과

관련 단위 검사는 통과했습니다. README 에 `2.0.0 버전 이전` 을
되넣으면 실패합니다.

## 다음 할 일

커밋·PR 은 요청을 기다립니다. PR 본문에 `Closes #135`.
대기열 2번은 `#136` 입니다.
