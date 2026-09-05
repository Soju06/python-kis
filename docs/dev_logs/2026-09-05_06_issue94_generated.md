# 2026-09-05 - #94 generated/ 정리 개발 일지

## 작업 내용

`API_REFERENCE.md` 를 생성기로 다시 만들었습니다. 가짜 생성물 10개는
`archive/docs/generated/` 로 옮기고 동결 안내만 얹었습니다.

검사는 `git diff` 스텝이 아니라 pytest 입니다. 로컬에서도 더러운 트리가
없어도 돌아갑니다. 생성기는 `render()` 를 내놓고, 검사가 그 문자열과
커밋된 파일을 비교합니다.

"현재 버전"은 `git describe --tags --abbrev=0` 의 계열과 맞춥니다.
`지난 판` 줄은 건너뜁니다.

## 밟은 함정

`git tag --sort=-v:refname` 의 맨 위는 `v3.0.0rc2` 입니다. 포크 이전
태그입니다. HEAD 에서 닿는 최신은 `git describe` 가 줍니다 (`v0.1.0`).

`uv run python scripts/generate_api_reference.py` 는 샌드박스에서
`.venv` 를 다시 쓰려다 실패했습니다. 생성 자체는
`.venv/bin/python scripts/...` 로 됩니다. 검사는 스크립트를 import 하므로
파일을 다시 쓸 필요가 없습니다.

생성기가 빈 docstring 을 `- \`request()\`:\ ` 처럼 뒤에 공백을 남기고,
파일 끝에 빈 줄을 하나 더 붙입니다. pre-commit 의 trailing-whitespace 와
end-of-file-fixer 가 그걸 지운 뒤 검사가 실패합니다. `render()` 가
`rstrip() + "\\n"` 하고, 빈 설명은 `: ` 를 붙이지 않습니다.

INDEX 의 `generated/` 는 "기록물 — 갱신하지 않습니다" 칸에 있었습니다.
생성기를 돌리는 파일이 동결 칸에 있으면 설명이 거짓말입니다. 개발자 문서
표로 옮겼습니다.

재생성 레퍼런스에는 ` ```python ` 펜스가 없습니다. 시그니처 검사에
넣어도 블록이 0개입니다. 그래도 SKIP 에서 빼 둔 이유는, 나중에 펜스가
생기면 옛 이름을 보게 하기 위해서입니다.

`src/vmkis/types.py` 모듈 docstring 에 `현재(0.0.1)` 이 남아 있습니다.
살아 있는 마크다운이 아니라서 이 이슈의 검사 밖입니다.

회귀: `API_REFERENCE.md` 끝에 `<!-- stale -->` 를 붙이면
`test_api_reference_matches_the_generator` 가 실패합니다. 복원은 복사본에서
했습니다. `git checkout` 은 쓰지 않았습니다.

## 변경 파일

- `scripts/generate_api_reference.py` — `render()` 분리
- `docs/generated/API_REFERENCE.md` — 재생성
- `archive/docs/generated/2025-12_*` — 가짜 생성물 10개
- `docs/INDEX.md`, `AGENTS.md`, `archive/README.md`
- `docs/architecture/ARCHITECTURE.md` — `**버전**` 칸에서 숫자 제거
- `docs/guidelines/API_STABILITY_POLICY.md` — 출력 예제에서 숫자 제거
- `tests/unit/test_api_reference_generated.py`
- `tests/unit/test_docs_current_version.py`
- `tests/unit/test_docs_signatures.py` — `generated` SKIP 제거

## 테스트 결과

관련 단위 검사는 통과했습니다. 레퍼런스에 한 줄을 덧붙이면 실패합니다.
`0.0.x | 현재` 문자열은 잡고, `지난 판` 줄은 안 잡습니다.

## 다음 할 일

커밋·PR 은 요청을 기다립니다. PR 본문에 `Closes #94`.
