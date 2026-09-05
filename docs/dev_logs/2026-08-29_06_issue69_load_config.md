# 2026-08-29 - #69 load_config 통합 + 미지의 키에 명시적 실패 개발 일지

## 작업 내용

`load_config` 5벌을 하나로 합치고, 프로필을 검증해 **조용히 실전 계좌로 붙는 경로**를
막았습니다. [#69](https://github.com/visualmoney/vm-stock-kis/issues/69).

## 걸린 것

### 1. 테스트가 그 위험을 **사양으로 못 박고** 있었습니다

구현을 끝내고 테스트를 돌렸더니 1건이 깨졌습니다. 이름이 전부 설명합니다.

```python
tests/unit/test_helpers.py:133
    def test_virtual_key_defaults_to_false(self, tmp_path, dummy_vmkis):
        """`virtual` 키가 없으면 실전으로 간주한다."""
        ...
        assert args[0].virtual is False
```

**막으려던 동작이 통과해야 할 사양으로 적혀 있었습니다.** 이 테스트가 있는 한
누가 나중에 기본값을 고쳐도 "테스트가 깨졌으니 되돌리자"가 됩니다.

착수 전 조사에서 이걸 놓쳤습니다. `load_config`/`create_client` 를 **호출하는
줄**만 grep 했고, `TestCreateClient` 클래스 본문을 읽지 않았습니다. **호출 지점이
아니라 단언을 읽어야 했습니다.**

### 2. 되돌려 확인 — 결함을 되살리면 7건이 실패합니다

`_validate_profile` 을 무력화하고 `.get(_MODE_KEY, False)` 를 복원했습니다.

```console
$ uv run pytest tests/unit/test_helpers.py::TestProfileValidation \
    tests/unit/test_helpers.py::TestCreateClient::test_missing_virtual_key_raises -q
7 failed in 0.32s
```

그 상태에서 실제로 무슨 일이 벌어지는지도 찍었습니다.

```console
설정 파일이 말하는 것 : virtaul(오타) = True   -> 사용자 의도: 모의투자
load_config 결과 키   : ['account', 'appkey', 'id', 'secretkey', 'virtaul']
create_client 가 볼 값: virtual = False

=> 실전 계좌로 붙습니다. 경고 한 줄 없습니다.
```

복원 후 `grep -c DEFECT-REVIVAL` 이 0인 것과 1058건 통과를 확인했습니다.

### 3. 예제 복사본을 겨냥한 테스트가 중복을 고착시키고 있었습니다

```python
tests/unit/test_load_config_get_quote.py:17
    load_mod = _load_example_module("examples/01_basic/get_quote.py")
    load_config_example = load_mod.load_config
```

5벌 중 하나를 importlib 로 끌어와 테스트하고 있었습니다. **중복을 지우려면
테스트부터 지워야 하는 구조**였습니다. 다만 이 테스트는 배포되는
`config.example*.yaml` 3개를 실제로 파싱해 보는 값어치가 있어, 대상을
라이브러리로 바꿔 `test_config_examples.py` 로 살렸습니다. 이제 예제 설정에
여분·오타 키가 섞이면 여기서 걸립니다.

### 4. 검증을 넣으면 깨지는 기존 테스트가 하나 더 있었습니다

```python
tests/unit/test_compat_aliases.py:85
    config = {"default": "virtual", "configs": {"virtual": {"id": "v"}, "real": {"id": "r"}}}
```

프로필에 `id` 하나뿐입니다. 이 테스트의 대상은 `PYKIS_PROFILE` 폴백이지 부분
설정이 아니므로 키를 채웠습니다. 왜 채웠는지 주석으로 남겼습니다 — 안 남기면
다음 사람이 "왜 이렇게 장황하지" 하고 되돌립니다.

### 5. 함정 — 모듈 단위 coverage 가 안 됩니다

```console
$ uv run pytest tests/unit/test_helpers.py --cov=vmkis.helpers
ImportError: PyO3 modules compiled for CPython 3.8 or older
             may only be initialized once per interpreter process
```

`--cov=vmkis` (패키지 전체)는 됩니다. 서브모듈을 지정하면 coverage 가 `vmkis` 를
먼저 import 하면서 `cryptography` 의 PyO3 확장이 두 번 초기화됩니다.
**이 변경과 무관한 기존 환경 문제**지만, 한 모듈만 재보려다 걸리기 쉽습니다.

### 6. `load_config` 는 이미 공개였습니다

`helpers.__all__` 에는 있었고(`helpers.py:17`) 빠진 곳은 패키지 루트뿐이었습니다.
루트에 올린 것은 **추가**라 하위호환을 깨지 않습니다.

## 남긴 빚

`__init__.py` 의 `except ImportError` 폴백에 `load_config = None` 을 **한 줄 더
늘렸습니다.** 기존 패턴을 따른 것이지만 문제를 키운 것도 사실입니다.
[#73](https://github.com/visualmoney/vm-stock-kis/issues/73) 으로 남겼습니다.

`#70` 이 이 결과물의 일부를 지웁니다 — 불리언 전용 sentinel 처리와
`Virtual (y/n)` 프롬프트입니다. **예정된 재수정**이고 #70 본문에 적어 두었습니다.

## 변경 파일

- `src/vmkis/helpers.py` - 프로필 키 상수 3개 + `_validate_profile` 신설.
  `create_client` 의 `.get(..., False)` 제거. `save_config_interactive` 가 같은 상수 사용
- `src/vmkis/__init__.py` - `load_config` 를 루트로 공개
- `examples/01_basic/{get_balance,get_quote,place_order,realtime_price}.py` -
  복붙 `load_config` 4벌 삭제, import 로 대체 (`import yaml` 도 함께 제거)
- `tests/unit/test_helpers.py` - `test_virtual_key_defaults_to_false` 를 뒤집고
  `TestProfileValidation` 6건 신설
- `tests/unit/test_load_config_get_quote.py` → `tests/unit/test_config_examples.py` -
  예제 복사본 대신 라이브러리를 대상으로
- `tests/unit/test_compat_aliases.py` - 프로필 키 채움

## 테스트 결과

```console
uv run pytest -m 'not requires_api'    1058 passed, 8 skipped, 17 deselected
coverage                               91.58%  (게이트 90)
helpers.py                             리포트에 없음 = 100% (skip_covered = true)
ruff check / format                    통과
lint-imports --no-cache                2 kept, 0 broken
```

되돌려 확인: **결함 복원 시 7건 실패**, 복원 해제 후 1058건 통과. 위 2번 참고.

## 다음 할 일

- [ ] #70 착수 — `blocked` 는 이 이슈가 닫히면 제거
- [ ] #72 python-dotenv 를 테스트 그룹으로 (USER_GUIDE 갱신 동반)
- [ ] #73 helpers import 실패를 조용한 `None` 대신 예외로
