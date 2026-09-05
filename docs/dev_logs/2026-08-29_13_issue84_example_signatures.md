# 2026-08-29 - #84 예제 7개가 없는 인자를 넘기던 문제 개발 일지

## 작업 내용

`create_client(config_path, profile=profile)` → `account=account`. 예제 7개에서
파일마다 **네 군데**를 고쳤고, 같은 결함을 다시 잡는 단위 테스트를 넣었습니다.

## 무엇에 걸렸는가

### 1. "왜 CI 가 못 잡았나"가 이 작업의 본체였습니다

고치는 것 자체는 `sed` 한 줄입니다. 진짜 질문은 **8개월치 개명이 지나가는 동안
아무도 못 봤다**는 것입니다.

`tests/integration/test_examples_run_smoke.py` 가 이미 있었습니다.

```python
@pytest.mark.skipif(os.environ.get("RUN_INTEGRATION") != "1", ...)
def test_examples_get_quote_paper_smoke():
    proc = subprocess.run([sys.executable, str(script), "--config", str(cfg)], ...)
```

두 가지가 겹쳐 무력했습니다.

1. **CI 가 `RUN_INTEGRATION` 을 주지 않습니다.** 통째로 skip 입니다
2. 예제를 **실제로 실행**하므로 자격증명과 네트워크가 필요합니다

**그런데 이 결함은 둘 다 필요 없습니다.** `create_client` 는 호출되는 순간
`TypeError` 로 죽으므로 서버에 닿을 일이 없습니다.

### 2. `--help` 로 돌리는 것은 답이 아닙니다

처음에 떠올린 방법입니다 — 자격증명 없이 도니까요. **안 됩니다.**

```python
parser.parse_args()          # --help 는 여기서 SystemExit(0)
kis = create_client(...)     # 여기까지 오지 않습니다
```

argparse 가 `create_client` 보다 먼저 끝납니다. 반환코드 0 을 보고 통과시키면
**아무것도 검사하지 않는 초록불**이 됩니다.

### 3. 그래서 AST 로 시그니처를 대조합니다

`tests/unit/test_examples_signatures.py` — `examples/` 를 파싱해
`create_client`·`VmKis`·`KisAuth`·`SimpleKIS`·`save_config_interactive` 호출을
찾고, 키워드 인자와 위치 인자 개수를 `inspect.signature` 와 맞춰 봅니다.

- 자격증명·네트워크 없음. **단위 테스트라 CI 가 항상 돌립니다**
- 시그니처를 코드에서 읽으므로 **다음 개명에도 따라옵니다** (하드코딩한 목록이
  아닙니다)

### 4. 검사기가 아무것도 안 보는 상태를 따로 막았습니다

`_violations()` 가 0건이면 테스트는 통과합니다. 그런데 **경로가 틀려도 0건**이고
**예제가 `create_client` 를 그만 써도 0건**입니다. 그때는 검사가 아니라 장식입니다.

```python
def test_checker_actually_sees_the_examples():
    assert len(files) >= 10
    assert "create_client" in seen
```

2026-08-28 에 `DOMESTIC_QUOTE.tr_real` 을 `"WRONG_TR_ID"` 로 바꿔도 165건이 전부
통과했던 일과 같은 종류의 구멍입니다.

## 회귀 확인 — 두 겹으로 했습니다

**① 실제 예제에 결함을 되살렸습니다.**

```console
$ sed -i 's/account=account/profile=account/' examples/02_intermediate/01_multiple_symbols.py
$ python -m pytest tests/unit/test_examples_signatures.py -q
FAILED ...::test_example_calls_match_public_signatures[examples/02_intermediate/01_multiple_symbols.py]
1 failed, 14 passed
```

```text
examples/02_intermediate/01_multiple_symbols.py:36 — create_client(...) 에
`profile=` 를 넘깁니다. 받는 이름은 ['account', 'config_path', 'keep_token'] 입니다
```

**② 결함을 테스트 안에 문자열로 박아 뒀습니다.**

```python
def test_checker_catches_the_original_defect():
    problems = _violations("create_client(config_path, profile=profile)\n", "<결함 재현>")
    assert problems
```

①은 지금 잡히는지를 보고, ②는 **예제가 앞으로 어떻게 바뀌든 검사기 자체의
성능**을 계속 검증합니다. ①만 있으면 나중에 예제에서 `create_client` 가 사라질 때
검사기가 죽은 줄도 모릅니다.

## 옆에서 확인한 것 — 문서의 프로파일 어휘

`examples/*/README.md` 가 `VMKIS_PROFILE` 과 `--profile virtual` 을 안내하고
있었습니다. 둘 다 없는 것입니다.

- 환경변수는 `helpers._env("ACCOUNT")` → **`VMKIS_ACCOUNT`**
- 값은 `real`/`virtual` 이 아니라 설정의 `accounts:` 아래 **키 이름**
  (`acc_paper1` 등). `configs/template_account_profiles.yaml` 참고
- `virtual: true` 는 앱의 `mode: "paper"` 가 됐습니다 (#75)

## 손대지 않은 것

`examples/02_intermediate/` 와 `03_advanced/` 의 `--config` 기본값이
`config.yaml` 입니다. `01_basic/` 은 `configs/account_profiles.yaml` 이고요.
저장소 루트에 `config.yaml` 은 없으므로 이 예제들은 **"파일을 찾을 수 없습니다"를
찍고 정상 종료**합니다. 크래시가 아니라 안내이고, #84 의 완료 기준에도 없어
건드리지 않았습니다. 기본값을 통일할지는 별도 판단입니다.

`test_examples_run_smoke.py` 도 그대로 뒀습니다. 그것이 검사하는 것(예제가
실제 서버와 끝까지 도는가)은 여전히 자격증명이 필요한 별개의 성질입니다.
**이번에 넣은 것은 그 대체가 아니라 앞단입니다.**

## 변경 파일

- `examples/02_intermediate/*.py` 5개 · `examples/03_advanced/*.py` 2개
  - 매개변수 · `create_client` 호출 · `--profile` → `--account` · 전달부
- `examples/README.md` · `02_intermediate/README.md` · `03_advanced/README.md`
- `tests/unit/test_examples_signatures.py` — 신규. 회귀 15건

## 테스트 결과

```console
$ python -m pytest tests/unit -q
1050 passed, 5 skipped          # 이전 1035 + 신규 15

$ ruff check . && ruff format --check . && python -m compileall -q examples/
All checks passed! / 211 files already formatted / OK
```
