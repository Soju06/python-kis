# 문서 정리 실태 보고서 — 0.2.0 대비

**작성일**: 2026-08-30
**작성자**: Claude
**대상**: `0.2.0` 문서 갱신 범위 산정
**방법**: 마크다운 172개 전수 조사 (`find` · `git log` · 링크 역참조)

---

## 요약

문서 **172개 / 43,512줄**입니다. 그중 **살아 있는 것은 32개 / 11,736줄**이고
나머지 140개는 동결(개발 일지 46 · 프롬프트 41 · 보고서 28 · 생성물 11 ·
archive 7 등)입니다.

**동결분은 문제가 아닙니다.** CLAUDE.md 가 정한 대로 손대지 않으면 됩니다.
문제는 **살아 있다고 표시된 32개 안에 죽은 것이 섞여 있고, 그것을 구분하는
장치가 없다**는 것입니다.

| 등급 | 건수 | 성격 |
|---|---|---|
| 🔴 즉시 | 3 | 사실이 아닌 것을 말하는 문서 |
| 🟡 0.2.0 | 5 | 유지 비용이 값보다 큰 것 |
| 🟢 관찰 | 2 | 지금은 두되 규칙이 필요한 것 |

---

## 1. 🔴 `docs/README.md` — 20개월 낡은 두 번째 인덱스

가장 큰 문제입니다.

```text
docs/README.md   440줄   **작성 완료**: 2024년 12월 10일
docs/INDEX.md    ...     **최종 업데이트**: 2026-08-28
```

**둘 다 "문서 인덱스"를 자처합니다.** `docs/README.md` 의 첫 줄이
`# VM-Stock-KIS 프로젝트 - 문서 인덱스` 입니다.

그리고 그 안에 CLAUDE.md 가 **손으로 적지 말라고 명시한 것**이 가득합니다.

```text
:5    **총 문서 6개**, **총 5,800+ 줄**, **38,000+ 단어**
:7    **테스트 커버리지**: ✅ **90%** (목표 80% 초과 달성)
:13   ### 1. 아키텍처 문서 (850줄)
:231  90% 커버리지 달성 (6,524 / 7,227 statements)
:346  🎯 대상 독자별 커버리지: 100%
```

실제는 문서 172개, `ARCHITECTURE.md` 950줄입니다. **모든 숫자가 틀렸습니다.**

> CLAUDE.md: *"손으로 적지 않는 것 — 이슈 목록, 테스트 통과 수, 커버리지,
> PyPI 버전, 닫힌 이슈 수. **적는 순간 낡습니다.**"*

이 파일은 그 규칙이 왜 있는지를 보여 주는 표본입니다.

**GitHub 이 `docs/` 를 열면 `README.md` 를 먼저 렌더링합니다.** 즉 방문자가
가장 먼저 보는 것이 20개월 낡은 인덱스입니다.

### 권고

`archive/docs/2024-12_DOCS_INDEX.md` 로 옮기고, `docs/README.md` 는
**`INDEX.md` 로 보내는 한 줄짜리 포인터**로 대체합니다. 지우지 않는 이유는
당시 상태의 기록 가치는 있기 때문입니다(archive 기준에 부합).

---

## 2. 🔴 한/영 문서가 갈라졌습니다

```text
2026-08-30  docs/FAQ.md              2026-08-29  docs/user/en/FAQ.md
2026-08-30  QUICKSTART.md            2026-08-29  docs/user/en/QUICKSTART.md
```

**어제 `#87` 로 "모의 계좌도 실전 앱이 필요하다"를 한국어 문서 3곳에
넣었는데 영문에는 안 들어갔습니다.** 영문 `QUICKSTART` 를 따라간 사용자는
`create_client()` 에서 막힙니다.

이건 이번만의 실수가 아니라 **구조적**입니다. 번역본이 3개(README ·
QUICKSTART · FAQ)이고 원본이 바뀔 때 함께 바뀐다는 보장이 없습니다.

### 권고

**둘 중 하나를 정해야 합니다.**

- **(A) 동기화를 검사로 강제** — 한국어 원본이 바뀐 커밋에서 영문이 안 바뀌면
  CI 가 경고. `tests/unit/test_docs_signatures.py` 가 이미 `docs/user/en/` 을
  훑고 있으므로 붙일 자리가 있습니다
- **(B) 영문을 축소** — 3개를 `README` 하나로 줄이고 나머지는 한국어로 링크

`MULTILINGUAL_SUPPORT.md`(356줄)가 다국어 정책을 적고 있으나 **그 문서 자체가
2026-08-27 이후 손대지 않았고, 이번 드리프트를 막지 못했습니다.**

---

## 3. 🔴 `docs/rules/TEST_RULES_AND_GUIDELINES.md` — 정체 불명

```text
docs/INDEX.md:81  | rules/ | **옛** 테스트 규칙 |
```

INDEX 가 스스로 "옛"이라고 적으면서 `docs/` 아래 살려 두고 있습니다. 그리고
INDEX 의 문서 표에는 **등재되지 않았습니다**(디렉터리 설명에만 있습니다).

`#70` 개명 때 이 디렉터리를 대상 목록에서 빠뜨려 `KisAuth(virtual=)` 가
살아남았고, `#78` 검사기가 뒤늦게 잡았습니다. **"옛 것"이 `docs/` 에 있으면
스윕 대상인지 아닌지 매번 판단해야 합니다.**

### 권고

`docs/guidelines/GUIDELINES_001_TEST_WRITING.md`(410줄)와 내용이 겹치는지
확인한 뒤, 겹치면 **archive 로**, 살아 있어야 하면 `guidelines/` 로 옮기고
"옛"을 뗍니다. **어느 쪽이든 `docs/rules/` 는 없어집니다.**

---

## 4. 🟡 `docs/reports/` 의 `ARCHITECTURE_*_KR` 7종

```text
242줄  ARCHITECTURE_CURRENT_KR      184줄  ARCHITECTURE_DESIGN_KR
547줄  ARCHITECTURE_EVOLUTION_KR    293줄  ARCHITECTURE_ISSUES_KR
335줄  ARCHITECTURE_QUALITY_KR      211줄  ARCHITECTURE_README_KR
361줄  ARCHITECTURE_ROADMAP_KR
                                   합계 2,173줄
```

전부 2026-08-27~28 에 멈췄고, 같은 기간 `docs/architecture/ARCHITECTURE.md`
(950줄)가 계속 갱신되고 있습니다. `ARCHITECTURE_CURRENT_KR.md:161` 은 아직
`python-dotenv` 를 **런타임 의존성**이라고 적습니다 — `#72` 가 지웠습니다.

INDEX 는 이 중 하나에 이미 경고를 답니다.

```text
docs/INDEX.md:89  ⚠️ reports/ARCHITECTURE_QUALITY_KR.md ...
```

**경고를 달아야 하는 문서는 살아 있는 문서가 아닙니다.**

### 권고

보고서는 동결이 원칙이므로 **내용을 고치지 않습니다.** 대신 `reports/archive/`
로 옮깁니다(이미 10개가 그렇게 가 있습니다). 비교 보고서
`2026-08-27_ARCHITECTURE_COMPARISON_...` 는 `#100` 의 근거라 **남깁니다.**

---

## 5. 🟡 Phase 잔재 4종

CLAUDE.md 가 **이름까지 적어 두었습니다.**

> Phase 가 하던 일은 … `PHASE2_WEEK3-4_STATUS.md`,
> `PHASE4_WEEK1_COMPLETION_REPORT.md`, `PHASE4_WEEK3_COMPLETION_REPORT.md`,
> `TASK_PROGRESS.md`

*"Phase 개념은 폐기했습니다"* 라고 선언해 놓고 산출물은 `docs/reports/` 에
그대로 있습니다. `2025-12-18_phase1_week1_complete_report.md` 도 같은 계열입니다.

### 권고

5개를 `reports/archive/` 로. **CLAUDE.md 가 이미 판단을 끝냈으므로 새 결정이
필요 없습니다.**

---

## 6. 🟡 용도가 끝난 것 3종

| 파일 | 줄 | 상태 |
|---|---|---|
| `docs/guidelines/VIDEO_SCRIPT.md` | 421 | 영상 대본. 제작 계획이 있는지 불명 |
| `docs/NEWSLETTER_TEMPLATE.md` | 173 | 서식. 발행 이력은 `archive/` 로 이미 분리됨 |
| `docs/guidelines/MULTILINGUAL_SUPPORT.md` | 356 | 다국어 정책. **2번 드리프트를 못 막았습니다** |

셋 다 *"만들어 뒀지만 쓰이는지 모르는"* 문서입니다. 합계 950줄.

### 권고

**지우자는 것이 아닙니다.** 각각에 **"이것을 언제 쓰는가"** 한 줄이 필요합니다.
그 한 줄을 쓸 수 없으면 `archive/` 로 가는 것이 맞습니다.

---

## 7. 🟢 관찰 — 날짜 표기가 반은 있고 반은 없습니다

```text
docs/guidelines/API_STABILITY_POLICY.md   **작성일**: 2025-12-20   (오늘 고쳤음)
docs/guidelines/CONFIG_SCHEMA.md          **작성일**: 2026-08-29
docs/architecture/ARCHITECTURE.md         (없음)
docs/user/USER_GUIDE.md                   (없음)
```

`API_STABILITY_POLICY.md` 는 오늘 17곳을 고쳤는데 헤더는 여전히
`2025-12-20` 입니다. **작성일은 갱신 여부를 말해 주지 않습니다.**

### 권고

`git log` 가 이미 정확히 알고 있습니다. **헤더의 날짜를 지우거나**,
남긴다면 "작성일"이 아니라 **"이 문서가 무엇을 기준으로 하는가"**(예:
`대상 버전: 0.1.x`)를 적는 편이 유용합니다.

---

## 8. 🟢 관찰 — 릴리스가 문서를 낡게 만드는 것을 아무도 안 잡습니다

`0.1.0` 을 낸 직후 `API_STABILITY_POLICY.md` 17곳 · `ARCHITECTURE.md` 1곳이
`0.0.x` 를 "현재"라고 적고 있었습니다(PR #101 에서 손으로 정정).
`docs/generated/API_REFERENCE.md` 도 `#70` 개명 후 제거된 이름 13곳을
광고하고 있습니다.

**이미 `#94` 가 이 문제를 다룹니다.** 여기서는 규모만 기록합니다.

---

## 무엇을 하지 말아야 하는가

- **동결 문서(개발 일지 46 · 프롬프트 41)를 건드리지 않습니다.** 140개 중
  대부분이 여기이고, 이것들은 "정리 대상"이 아니라 기록입니다
- **문서를 새로 쓰지 않습니다.** 이 보고서의 권고는 전부 *옮기기 · 지우기 ·
  한 줄 덧붙이기* 입니다. 172개가 된 원인이 "필요해 보여서 하나 더 쓴 것"입니다
- **숫자를 문서에 적지 않습니다.** 1번이 그 결과입니다

---

## 예상 효과

| | 지금 | 정리 후 |
|---|---|---|
| 살아 있는 문서 | 32개 / 11,736줄 | **약 26개 / 10,300줄** |
| `docs/` 최상위 진입점 | 2개 (`README` · `INDEX`) | 1개 |
| "옛"이라고 적힌 채 살아 있는 것 | 2곳 | 0 |
| 한/영 드리프트 감지 | 없음 | 검사 또는 축소 |

**줄 수를 줄이는 것이 목적이 아닙니다.** 살아 있는 문서를 열었을 때 그것이
사실이라고 믿을 수 있게 만드는 것이 목적입니다.

---

## 부록 — 조사 방법

```bash
# 전수
find . -name '*.md' -not -path './.git/*' -not -path './.venv/*'

# 살아 있는 것만
... | grep -vE 'dev_logs|prompts|reports|generated|archive'

# INDEX 양방향 대조
grep -oE '\]\(([^)]+\.md)\)' docs/INDEX.md    # 링크 → 실재 확인
find docs -name '*.md' | ...                  # 실재 → 등재 확인

# 한/영 드리프트
git log -1 --format='%ad' --date=short -- <파일>
```

**INDEX 의 링크는 28곳 전부 실재했습니다** — `#29` 가 고친 것이 유지되고
있습니다. 이 보고서가 지적하는 것은 링크가 아니라 **내용의 수명**입니다.
