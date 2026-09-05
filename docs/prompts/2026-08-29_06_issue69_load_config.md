# 2026-08-29 - #69 load_config 통합 + 미지의 키에 명시적 실패

## 사용자 요청

> #69 부터 먼저 착수하고 #70에서 스키마 변경 등에 의하여 재수정 예정 같이 PR 머지 예정

`#69` 를 먼저 하고, `#70` 이 이 결과물 일부를 다시 고치는 것을 **예정된 재수정으로
받아들인다**는 결정입니다. 그 두 건은 착수 전에 #70 본문에 못 박아 두었습니다.

## 분석

### 고쳐야 할 것 — 조용히 실전으로 붙는 경로

```python
src/vmkis/helpers.py:114    virtual=cfg.get("virtual", False),
```

**기본값이 `False` = 실전입니다.** `create_client` 는 키를 하나씩 뽑아 쓰기 때문에
(`helpers.py:109-115`) 여분·오타 키는 **아무 소리 없이 무시**됩니다. 그래서
`virtaul: true` 는 오타를 알려주는 것 없이 실전 계좌로 연결됩니다.

같은 코드가 **5벌**입니다.

```text
src/vmkis/helpers.py:114
examples/01_basic/get_balance.py:43
examples/01_basic/get_quote.py
examples/01_basic/place_order.py
examples/01_basic/realtime_price.py
```

### 착수 전에 알게 된 것

**1. `load_config` 는 이미 `helpers.__all__` 에 있습니다** (`helpers.py:17`).
빠진 곳은 **패키지 루트**입니다 — `vmkis/__init__.py:51` 이 `create_client` 와
`save_config_interactive` 만 올립니다. 예제가 import 로 쓰려면 루트에 올리는 것이
자연스럽고, 이는 **추가**라 하위호환을 깨지 않습니다.

**2. 예제 복사본을 겨냥한 테스트가 이미 있습니다.**

```python
tests/unit/test_load_config_get_quote.py:17
    load_mod = _load_example_module("examples/01_basic/get_quote.py")
    load_config_example = load_mod.load_config
```

**중복을 테스트가 고착시키고 있었습니다.** 다만 이 테스트는 실제
`config.example*.yaml` 3개를 파싱해 보는 값어치가 있으므로, 대상을 라이브러리
쪽으로 바꿔 살립니다.

**3. 검증을 넣으면 깨지는 기존 테스트가 1건 있습니다.**

```python
tests/unit/test_compat_aliases.py:85
    config = {"default": "virtual", "configs": {"virtual": {"id": "v"}, "real": {"id": "r"}}}
```

프로필에 `id` 하나뿐입니다. 이 테스트의 목적은 `PYKIS_PROFILE` 폴백이지 부분
설정이 아니므로, 키를 채워도 **검증력이 줄지 않습니다.**

`test_helpers.py` 의 `FLAT_CONFIG`/`MULTI_CONFIG` 와 `config.example*.yaml` 3개는
전부 5개 키를 갖고 있어 영향이 없습니다.

**4. 검증 위치는 `load_config` 입니다.** `create_client` 에만 넣으면 예제처럼
`load_config` 로 읽어 `KisAuth` 를 직접 만드는 경로가 보호되지 않습니다.

### 스키마 의존도 — #70 에서 무엇이 살아남는가

착수 전에 사용자가 물어 확인한 것입니다.

| | #70 (`mode: live\|paper`) 이후 |
|---|---|
| `load_config` 1벌 통합 | 그대로 |
| 모르는 키 → 예외 | 메커니즘 그대로. 허용 키 집합만 갱신 |
| 판정 키 없으면 → 예외 | **원칙만 남고 구현은 버려집니다** (불리언 전용 sentinel) |
| 상수 공유 | 그대로. 내용만 바뀜 |
| 회귀 테스트 | 남지만 #70 은 **자기 테스트를 새로 써야** 합니다 (값 오타 `mode: papr`, 옛 키 잔존) |

버려질 코드가 3~5줄이라 분리 비용이 순서를 바꿀 만큼 크지 않다고 판단했습니다.

## 계획

1. `helpers.py` 에 프로필 키 상수 도입 — `#70` 이 **이 상수만** 고치면 되게
2. `load_config` 가 프로필을 검증: 모르는 키 / 필수 키 누락 / 판정 키 누락 → 예외
3. `create_client` 를 `cfg[_MODE_KEY]` 로. `.get(..., False)` 제거
4. `save_config_interactive` 가 같은 상수를 쓰도록
5. `load_config` 를 패키지 루트 `__all__` 에 추가
6. 예제 4개의 복붙 `load_config` 제거 → import
7. 테스트: 오타 키·판정 키 누락. **결함을 되살려 실패하는지 확인**
8. `test_load_config_get_quote.py` 를 라이브러리 대상으로 전환
9. `test_compat_aliases.py:85` 프로필 키 채우기

## 결과

계획 9단계를 전부 수행했습니다. 계획에 없던 것 하나가 나왔습니다 —
**막으려던 동작이 테스트에 사양으로 적혀 있었습니다.**

```python
tests/unit/test_helpers.py:133
    def test_virtual_key_defaults_to_false(...):
        """`virtual` 키가 없으면 실전으로 간주한다."""
```

착수 전 조사에서 놓친 이유는 `load_config`/`create_client` 를 **호출하는 줄**만
grep 하고 단언을 읽지 않았기 때문입니다. 뒤집어서
`test_missing_virtual_key_raises` 로 바꿨습니다.

```console
uv run pytest -m 'not requires_api'    1058 passed, 8 skipped
coverage                               91.58%  (게이트 90), helpers.py 100%
되돌려 확인                            결함 복원 시 7건 실패
```

작업 중 사용자가 의존성 검토를 지시해 [#72](https://github.com/visualmoney/vm-stock-kis/issues/72)(python-dotenv),
[#73](https://github.com/visualmoney/vm-stock-kis/issues/73)(조용한 `None` 폴백)을 별도 이슈로 남겼습니다.

상세는 [개발 일지](../dev_logs/2026-08-29_06_issue69_load_config.md).
