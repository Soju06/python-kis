# 2026-08-28 - CLAUDE.md 작업 상태 관리 규칙 개정 개발 일지

**대상**: `CLAUDE.md` · `docs/guidelines/AGENT_WORKFLOW_RULES.md`
**선행**: [PR #54](https://github.com/visualmoney/vm-stock-kis/pull/54) To-Do 아카이브 ·
[PR #56](https://github.com/visualmoney/vm-stock-kis/pull/56) Discussions 폐지

---

## 요약

```text
CLAUDE.md   269줄 -> 376줄
삭제한 규칙  To-Do List 작성(3곳) · Phase별 문서 요구사항(절 전체)
신설한 절    작업 상태는 어디에 사는가 · 세션 시작 시
정정한 사실  존재하지 않는 경로 4개 · apply_patch · coverage_html
```

**규칙 문서 자체가 코드에 대해 사실이 아닌 것을 말하고 있었습니다.**

---

## 1. 왜 이 개정이 필요했나

`CLAUDE.md` 전문 269줄에 **"이슈", "GitHub", "PR", "라벨" 이 한 번도 나오지
않았습니다.** 새 세션의 AI 는 이 문서만 읽으면 **작업 상태가 마크다운에
있다고 결론짓습니다.** 실제로 그렇게 해서 116줄짜리 복제본이 생겼습니다.

| 위치 | 무엇이 문제였나 |
|---|---|
| 108행 | `3. To-Do List 작성` — 그 문서는 전날 아카이브됨 |
| 216~233행 | `Phase별 문서 요구사항` — Phase 1~4 는 2025-12 종료 |
| 254행 | `To-Do List 작성 (다음 Phase용)` — 위 둘의 결합 |

Phase 폐기의 근거는 실측했습니다.

```console
$ git log --since=2026-01-01 --oneline | wc -l
47
$ git log --since=2026-01-01 --oneline | grep -ci phase
0
```

47건 중 Phase 표기 **0건**입니다. 그런데 "Phase 완료 시 완료 보고서" 규칙이
만든 산출물 4건(`PHASE2_WEEK3-4_STATUS.md`, `PHASE4_WEEK1_COMPLETION_REPORT.md`,
`PHASE4_WEEK3_COMPLETION_REPORT.md`, `TASK_PROGRESS.md`)은 동결된 채 남아
있습니다.

---

## 2. 착수 전에 드러난 것 — 문서가 자기 규칙을 어기고 있었습니다

문서 체계 트리 바로 위에 이렇게 적혀 있습니다.

> 아래는 **실제 존재하는 파일**만 적습니다. 없는 문서를 참조하면 그것을 믿고
> 찾다가 시간을 버립니다.

그 아래 트리가 **존재하지 않는 경로 4개**를 가리켰습니다.

```text
docs/reports/ARCHITECTURE_REPORT_V3_KR.md   없음
docs/reports/DEVELOPMENT_REPORT_*.md        없음
docs/user/QUICKSTART.md                     없음  (실제: USER_GUIDE.md, EXTENDING_API.md, en/)
docs/user/TUTORIALS.md                      없음
```

**이 저장소가 세 번 고친 결함**(#25 존재하지 않는 배포명 · #29 포크 이전
절대경로 · #31 존재하지 않는 라벨)과 같은 것이, 그 결함을 경고하는 문서
안에 있었습니다.

정정하면서 트리에 **왜 틀렸었는지**를 남겼습니다. 다음 사람이 트리를 고칠 때
`ls` 를 하도록 만드는 것이 목적입니다.

---

## 3. `AGENT_WORKFLOW_RULES.md` 의 사실 오류 2건

| 문장 | 검증 |
|---|---|
| "파일 편집은 패치 기반(`apply_patch`)으로 수행" | `git grep apply_patch` → **이 문서에만 등장.** 쓰지 않는 도구 |
| "커버리지 리포트 산출(`reports/coverage_html`)" | 실제는 `reports/htmlcov/`. `reports/coverage.xml` 은 맞음 |

두 건을 고치고, 작업 상태 관리는 `CLAUDE.md` 가 정본임을 문서 맨 위에
적었습니다.

> **삭제하지 않았습니다.** 코딩·테스트·커밋 관행은 여전히 유효하고,
> 가이드라인 삭제는 별도 판단이 필요합니다.

---

## 4. 지켜지지 않던 규칙 하나를 실제에 맞췄습니다

`매 프롬프트마다 프롬프트 문서 작성` — 지켜진 적이 없습니다.

```text
2026-08-28  개발 일지 12건  vs  프롬프트 문서 5건
```

**지켜지지 않는 규칙은 규칙이 아니라 소음입니다.** "작업을 시작하는 요청
하나당 한 건"으로 바꿨습니다. 실제 운영이 이미 그 형태였습니다.

---

## 5. 새 규칙의 골자

### 작업 상태는 어디에 사는가

9행짜리 표로 정리했습니다. 핵심은 셋입니다.

- **닫힐 수 있는 것은 이슈** — 끝나면 목록에서 스스로 사라집니다
- **밟은 함정은 개발 일지** — 이슈가 닫혀도 남아야 하는 지식입니다
- **외부 조건 감시는 검사(CI)** — 이슈로 만들면 영원히 안 닫히고, 문서에
  적으면 아무도 안 봅니다

### "닫을 조건이 없으니 이슈가 아니다"는 성립하지 않습니다

이 저장소 안에 반증이 있습니다.

> [#27](https://github.com/visualmoney/vm-stock-kis/issues/27)
> `... 고정 해제 검토 — 결론: 유지하되 근거를 갱신` → **CLOSED**

판단이 목적인 이슈를 열고 결론을 제목에 박고 닫는 관행이 이미 있었습니다.
**닫는 조건은 "고쳤다"가 아니라 "정했다"로 충분합니다.** 이것이 Discussions
가 필요 없었던 이유이기도 합니다.

### 마일스톤은 쓰지 않습니다

1인 프로젝트에서 판단 비용만 늘리고 행동을 바꾸지 않습니다. 묶음 완료 판정은
네이티브 서브이슈가 이미 합니다 — `#30` 이 `#33`~`#36` 을 물고 있음을
확인했습니다.

```console
$ gh api repos/visualmoney/vm-stock-kis/issues/30/sub_issues
  #33 #34 #35 #36
```

다만 서브이슈는 **포함 관계**이지 **순서 의존**이 아니므로 `blocked` 라벨은
별도로 필요합니다.

---

## 6. 문서에 적은 명령은 전부 실행해 보고 넣었습니다

검증 안 된 명령을 규칙 문서에 넣는 것이 이 개정이 고치려는 실패 양상
그 자체입니다.

```console
$ gh issue list --label next-up --json number,title --jq '.[]|"#\(.number) \(.title)"'
#50 ci: import-linter 계약으로 ...
#42 test: __del__ 무력화 패치 3곳이 ...
#41 test: 실제 네트워크를 쓰는 테스트 17개가 ...

$ gh issue list --label needs-decision ...
#55 refactor(config)!: real/virtual → live/paper ...
#45 refactor(adapter): Protocol/Mixin 중복 축소 ...
#21 feat: examples_llm 기반 엔드포인트 codegen ...
```

`## 손으로 적지 않는 것` 절에 이 명령들을 넣은 이유가 여기 있습니다 —
**이 숫자들을 문서에 적으면 그 순간 낡습니다.**

---

## 변경 파일

- `CLAUDE.md` — 269줄 → 376줄. 트리 정정, 신설 2개 절, 프로세스 3단계 분리,
  Phase 절 대체, 체크리스트 재작성
- `docs/guidelines/AGENT_WORKFLOW_RULES.md` — 사실 오류 2건 + 정본 포인터
- `docs/prompts/2026-08-28_06_claude_md_workflow_rules.md` — 신규
- `docs/dev_logs/2026-08-28_13_claude_md_workflow_rules.md` — 이 문서

`docs/reports/` 와 기존 `docs/dev_logs/` 는 **동결 구역이라 손대지
않았습니다.**

## 테스트 결과

```text
985 passed, 22 skipped
markdownlint  변경 파일 0 issues
```

문서 변경이라 코드 테스트는 회귀 확인용입니다.

## 다음 할 일

- [ ] [#44](https://github.com/visualmoney/vm-stock-kis/issues/44) 가 착수
      가능해졌습니다(#43 완료). `next-up` 3건 중 하나와 교체할지 판단 필요
- [ ] [#55](https://github.com/visualmoney/vm-stock-kis/issues/55)
      `real`/`virtual` 결정 — 재료는 다 모였고 고르기만 하면 됩니다
- [ ] `docs/guidelines/API_STABILITY_POLICY.md:420` markdownlint MD026.
      main 에도 있는 선재 오류
