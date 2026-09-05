# 2026-08-31 - Cursor 환경에서 CLAUDE.md를 Cursor 방식으로 바꿀 수 있는지 검토

## 사용자 요청
> CLAUDE.md를 cursor 환경에서 cursor 방식으로 변경 가능한지 검토하기

## 분석
- 범위: Claude Code 겸용이 아니라 **이 Cursor 워크스페이스**에서 `CLAUDE.md`를 Project Rules / AGENTS.md / skills 로 치환 가능한지 판단.
- 근거: Cursor 공식 Rules 문서, create-rule skill, 이 세션에 `CLAUDE.md`가 always-on 으로 주입되는 사실.
- 구현·이슈 생성 없음.

## 결과
채팅 검토. 결론: Cursor 환경에서는 가능하고, 지금 동작은 "호환 주입"이지 Cursor 방식이 아님.
