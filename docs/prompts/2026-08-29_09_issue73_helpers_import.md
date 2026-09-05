# 2026-08-29 - #73 helpers import 실패를 조용한 None 대신 예외로

## 사용자 요청

> main으로 체크아웃하고 #73 착수해줘

## 분석

### 대상

`src/vmkis/__init__.py` 의 `try/except ImportError` 폴백 2벌.

```python
try:
    from vmkis.simple import SimpleKIS
except ImportError:
    SimpleKIS = None

try:
    from vmkis.helpers import create_client, save_config_interactive
except ImportError:
    create_client = None
    save_config_interactive = None
```

### 이슈 본문과 현재 코드의 차이

이슈 본문은 폴백에 `load_config = None` 이 있다고 적었지만 **지금은 없습니다.**
#75(`af582e2`)가 `helpers.load_config` 를 삭제하고 `vmkis.config.load_kis_config`
로 옮기면서 루트 공개도 함께 내렸습니다. 이슈 본문이 그 시점보다 앞섭니다.
완료 기준 자체는 그대로 유효합니다.

### 폴백에 기대는 코드가 있는가 — 없습니다

```console
$ grep -rn 'create_client is None|save_config_interactive is None|SimpleKIS is None' src/ examples/ scripts/
(0건)
```

반대로 **예제 9개**가 `from vmkis import create_client` 를 씁니다. 폴백이 걸리면
그 9개가 전부 `TypeError: 'NoneType' object is not callable` 로 죽습니다.

### 영향 받는 모듈

- `src/vmkis/__init__.py` — 폴백 제거
- `pyproject.toml` — pyyaml 필수 사유 주석. 현재 근거가 "폴백이 삼키니까"입니다
- `tests/unit/` — 검사하는 테스트가 0건

## 계획

1. 두 `try/except` 를 평범한 import 로 바꾸고, 폴백을 왜 지웠는지 주석에 남깁니다
2. `import vmkis` 가 helpers/simple 의 결함을 가리지 않는지 서브프로세스 테스트
3. `pyproject.toml` 의 pyyaml 주석을 실제 근거로 갱신
4. `SimpleKIS` 쪽 범위 판단을 이슈 본문에 기록

## 결과

폴백 2벌 제거 + 회귀 테스트 3건. 상세는
[docs/dev_logs/2026-08-29_10_issue73_helpers_import.md](../dev_logs/2026-08-29_10_issue73_helpers_import.md).
