# 2026-08-29 - #41 네트워크 테스트를 tests/integration/ 으로

## 사용자 요청

> pr #66 merge, #41 착수

([#41](https://github.com/visualmoney/vm-stock-kis/issues/41)
`test: 실제 네트워크를 쓰는 테스트 17개가 tests/unit/ 에 있습니다`)

## 분석

`requires_api` 로 표시된 17개가 전부 `tests/unit/` 에 있습니다. 이 테스트들은
**실제 KIS 서버에 HTTP 요청을 보냅니다** — 실계좌 자격증명과 네트워크가 필요합니다.
단위 테스트의 정의와 정반대이고, **디렉터리와 마커가 서로 다른 말을 합니다.**

### 착수 전 실측 — 갈라 옮길 필요가 없습니다

이슈가 먼저 확인하라고 한 것("`requires_api` 아닌 테스트가 섞여 있는가")을 쟀습니다.

```console
tests/unit/test_account_balance.py : 전체  6 / requires_api 아닌 것 0
tests/unit/test_product_quote.py   : 전체 11 / requires_api 아닌 것 0
```

둘 다 파일 첫머리에 `pytestmark = pytest.mark.requires_api` 가 있어 **파일 전체가
`requires_api`** 입니다. **통째로 옮기면 됩니다.**

### "(선택)" 항목은 선택이 아닙니다

`tests/integration/` 에 이미 같은 드리프트가 있습니다.

```console
tests/integration  전체 29개 수집 / integration 마커 9개
```

**29개 중 20개가 마커 없이** `tests/integration/` 에 있습니다.
`tests/performance/conftest.py` 가 똑같은 상황(30개 중 8개)을 겪고 만들어진
선례입니다 — 그 docstring 이 이유를 이미 적어 놨습니다.

> 파일마다 손으로 붙이지 않는 이유가 있다. 실제로 그렇게 하다가 어긋났다.

**여기서 파일 2개를 옮기면 마커 없는 파일이 하나 더 늘어납니다**(옮기는 두 파일은
`requires_api` 는 있지만 `integration` 은 없습니다). 같은 실수를 반복하게 됩니다.

### 주의 — `pythonpath` 의존

`tests/` 에 `__init__.py` 가 없고 `from tests.env import load_vmkis` 가
`pyproject.toml` 의 `pythonpath = ["."]` 에 의존합니다. 옮긴 두 파일 모두 이
import 를 씁니다. 새 위치에서 동작하는지 반드시 확인합니다.

## 계획

1. `test_product_quote.py` · `test_account_balance.py` 를 `git mv` 로 이동
2. `tests/integration/conftest.py` 신설 — `performance/conftest.py` 와 같은 방식
3. `from tests.env import ...` 가 새 위치에서 동작하는지 확인
4. 완료 기준 실행 + **디렉터리 규칙이 실제로 붙는지 되돌려 확인**
5. 개발 일지 작성

## 결과

완료. 개발 일지:
[`2026-08-29_04_issue41_network_tests.md`](../dev_logs/2026-08-29_04_issue41_network_tests.md)

착수 전 예측대로 "(선택)" 항목이 선택이 아니었습니다. 계획 외로 하나 더:
`CONTRIBUTING.md` 의 테스트 트리가 없는 경로 4개를 가리키고 있어 함께 고쳤습니다.
`docs/developer/DEVELOPER_GUIDE.md` 의 트리는 6개 전부 허구지만 범위 밖으로 남겼습니다.
