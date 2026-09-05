# 2026-08-29 - #41 네트워크 테스트를 tests/integration/ 으로 개발 일지

**이슈**: [#41](https://github.com/visualmoney/vm-stock-kis/issues/41)
`test: 실제 네트워크를 쓰는 테스트 17개가 tests/unit/ 에 있습니다`
**프롬프트**: [`2026-08-29_04_issue41_network_tests.md`](../prompts/2026-08-29_04_issue41_network_tests.md)

## 이동 자체는 간단했습니다

이슈가 먼저 확인하라고 한 것("`requires_api` 아닌 테스트가 섞여 있는가")을 쟀더니
**갈라 옮길 필요가 없었습니다.**

```console
tests/unit/test_account_balance.py : 전체  6 / requires_api 아닌 것 0
tests/unit/test_product_quote.py   : 전체 11 / requires_api 아닌 것 0
```

둘 다 파일 첫머리에 `pytestmark = pytest.mark.requires_api` 가 있습니다.
`git mv` 두 번으로 끝났고, `from tests.env import load_vmkis` 도 새 위치에서
그대로 동작합니다(`pythonpath = ["."]` 이 저장소 루트를 기준으로 하므로 파일이
어느 하위 디렉터리에 있든 무관합니다).

## 걸린 것 — "(선택)" 항목이 선택이 아니었습니다

이슈가 괄호로 남긴 항목입니다.

> (검토) `tests/integration/` 전체에 `pytestmark = pytest.mark.integration` 을
> 붙일지. `tests/performance/conftest.py` 가 디렉터리 단위 마커의 선례입니다

재 보니 **이미 어긋나 있었습니다.**

```console
tests/integration  전체 29개 수집 / integration 마커 9개
```

29개 중 20개가 마커 없이 `tests/integration/` 에 있었습니다.
`tests/performance/conftest.py` 가 만들어진 이유(30개 중 8개)와 **같은 상황이
같은 저장소에서 두 번째로 반복된 것**입니다. 그 파일 docstring 이 이미 적어
놨습니다.

> 파일마다 손으로 붙이지 않는 이유가 있다. 실제로 그렇게 하다가 어긋났다.

그리고 **이 이슈의 이동 자체가 그 드리프트를 더 키울 참이었습니다.** 옮기는 두
파일은 `requires_api` 는 갖고 있지만 `integration` 은 없습니다. 그냥 옮기면
마커 없는 파일이 5개에서 7개로 늘어납니다. 그래서 `tests/integration/conftest.py`
를 함께 넣었습니다.

**게이팅은 바뀌지 않습니다.** CI 의 게이팅 잡은
`-m 'not requires_api and not performance'` 라 `integration` 을 제외하지 않습니다.
이 마커는 사람이 고르기 위한 것이지 머지를 막는 장치가 아닙니다.

## 되돌려 확인

디렉터리 규칙이 **실제로 새 파일에 붙는지** 확인했습니다. 마커 없는 빈 테스트
파일을 `tests/integration/` 에 넣고:

| 조건 | `-m integration` 수집 |
|---|---|
| `conftest.py` 있음 | **1** ✅ |
| `conftest.py` 치움 | **0** |

마커 누출도 확인했습니다 — 저장소 전체 `-m integration` 이 46개(기존 29 + 옮긴
17)이고 `tests/unit` 은 0개입니다. `pytest_collection_modifyitems` 는 하위
conftest 라도 **수집된 전체 목록**을 받으므로 경로로 거르지 않으면 저장소의 모든
테스트가 integration 이 됩니다. `performance/conftest.py` 의 주석이 경고한 그대로라
같은 방식으로 걸렀습니다.

## 함께 고친 것 — `CONTRIBUTING.md` 의 테스트 트리

옮긴 파일을 가리키는 문서를 찾다가 발견했습니다. `CONTRIBUTING.md` 의
"테스트 구조" 트리가 **없는 경로 4개**를 가리키고 있었습니다.

```text
tests/fixtures/                      없음
tests/integration/test_stock_quote.py  없음
tests/integration/test_websocket.py    없음
tests/unit/test_load_config.py         없음
```

`CLAUDE.md` 가 자기 문서 트리에 대해 적어 둔 것과 **똑같은 문제**입니다.

> 트리를 고칠 때는 실제로 `ls` 해 보세요.

`ls tests/` 를 해서 다시 썼고, 같은 경고문을 그 자리에 남겼습니다. 이 트리는 제가
방금 바꾼 구조를 서술하는 문서라 범위 안입니다.

## 범위 밖으로 남긴 것

`docs/developer/DEVELOPER_GUIDE.md:525-545` 의 테스트 트리는 **통째로 허구**입니다.

```text
tests/__init__.py     없음 (있으면 pythonpath 의존이 깨집니다)
tests/conftest.py     없음
tests/test_kis.py     없음 (tests/unit/test_kis.py 입니다)
tests/test_api/       없음
tests/test_responses/ 없음
tests/fixtures/       없음
```

**6개 전부 없습니다.** 다만 이 파일은 테스트 구조만 틀린 게 아니라 문서 전체가
옛 레이아웃 기준으로 보이므로, 트리 한 조각만 고치면 나머지가 여전히 거짓말을
합니다. #41 의 범위를 넘으므로 손대지 않았습니다.

## 변경 파일

- `tests/unit/test_account_balance.py` → `tests/integration/` (이동, 내용 무변경)
- `tests/unit/test_product_quote.py` → `tests/integration/` (이동, 내용 무변경)
- `tests/integration/conftest.py` — **신규.** 디렉터리 단위 `integration` 마커
- `CONTRIBUTING.md` — 테스트 구조 트리를 실제 구조로

## 테스트 결과 (완료 기준 포함)

```console
$ uv run pytest -m requires_api --collect-only -q tests/unit/
0                                    # 완료 기준: 빈 출력

$ uv run pytest -m requires_api --collect-only -q
17                                   # 완료 기준: 기존과 같은 수

$ uv run pytest -m integration --collect-only -q
46                                   # 29(기존) + 17(이동). 전에는 9

$ uv run pytest -m 'not requires_api' -q
1052 passed, 8 skipped
```

커버리지 92%(게이트 90), `ruff`·`lint-imports --no-cache`(2 kept, 0 broken) 통과.

## 남은 것

`DEVELOPER_GUIDE.md` 의 허구 트리(위 참고). 이슈로 만들지 여부는 사용자 판단에
맡깁니다 — 트리 한 조각이 아니라 문서 전체의 신선도 문제로 보입니다.
