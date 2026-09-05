# 2026-08-31 - Cursor 방식으로 변경 가능한지 검토

## 사용자 요청
> cursor 방식으로 변경가능한지 검토

## 분석
- 작업 범위: `CLAUDE.md`(376줄) + `docs/guidelines/AGENT_WORKFLOW_RULES.md`를 Cursor 규칙 체계(AGENTS.md, `.cursor/rules/*.mdc`, skills)로 옮길 수 있는지 **판단만**. 구현은 요청 없음.
- 예상 시간: 검토 1회
- 영향 받는 모듈: 문서/에이전트 안내만. 런타임 코드 없음.

## 계획
1. Cursor 규칙 형식(`.mdc`, AGENTS.md, skills)과 현재 `CLAUDE.md`를 대조
2. 이미 Cursor가 `CLAUDE.md`를 읽는 사실과, 정본 이중화 위험을 적기
3. 옮길 수 있는 것 / 항상 켜 두면 안 되는 것을 분리해 권고안을 내기

## 결과
채팅에 검토 본문. 구현·이슈 생성은 하지 않음.
