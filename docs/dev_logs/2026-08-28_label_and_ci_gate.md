# 2026-08-28 - 라벨 체계 점검과 CI 게이트 분리 개발 일지

**범위**: 라벨 참조 복구(PR #31), 성능 테스트를 머지 게이트에서 분리
**관련 이슈**: [#23](https://github.com/visualmoney/vm-stock-kis/issues/23)

---

## 발단

라벨 체계에 Phase/step 축을 추가할지 검토하려고 세 관점(아키텍처 / 품질·테스트 /
구현·기여자)으로 나눠 조사했다. **셋 다 첫 항목으로 같은 것을 짚었다** — 라벨을
늘리기 전에 이미 깨진 참조가 있다.

그리고 그 검증 과정에서 **CI에 지뢰가 있다는 것**이 드러났다. 이쪽이 더 급했다.

---

## 1. 라벨 참조가 끊겨 있었다 (PR #31)

| 위치 | 참조 | 저장소 |
|---|---|---|
| `.github/ISSUE_TEMPLATE/bug-report.yml:4` | `버그` | 없음 |
| `.github/ISSUE_TEMPLATE/feature-request.yml:4` | `기능` | 없음 |
| `.github/ISSUE_TEMPLATE/question.yml:4` | `질문` | 없음 |
| `.github/dependabot.yml:14,24` | `dependencies` | 없음 |

GitHub은 이슈 폼의 `labels:` 에 없는 이름이 있으면 **조용히 버린다.** 만들어주지
않는다. 템플릿으로 들어온 외부 이슈와 dependabot PR이 전부 무라벨로 생성되고
있었다. 기존 `bug`/`enhancement`/`question` 과 **이름만 한국어로 다를 뿐**이다.

템플릿 쪽을 영문 기본 라벨에 맞췄다(라벨을 늘리지 않는 방향).
`dependabot.yml` 은 **참조가 옳고 라벨이 없던 것**이라 라벨을 만들어 복구했다.

### Phase 라벨은 도입하지 않았다

`docs/reports/ARCHITECTURE_ROADMAP_KR.md` 의 Phase 1~4는 **포크 이전 계획**이다.
목표가 v3.0.0이고 "팀 7명 → 10명, QA 2명 증원"을 전제한다. 현재는 1인 체제에
0.0.1 배포 직후다. **열린 이슈 11개 중 Phase를 언급하는 것은 0건.**

죽은 계획을 라벨로 고정하면 문서 부채가 이슈 트래커로 번진다. 그리고 "단계"는
시간축인데 라벨은 성격축이라 애초에 축이 다르다 — 릴리스는 Milestone, 계층은
서브이슈, 성격은 라벨이 맞다.

### 최종 라벨

기본 9개 + 신규 3개. 붙일 이슈를 특정하지 못하는 라벨은 만들지 않았다.

| 라벨 | 근거 | 붙은 곳 |
|---|---|---|
| `dependencies` | 신규가 아니라 끊긴 참조 복구 | dependabot PR |
| `breaking-change` | 커밋의 `!` 표기에 대응하는 이슈 쪽 수단이 없었음 | #30 |
| `test` | 테스트/CI 자체의 문제. 라이브러리 결함이 아님 | #23 |

`#23` 에서 `bug` 를 뗐다. 라이브러리는 멀쩡하고 테스트가 자기 시계를 잘못
재는 것이라 사용자 영향이 0이다. 이제 `bug` 는 실제 결함 3건(#14·#15·#16)만
가리킨다.

`area:*`, 우선순위(P0/P1), `security`, `regression`, `ci` 는 만들지 않았다.
이슈 11개 규모에서 유지 비용만 든다.

---

## 2. CI 게이트에 지뢰가 있었다

품질 관점의 지적을 확인하다 나왔다.

```console
$ grep 'pytestmark\|@pytest.mark' tests/performance/test_benchmark.py
(없음)

$ uv run pytest -m 'not requires_api' --collect-only -q tests/performance/
30 tests collected
```

`tests/performance/` 30개 중 **8개만** `performance` 마커를 갖고 있었다.

| 파일 | 마커 | 테스트 |
|---|---|---|
| `test_benchmark.py` | 0 | 7 |
| `test_memory.py` | 0 | 7 |
| `test_websocket_stress.py` | 0 | 8 |
| `test_performance_advanced.py` | 3 | 7 |
| `test_perf_dummy.py` | 1 | 1 |

즉 `ci.yml` 의 게이팅 잡(`-m 'not requires_api'`)이 성능 테스트 22개를 그대로
수집하고 있었다. 그중 `test_benchmark.py` 는 [#23](https://github.com/visualmoney/vm-stock-kis/issues/23)
의 시계 해상도 flake다.

**지금 CI가 초록인 것은 러너가 느려서일 뿐이고, 러너 세대가 바뀌면 `main` 이
red 가 될 상태였다.** 코드와 무관한 이유로 머지가 막힌다.

### 디렉터리 규칙으로 처리

파일마다 마커를 붙이는 방식은 **이미 한 번 실패했다**(5개 중 3개 누락).
`tests/performance/conftest.py` 를 두어 그 디렉터리의 모든 테스트에 자동으로
붙인다. 새 파일이 마커 없이 추가돼도 반복되지 않는다.

**함정 하나를 밟았다.** 하위 디렉터리의 `conftest` 라도
`pytest_collection_modifyitems` 는 **수집된 전체 목록**을 받는다. 경로로 거르지
않은 첫 시도에서 저장소의 모든 테스트가 `performance` 로 표시되어 게이팅 잡이
**아무것도 실행하지 않게** 됐다.

```text
첫 시도  : 게이팅 잡 0개 수집 (991 deselected)   ← 조용히 전부 통과할 뻔
수정 후  : 게이팅 944 + 성능 30 = 974 (합 일치)
```

검증 없이 넘어갔다면 CI가 초록인 채로 테스트를 하나도 돌리지 않았을 것이다.

### 커버리지 영향은 실측했다

성능 테스트를 게이트에서 빼면 커버리지 게이트(90)가 깨질 수 있어 먼저 쟀다.

```text
성능 포함 : TOTAL 90.73%
성능 제외 : TOTAL 90.72%
```

**0.01%p.** 성능 테스트는 커버리지에 사실상 기여하지 않는다.

### 잡 구성

```text
test          게이트    -m 'not requires_api and not performance' + 커버리지
lint          게이트    actionlint, uv lock --check, ruff
performance   비차단    -m 'performance and not requires_api', continue-on-error
ci-ok         집계      needs: [test, lint]     ← performance 는 의도적으로 제외
```

`performance` 잡에 `--cov` 를 주지 않았다. coverage의 trace 함수가 측정을 느리게
만들어 성능 수치를 왜곡한다.

동작 확인:

```console
$ # 게이팅 잡
937 passed, 7 skipped, 47 deselected
TOTAL 90.72%

$ # 비차단 성능 잡
3 failed, 26 passed, 1 skipped
```

**성능 잡이 실패해도 `ci-ok` 는 통과한다.** 이것이 이 변경의 요점이다.
`#23` 의 근본 수정(`time.time()` → `time.perf_counter()` 18곳)은 별건으로 남는다.

---

## 변경 파일

- `.github/ISSUE_TEMPLATE/{bug-report,feature-request,question}.yml` — 라벨 참조 (PR #31)
- `tests/performance/conftest.py` — 신규. 디렉터리 단위 마커
- `.github/workflows/ci.yml` — 게이팅 잡 필터, `performance` 잡 신설

## 다음 할 일

- [ ] [#23](https://github.com/visualmoney/vm-stock-kis/issues/23) 근본 수정
- [ ] Milestone `0.0.2` / `1.0.0` 생성 및 이슈 배정 (마일스톤 0개 상태)
- [ ] #30 을 서브이슈로 분해 (서브이슈 0개 상태)
