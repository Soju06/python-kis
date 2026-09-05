# archive/ — 동결 보관소

여기 있는 파일은 **당시 상태 그대로 보존**합니다. 읽을 수는 있지만
빌드·테스트·린트·이름 스윕의 대상이 아닙니다.

## 무엇을 넣나

수명이 끝났지만 없애기는 아까운 것들입니다.

- 발행이 끝난 뉴스레터 한 호
- 대체된 옛 보고서·설계 문서
- 더 이상 쓰지 않지만 참고 가치가 있는 스크립트·프로토타입 코드

## 무엇을 넣지 않나

- **아직 쓰이는 것.** 참조되는 문서나 실행되는 코드는 제자리에 둡니다.
- **git이 이미 기억하는 것.** 단순히 지운 파일은 `git log`로 되찾을 수 있습니다.
  여기에 넣는 기준은 "지금도 사람이 찾아 읽을 만한가"입니다.
- **비밀 정보.** 옛 설정 파일에 남은 앱키·토큰은 보관 대상이 아닙니다.

## 구조

원본이 있던 자리를 그대로 옮깁니다.

```text
archive/
├── docs/        # 문서 (docs/ 에서 옮겨온 것)
├── src/         # 파이썬 모듈 (src/vmkis/ 에서 옮겨온 것)
└── scripts/     # 스크립트 (scripts/ 에서 옮겨온 것)
```

파일명에 시점을 남깁니다: `2025-12_NEWSLETTER.md`, `2025-12-20_legacy_fetch.py`.

## 규칙

1. **내용을 고치지 않습니다.** 옛 이름(`pykis` / `PyKis` / `Python-KIS`)과 죽은
   링크가 남아 있어도 그대로 둡니다. 그것이 당시 서술입니다.
2. **맨 위에 동결 안내를 답니다.** 왜 보관됐는지, 언제 것인지, 지금은 무엇을
   봐야 하는지 한 문단이면 충분합니다.
3. **여기서 옮겨 오지 않습니다.** 다시 쓸 것이 생기면 복사해서 제자리에
   되살리고, 원본은 여기 남깁니다.

## 도구에서 제외되는 경로

| 도구 | 설정 |
|---|---|
| markdownlint | `.markdownlint-cli2.jsonc` 의 `ignores` |
| ruff | `pyproject.toml` `[tool.ruff] extend-exclude` |
| pytest | `[tool.pytest.ini_options] testpaths = ["tests"]` 라 애초에 대상 밖 |
| 커버리지 | `[tool.coverage.run] source_pkgs = ["vmkis"]` 라 대상 밖 |
| sdist/휠 | `[tool.hatch.build.targets.sdist] include` 에 없음 |

앞으로의 이름 스윕도 `archive/` 를 제외해야 합니다.

## 목록

| 경로 | 원래 자리 | 시점 | 비고 |
|---|---|---|---|
| [docs/2025-12_NEWSLETTER.md](./docs/2025-12_NEWSLETTER.md) | `docs/NEWSLETTER_TEMPLATE.md` | 2025-12 | 서식이 아니라 실제 발행된 한 호였음 ([#2](https://github.com/visualmoney/vm-stock-kis/issues/2)) |
| [docs/reports/2026-08-28_TODO_LIST.md](./docs/reports/2026-08-28_TODO_LIST.md) | `docs/reports/2026-08-28_TODO_LIST.md` | 2026-08-28 | 아래 "To-Do 문서를 왜 전부 옮겼나" 참고 |
| [docs/reports/2025-12-17_TODO_LIST.md](./docs/reports/2025-12-17_TODO_LIST.md) | `docs/reports/TODO_LIST_2025_12_17.md` | 2025-12-17 | P0~P3 체계. 쓰지 않음 |
| [docs/generated/2025-12-17_TODO_LIST.md](./docs/generated/2025-12-17_TODO_LIST.md) | `docs/generated/TODO_LIST.md` | 2025-12-17 | 본문은 "2024년 12월 · PyKIS 테스트 프로젝트"라고 적고 있음 |
| [docs/generated/2025-12-17_todo.md](./docs/generated/2025-12-17_todo.md) | `docs/generated/todo.md` | 2025-12-17 | poetry 시절 임시 메모 |
| [docs/generated/2025-12_COMPLETION_SUMMARY.md](./docs/generated/2025-12_COMPLETION_SUMMARY.md) | `docs/generated/COMPLETION_SUMMARY.md` | 2025-12 | 생성기가 만들지 않는 일회성 산출물 ([#94](https://github.com/visualmoney/vm-stock-kis/issues/94)) |
| [docs/generated/2025-12_dev_log.md](./docs/generated/2025-12_dev_log.md) | `docs/generated/dev_log.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_dev_log_complete.md](./docs/generated/2025-12_dev_log_complete.md) | `docs/generated/dev_log_complete.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_prompts_guide.md](./docs/generated/2025-12_prompts_guide.md) | `docs/generated/prompts_guide.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_prompts_rules.md](./docs/generated/2025-12_prompts_rules.md) | `docs/generated/prompts_rules.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_report.md](./docs/generated/2025-12_report.md) | `docs/generated/report.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_report_final.md](./docs/generated/2025-12_report_final.md) | `docs/generated/report_final.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_VALIDATION_REPORT_WEBSOCKET_STRESS.md](./docs/generated/2025-12_VALIDATION_REPORT_WEBSOCKET_STRESS.md) | `docs/generated/VALIDATION_REPORT_WEBSOCKET_STRESS.md` | 2025-12 | 같음 |
| [docs/generated/2025-12_VALIDATION_REPORT_WEBSOCKET_STRESS_COMPLETE.md](./docs/generated/2025-12_VALIDATION_REPORT_WEBSOCKET_STRESS_COMPLETE.md) | `docs/generated/VALIDATION_REPORT_WEBSOCKET_STRESS_COMPLETE.md` | 2025-12 | 같음 |
| [docs/generated/2025-12-17_test_run.md](./docs/generated/2025-12-17_test_run.md) | `docs/generated/test_run_2025-12-17.md` | 2025-12-17 | 같음 |

## To-Do 문서를 왜 전부 옮겼나

**작업 목록이 저장소에 네 벌 있었고, 서로를 몰랐습니다.**

```text
docs/reports/TODO_LIST_2025_12_17.md   2025-12-17, 명명 규칙 A
docs/reports/2026-08-28_TODO_LIST.md   2026-08-28, 명명 규칙 B
docs/generated/TODO_LIST.md            본문은 "2024년 12월"
docs/generated/todo.md                 poetry 시절
```

정렬 순서로는 `2026-08-28_TODO_LIST.md` 가 `TODO_LIST_2025_12_17.md` **앞**에
옵니다(`2` < `T`). `grep TODO_LIST` 로 시작하는 사람은 8개월 낡은 문서를 먼저
만납니다.

가장 최근 것(2026-08-28)조차 **고유한 정보가 없었습니다.** 116줄을 줄 단위로
추적한 결과 이슈 본문·이슈 코멘트·개발 일지·`pyproject.toml` 주석 어딘가에
전부 있었습니다. 게다가 "갱신하지 않는다"고 선언된 `docs/reports/` 안에
**아무도 켤 수 없는 체크박스 3개**를 두고 있었습니다.

**작업 목록은 이슈 트래커가 유일한 출처입니다** — `gh issue list`.
