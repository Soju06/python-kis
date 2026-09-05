# 2026-08-31 - CLAUDE.md → Cursor 규칙 이전 개발 일지

## 작업 내용

Cursor 전제에서 `CLAUDE.md` 376줄을 정본에서 뺐다. Cursor는 그 파일을
공식 Rules 타입으로 적지 않으면서도 Agent 채팅에 always-on 으로 넣고
있었다. 그래서 “이미 따른다”와 “Cursor 방식이다”가 달랐다.

옮긴 자리:

| 내용 | 위치 |
|---|---|
| 이슈 트래커, next-up, 세션 시작, 문서 트리 | `AGENTS.md` |
| 파일명·프롬프트/일지 | `.cursor/rules/docs-workflow.mdc` |
| 테스트·회귀 되돌리기, #43 Mock 함정 | `.cursor/rules/tests.mdc` |
| import 불변식 | `.cursor/rules/src-invariants.mdc` → ARCHITECTURE.md §1.1 |
| 세션 종료 | `.cursor/skills/session-close/` |
| PyPI | `.cursor/skills/pypi-release/` → `PYPI_RELEASE.md` |

`CLAUDE.md` 는 삭제했다. 남기면 Cursor가 구 본문과 `AGENTS.md`를 같이
넣을 수 있다. 동결 문서의 옛 링크는 그대로 둔다.

## 변경 파일

- `AGENTS.md` — 신설, 정본
- `.cursor/rules/*.mdc` — 3개
- `.cursor/skills/session-close/SKILL.md`, `pypi-release/SKILL.md`
- `CLAUDE.md` — 삭제
- `docs/INDEX.md` — 포인터
- `docs/guidelines/AGENT_WORKFLOW_RULES.md` — 정본 링크만

## 테스트 결과

코드 변경 없음. 규칙 파일이 주입되는지는 다음 Agent 세션에서 `AGENTS.md`가
always-on 으로 보이는지로 확인한다. 이 세션은 시작 시점에 이미
`CLAUDE.md`를 붙인 상태라 여기서 재현할 수 없다.

## 밟은 함정

- PowerShell에서 `gh ... --jq '.[]|"#\(.number) ..."'` 는 이스케이프 때문에
  실패한다. `AGENTS.md` 세션 시작은 `gh issue list --label …` 만 적었다.
- `AGENT_WORKFLOW_RULES.md` 에 본문을 다시 적으면 정본이 또 갈라진다.
  링크만 바꿨다.
- 규칙에 ARCHITECTURE §1.1 을 복사하지 않았다. `@` 로 파일을 가리킨다.

## 다음 할 일

커밋·PR은 사용자 요청 시. 다음 세션에서 `CLAUDE.md` 주입이 사라졌는지
확인.
