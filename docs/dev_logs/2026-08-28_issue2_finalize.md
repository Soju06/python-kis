# 2026-08-28 - Issue #2 마무리 개발 일지

**대상 이슈**: [visualmoney/vm-stock-kis#2](https://github.com/visualmoney/vm-stock-kis/issues/2)
**프롬프트 문서**: [2026-08-28_issue2_finalize.md](../prompts/2026-08-28_issue2_finalize.md)
**범위**: 뉴스레터 기록물 분리, `archive/` 신설, 죽은 링크 정정.
**커밋 6(`v3.0.0` 태그 + PyPI 배포)은 사용자 결정에 따라 하지 않았다.**

---

## 요약

이슈 #2에서 유일하게 남아 있던 옛 이름 파일을 처리하고, 그 과정에서 드러난
죽은 링크를 고쳤다. 라이브러리 코드는 건드리지 않았다.

```text
963~965 passed, 8 skipped, 17 deselected
ruff check / ruff format --check / uv lock --check 통과
완료 기준 grep 4종 전부 빈 출력
사전 결함 1건 유지 — 벤치마크 시계 해상도 flake (아래 참고)
```

---

## 1. 뉴스레터 — 서식이 아니라 발행물이었다

`docs/NEWSLETTER_TEMPLATE.md`는 이슈의 스윕 포함 목록에도 제외 목록에도 없어
유일하게 옛 이름(`pykis` 15곳, `PyKis` 2곳, `Python-KIS` 3곳)이 남은 파일이었다.
직전 세션이 "기록물"로 보고 스윕하지 않았지만 판단을 미뤄 둔 상태였다.

파일을 열어 보니 문제는 이름이 아니라 **정체성**이었다. 내용이 "2025년 12월호"로
채워진 실제 발행물인데 파일명만 `TEMPLATE`이다. 즉 다음 호를 이 파일에서 복사하면
2025년 12월의 통계·일정·이름이 그대로 딸려 간다.

그래서 스윕이 아니라 둘로 나눴다.

| 결과물 | 성격 |
|---|---|
| `archive/docs/2025-12_NEWSLETTER.md` | 발행물 원본. 옛 이름·옛 링크 그대로 |
| `docs/NEWSLETTER_TEMPLATE.md` | 실제 빈 서식. `{{ }}` 자리표시자, 현재 이름 |

기록물 맨 위에 동결 안내를 달았다 — 왜 보관됐는지, 언제 것인지, 지금은 무엇을
봐야 하는지. 본문은 손대지 않았다.

### 파일에서 발견한 것

- 파일 첫 줄과 마지막 줄이 `"""` 였다. Markdown 파일에 파이썬 삼중따옴표가
  남아 있었다. 기록물로 옮기며 **이 두 줄만** 지웠다. 당시 서술이 아니라
  기계적 잔재다.
- 본문의 GitHub 링크가 `github.com/QuantumOmega/python-kis` 였다. 업스트림
  (`Soju06`)도 이 포크(`visualmoney`)도 아닌 제3의 이름이다. 발행 당시부터
  잘못된 주소였으므로 기록물에서는 고치지 않고, 그렇다는 사실만 안내에 적었다.

### rename 이력이 이어지지 않는 이유

`git log --follow archive/docs/2025-12_NEWSLETTER.md` 는 이전 이력을 따라가지
못한다. 옛 경로(`docs/NEWSLETTER_TEMPLATE.md`)가 **삭제되지 않고 새 내용으로
남기** 때문에 git이 rename 쌍을 만들 수 없다. 서식이 그 자리를 유지해야 하므로
피할 수 없는 구조다. 대신 기록물 헤더에 원래 경로를 명시했다.

---

## 2. `archive/` — 동결 보관소

사용자 지시로 저장소 루트에 `archive/` 를 두고 종류별 하위 폴더
(`docs` / `src` / `scripts`)로 나눴다. 원본이 있던 자리를 그대로 옮기는 구조다.

`archive/README.md` 에 보관 기준을 적었다. 특히 **넣지 않을 것**을 명시했다 —
아직 쓰이는 것, git이 이미 기억하는 것(단순 삭제는 `git log`로 되찾을 수 있다),
그리고 옛 설정 파일에 남은 앱키·토큰.

### 도구에서 제외

보관소는 "당시 상태 그대로"가 목적이므로 자동 도구가 건드리면 안 된다.

| 도구 | 조치 |
|---|---|
| markdownlint | `.markdownlint-cli2.jsonc` `ignores` 에 `archive/docs/**`·`archive/src/**`·`archive/scripts/**` 추가 |
| ruff | `[tool.ruff] extend-exclude` 에 `archive` 추가 |
| pytest | `testpaths = ["tests"]` 라 이미 대상 밖 |
| 커버리지 | `source_pkgs = ["vmkis"]` 라 이미 대상 밖 |
| sdist/휠 | `[tool.hatch.build.targets.sdist] include` 에 없어 이미 대상 밖 |

`archive/README.md` 는 **일부러 제외하지 않았다.** 보관소 자체의 안내문이므로
계속 린트를 받아야 한다.

이미 있던 `docs/reports/archive/` 는 그대로 뒀다. 그쪽은 파일끼리 네비게이션
앵커로 얽혀 있어 옮기면 링크를 전부 다시 걸어야 하고, 이슈 #2 범위를 넘는다.
→ 아래 "다음 할 일" 참고.

---

## 3. 존재하지 않는 저장소를 가리키던 링크 19곳

완료 기준 grep을 돌리다 `QuantumOmega` 를 발견했고, 소유자 이름 분포를
전수 조사해 같은 부류를 찾았다.

```console
$ git grep -hoE 'github\.com/[A-Za-z0-9_.-]+' -- . ':!docs/dev_logs' ... | sort | uniq -c | sort -rn
     67 github.com/visualmoney
     29 github.com/Soju06          # 업스트림 — 정상
     12 github.com/yourusername    # ← 자리표시자가 그대로
      5 github.com/en              # docs.github.com — 오탐
      4 github.com/...             # 대본 초안의 의도적 생략 — 유지
```

| 잘못된 소유자 | 곳 | 파일 |
|---|---|---|
| `QuantumOmega` | 7 | `docs/FAQ.md`, `examples/tutorial_basic.ipynb` |
| `yourusername` | 12 | `docs/user/en/{FAQ,QUICKSTART,README}.md`, `examples/README.md` |

전부 `visualmoney` 로 고쳤다.

**이름 스윕이 이 결함을 더 나쁘게 만들었다.** 스윕은 `python-kis` →
`vm-stock-kis` 만 바꾸고 소유자는 손대지 않았다. 그 결과
`github.com/QuantumOmega/python-kis` (한눈에 남의 저장소)가
`github.com/QuantumOmega/vm-stock-kis` (이 프로젝트처럼 보이는 404)로 바뀌었다.
이슈의 sentinel 규칙은 업스트림 URL만 보호했고, 애초에 틀린 소유자는
검토 대상이 아니었다.

`github.com/...` 4곳은 `VIDEO_SCRIPT.md` 와 `GITHUB_DISCUSSIONS_SETUP.md` 의
대본·서식 초안 안에 있는 의도적 생략이라 그대로 뒀다. 링크처럼 읽히지 않는다.

---

## 변경 파일

- `docs/NEWSLETTER_TEMPLATE.md` — 빈 서식으로 새로 작성
- `archive/docs/2025-12_NEWSLETTER.md` — 신규 (발행물 기록물)
- `archive/README.md` — 신규 (보관 기준)
- `.markdownlint-cli2.jsonc` — `archive/` 제외
- `pyproject.toml` — `[tool.ruff] extend-exclude` 에 `archive`
- `docs/FAQ.md`, `examples/tutorial_basic.ipynb` — `QuantumOmega` → `visualmoney`
- `docs/user/en/{FAQ,QUICKSTART,README}.md`, `examples/README.md` —
  `yourusername` → `visualmoney`
- `CHANGELOG.md` — 위 내용 반영

---

## 테스트 결과

```console
$ uv run ruff check .           All checks passed!
$ uv run ruff format --check .  185 files already formatted
$ uv lock --check               Resolved 47 packages
$ uv run pytest -q -m "not requires_api"
  965 passed, 8 skipped, 17 deselected   # 벤치마크 flake 제외
```

완료 기준 grep 4종(`\bpykis\b`, `PyKis|PyKIS|Pykis|PYKIS_`, `Python-KIS`,
`QuantumOmega|yourusername`) 은 의도적 잔존 지점(호환 shim, 마이그레이션 문서,
CHANGELOG, 기록물)을 제외하면 전부 빈 출력이다.

### 사전에 있던 실패 — 이 작업과 무관

`tests/performance/test_benchmark.py::TestTransformBenchmark` 의 7개 중
**실행할 때마다 1~4개가 실패한다.** `main` 을 체크아웃해 그대로 재현했으므로
이번 변경과 무관한 사전 결함이다.

```text
단순 (5필드): 500 ops in 0.000s (0.0 ops/s)
assert all(s.ops_per_second > 10 for s in scenarios)  →  False
```

원인은 성능이 아니라 시계 해상도다. Windows에서 `time.time()` 의 눈금이
약 15.6ms인데 측정 구간이 그보다 빨리 끝나면 경과 시간이 정확히 `0.000s` 로
찍히고 `ops_per_second` 가 0이 된다. **빠른 기계일수록 실패한다.**
실패 개수가 실행마다 달라지는 것도 눈금 경계에 걸려 있기 때문이다.

`time.time()` 이 18곳에 쓰였고 전부 경과 시간 측정 용도라
`time.perf_counter()` 로 바꾸면 해결된다. 이슈 #2 범위가 아니라 손대지 않았다.

CI가 초록인 이유는 러너가 이 경계를 넘지 않을 만큼 느리기 때문이며, 언제든
뒤집힐 수 있다.

---

## 다음 할 일

### 이슈 #2에 남은 것

- [ ] **커밋 6**: `git tag -a v3.0.0 && git push origin v3.0.0`
      → `publish.yml` 이 실제 PyPI에 게시한다. **되돌릴 수 없다.**
      선행 조건: PyPI에 pending publisher 등록
      (Owner `visualmoney`, Repo `vm-stock-kis`, Workflow `publish.yml`,
      Environment `pypi`). 저장소 밖이라 코드로 확인할 수 없다.
- [ ] `main` 브랜치 보호에 `CI OK` 체크 필수화
- [ ] (선택) `[tool.hatch.build.targets.*] core-metadata-version = "2.4"` 해제 여부.
      TestPyPI `v3.0.0rc1` 은 2.4로 통과했을 뿐 2.5를 검증하지 않았다.
      **정식 배포 전에는 풀지 않기를 권한다.**

### 이슈 #2 밖에서 발견한 것

- [ ] `tests/performance/test_benchmark.py` 의 `time.time()` 18곳 →
      `time.perf_counter()`. 지금 상태로는 벤치마크 잡이 기계 속도에 따라
      무작위로 실패한다.
- [ ] `docs/INDEX.md` 가 망가져 있다. 디렉터리 트리 블록(46행 등)이 섞여 있고
      존재하지 않는 `docs/user/ko/` 를 안내한다. `2025-12-20` 이후 갱신되지 않았다.
- [ ] `docs/reports/archive/` 를 `archive/docs/` 로 합칠지 결정.
      파일 간 앵커를 다시 걸어야 해서 별건으로 둔다.
