# 2026-08-31 - CLAUDE.md를 Cursor 규칙으로 이전

## 사용자 요청
> 이전(migration) 승인

## 분석
- 작업 범위: `CLAUDE.md` 정본을 `AGENTS.md` + `.cursor/rules/*.mdc` + `.cursor/skills/` 로 옮기고, Cursor 전용이므로 `CLAUDE.md` 삭제.
- 동결 문서(`docs/dev_logs/`, `docs/reports/`, 옛 prompts)의 `CLAUDE.md` 링크는 손대지 않음.
- 이슈 없음. 커밋은 사용자가 요청할 때만.

## 계획
1. `AGENTS.md`에 불변식
2. glob 규칙 3개, skill 2개
3. 살아 있는 포인터만 고치고 `CLAUDE.md` 삭제
4. 개발 일지

## 결과
이전 완료. 정본은 `AGENTS.md`.
