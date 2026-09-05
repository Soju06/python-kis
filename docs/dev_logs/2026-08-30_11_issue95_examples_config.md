# 2026-08-30 - #95 예제 `--config` 기본값 개발 일지

이슈 [#95](https://github.com/visualmoney/vm-stock-kis/issues/95).
예제의 `--config` 기본값이 저장소에 없는 `config.yaml` 을 가리킵니다.

## 걸린 것 1 — 7곳이 아니라 28곳이었습니다

이슈는 `default="config.yaml"` 7건을 셉니다. 예제 전체를 훑으니 **파일 12개에
28곳**이었습니다.

| 유형 | 건수 | 사용자에게 무엇으로 보이나 |
|---|---|---|
| `default="config.yaml"` | 7 | 예제가 실행되지 않습니다 |
| `os.path.join(os.getcwd(), "config.yaml")` | 7 | **두 번째 기본값.** 함수를 직접 부르면 여기 걸립니다 |
| `config.yaml이 루트에 있어야 함` (docstring) | 8 | 없는 파일을 만들려 합니다 |
| 나머지 문구 | 6 | 안내 메시지가 없는 파일을 가리킵니다 |

`#75` 가 고쳤다고 되어 있는 `01_basic/` 에도 **문구가 4건 남아 있었습니다.**
`03_advanced/02_performance_analysis.py` 는 `--config` 가 아예 없는데 실행
조건에만 `config.yaml` 이 적혀 있었습니다 — 기본값만 세면 안 보이는 자리입니다.

여기에 예제 README 2건, 그리고 **`src/vmkis/types.py:97`** 이 더 있었습니다.
라이브러리 자신의 docstring 이 `create_client("config.yaml")` 을 가르치고
있었습니다.

**전부 대상 목록을 손으로 적어서 생겼습니다.** 그래서 이번에는 목록을 적지 않고
`examples/**/*.py` 를 전부 훑어 유형별로 치환했습니다.

## 걸린 것 2 — 이슈가 제안한 검사가 통과할 수 있었습니다

이슈의 완료 기준은 이렇습니다.

> `--config` 의 default 가 전부 같은 값인지

**그 검사는 11개가 똑같이 틀려도 통과합니다.** 오늘 세션 종료 일지가 적은
"게으르게 만든 구현"이 정확히 이 형태입니다 — 올바른 테스트는 통과하는데
아무것도 검사하지 않습니다.

라이브러리에 이미 정답이 있었습니다.

```python
# src/vmkis/helpers.py:24
DEFAULT_CONFIG_PATH = "configs/account_profiles.yaml"
```

그래서 서로 대조하지 않고 **`create_client` 자신의 기본값과 대조**합니다.

```python
EXPECTED_CONFIG_DEFAULT = inspect.signature(create_client).parameters["config_path"].default
```

비공개 `helpers.DEFAULT_CONFIG_PATH` 를 import 하지 않은 이유: 예제가 쓰는 것은
공개 API 이고, 검사도 같은 것을 봐야 합니다. 라이브러리가 경로를 바꾸면 검사가
따라옵니다.

### 그래도 부족합니다 — 이름 검사를 따로 뒀습니다

기본값만 보면 28곳 중 **21곳이 검사 밖**입니다. docstring·폴백·안내 문구는
argparse 를 거치지 않기 때문입니다. 그래서 `config.yaml` 이라는 **이름 자체가
남아 있는지**를 별도로 봅니다. 이쪽이 28곳 전부를 덮습니다.

## 되돌려 확인한 것 — 다섯 방향

| 무엇을 되돌렸나 | 결과 |
|---|---|
| 예제 1개의 기본값을 `config.yaml` 로 | **2건 실패** (기본값 검사 + 이름 검사) |
| 추출기가 `--config` 를 못 찾게 | 2건 실패 — *"--config 기본값을 0개만 찾았습니다"* |
| 기대값을 손으로 `"config.yaml"` 로 박기 | **13건 실패** |
| README 1곳을 `cat config.yaml` 로 | 1건 실패 |
| `_example_docs()` 를 빈 목록으로 | 1건 실패 — *"예제 README 를 0개만 찾았습니다"* |

세 번째가 중요합니다. 기대값을 손으로 적는 순간 라이브러리와 분리되고, 그러면
라이브러리가 경로를 바꾼 날 검사가 조용히 거짓이 됩니다.

## 손대지 않은 것

**`examples/tutorial_basic.ipynb`** — `config.yaml` 이 6곳 있지만 경로만
문제가 아닙니다. 셀 5가 **폐기된 평면 스키마**를 가르칩니다.

```yaml
id: "YOUR_ID"
account: "YOUR_ACCOUNT"
appkey: "YOUR_APPKEY"
secretkey: "YOUR_SECRETKEY"
```

지금 스키마는 `apps` / `accounts` / `default_account` 3블록입니다. 셀 6 에는
*"위 config.yaml 형식은 더 이상 쓰지 않습니다"* 라는 메모가 이미 붙어
있습니다. **경로만 고치면 틀린 것을 최신처럼 보이게 만듭니다** — `#70` 이
`VmKis(virtual=True)` 를 `VmKis(paper=True)` 로 바꾸며 밟은 함정과 같습니다.
별도 이슈로 냈습니다.

**`docs/` 의 살아 있는 문서 10개, 32곳** — `SIMPLEKIS_GUIDE.md` 만 11곳입니다.
`#95` 는 예제 이슈이므로 범위를 넘기지 않고 별도 이슈로 냈습니다.

## 제가 만든 사고

되돌리기 확인 스크립트의 복구 경로에 이렇게 적었습니다.

```bash
git checkout -- tests/unit/test_examples_signatures.py 2>/dev/null || cp $SP/checker.orig.py ...
```

그 파일은 **커밋되지 않은 상태**였습니다. `git checkout` 이 성공하면서 새로
쓴 검사 5건이 통째로 사라졌고(49건 → 15건), `||` 폴백은 돌지 않았습니다.

세션 종료 일지가 어제 적은 것과 **같은 형태**입니다.

> `git branch -m` 을 `||` 폴백에 넣어 로컬 `main` 을 개명했습니다. …
> **되돌리기 어려운 명령을 폴백에 넣은 것이 잘못**입니다.

스크래치패드 사본이 있어 복구했습니다. **복구용 사본을 먼저 만들어 둔 것이
값을 했습니다.**

## 변경 파일

- `examples/` 12개 `.py` — 28곳
- `examples/02_intermediate/README.md`, `examples/03_advanced/README.md` — 2곳
- `src/vmkis/types.py` — 모듈 docstring 1곳
- `tests/unit/test_examples_signatures.py` — 검사 5개 추가

## 테스트 결과

```text
uv run pytest -m 'not requires_api and not performance' --cov
  1201 passed, 7 skipped, 47 deselected in 41.33s
```

네트워크 없이 안내 문구도 확인했습니다.

```console
$ python examples/02_intermediate/01_multiple_symbols.py --config /nonexistent/x.yaml
❌ /nonexistent/x.yaml를 찾을 수 없습니다.
   저장소 루트에서 실행하거나 configs/template_account_profiles.yaml 을
   configs/account_profiles.yaml 로 복사해 채우세요.
```
