# 2026-08-29 - #50 import-linter 계약 도입 개발 일지

**이슈**: [#50](https://github.com/visualmoney/vm-stock-kis/issues/50)
`ci: import-linter 계약으로 아키텍처 역방향 의존 회귀 차단`
**프롬프트**: [`2026-08-29_01_issue50_import_linter.md`](../prompts/2026-08-29_01_issue50_import_linter.md)

## 걸린 것 1 — 계약이 패키지의 **1/4 만** 보고 있었습니다

계약을 넣고 처음 돌렸을 때 나온 것은 위반이 아니라 이것입니다.

```text
Module 'vmkis.utils' does not exist.
```

`src/vmkis` 의 디렉터리 18개 중 **13개에 `__init__.py` 가 없습니다.** 암묵적
네임스페이스 패키지이고, grimp 은 상위 패키지 하나만 받으면 이들을 건너뜁니다.

```python
>>> len(grimp.build_graph("vmkis").modules)
20      # utils / client / responses / api / adapter 가 통째로 없음
>>> len(grimp.build_graph("vmkis", "vmkis.utils", "vmkis.client",
...                       "vmkis.responses", "vmkis.api", "vmkis.adapter").modules)
92      # = .py 79개 + 네임스페이스 패키지 13개
```

`root_packages`(복수)에 네임스페이스 부분을 전부 나열해 해결했습니다.

**여기서 무서운 것은 죽는 쪽이 아닙니다.** 빠진 것이 계약의 `source_modules` 면
위처럼 죽지만, `forbidden_modules` 쪽이거나 아직 계약에 안 걸린 서브패키지면
**아무 말 없이 초록입니다.** `__init__.py` 없는 서브패키지가 새로 생기면 정확히
그 상태가 됩니다.

그래서 `tests/unit/test_import_contracts.py::test_contract_graph_covers_every_source_module`
을 만들었습니다. `src/vmkis` 의 모든 `.py` 가 그래프에 있는지만 봅니다.

> `__init__.py` 13개를 추가하는 쪽은 택하지 않았습니다. 배포되는 패키지의 구조를
> 바꾸는 별건이고, #50 의 범위가 아닙니다. 필요하다면 별도 이슈입니다.

## 걸린 것 2 — 세 번째 역방향 간선이 있었습니다

이슈 본문과 착수 전 제 AST 스캔이 **똑같이** 이렇게 판정했습니다.

> `utils` 는 vmkis 내부를 하나도 import 하지 않는다

계약을 돌리자 위반 9건이 나왔고, 전부 한 줄에서 나왔습니다.

```python
# src/vmkis/utils/diagnosis.py:4
import vmkis
```

```text
vmkis.utils is not allowed to import vmkis.adapter:
-   vmkis.utils.diagnosis -> vmkis (l.4)
    vmkis -> vmkis.public_types (l.30)
    vmkis.public_types -> vmkis.api.account.order (l.9)
    vmkis.api.account.order -> vmkis.adapter.account_product.order_modify (l.15)
```

**`import <루트패키지>` 한 줄은 간선 하나처럼 보이지만 그래프에서는 상위
전체입니다.** `vmkis/__init__.py` 가 `kis` · `api` · `client` · `scope` 를 전부
끌고 오기 때문입니다.

제 스캔이 놓친 이유가 정확히 이것입니다. `vmkis.client.page` 는 `parts[1]` 이
`client` 라 그룹이 잡히지만, `vmkis` 는 `parts[1]` 이 없어 `None` 그룹으로
빠집니다. **"그룹 대 그룹"으로만 보는 눈에는 루트 파사드가 안 보입니다.**
사람이 쓴 AST 스캔을 도구로 대체하는 이유가 이런 것입니다.

`diagnosis.check()` 가 루트에서 쓰는 값은 `__version__` 과 `__package_name__`
둘뿐이고, 둘 다 원래 `vmkis/__env__.py` 에 있습니다(루트는 재export만 합니다).
`from vmkis import __env__` 로 바꿨습니다 — #18 이 `utils/retry.py` 에서 한 것과
같은 발상입니다. **필요한 것만 아래에서 가져옵니다.**

```python
>>> g.find_modules_directly_imported_by("vmkis.utils.diagnosis")
['vmkis.__env__']
```

## 걸린 것 3 — `ignore_imports` 는 **위치를 보지 않습니다**

`client/messaging.py:52` 의 지연 import 를 면제로 등록했습니다. 그런데:

```text
검증 3: 그 import 를 파일 상단으로 승격 → Contracts: 2 kept, 0 broken
```

면제는 **모듈 쌍**(`vmkis.client.messaging -> vmkis.api.auth.websocket`) 단위라
함수 안인지 모듈 레벨인지 구분하지 못합니다. 모듈 레벨로 올라가면 패키지가
로드 불능이 되는데(불변식 3번) 계약은 초록입니다.

기존 AST 테스트(`test_client_websocket_does_not_import_api`)는 `client/websocket.py`
만 봐서 이 자리를 덮지 않았습니다. `test_messaging_keeps_api_import_lazy` 를
추가했습니다.

그리고 그 지연 import 에는 **사유 주석이 없었습니다** — 불변식 3번을 어기고 있던
상태입니다. 함께 달았습니다.

## 되돌려 확인 (완료 기준)

이슈의 완료 기준은 "통과"가 아니라 **"일부러 위반을 만들면 실패한다"** 입니다.
5건 전부 실측했습니다.

| # | 되살린 결함 | 결과 |
|---|---|---|
| 1 | `utils/repr.py` 에 `from vmkis.client.exceptions import ...` | ✅ `utils ... BROKEN` |
| 2 | `client/page.py` 에 모듈 레벨 `from vmkis.api.auth.websocket import ...` | ✅ `client ... BROKEN` — 면제는 `messaging.py` 에만 걸림이 확인됨 |
| 3 | `messaging.py` 의 면제된 import 를 모듈 레벨로 승격 | ❌ **계약은 통과** (걸린 것 3) |
| 4 | `root_packages` 에서 `vmkis.utils` 제거 | ✅ `lint-imports` 사망 + 가드 테스트 실패 |
| 5 | 3번과 같은 조작 | ✅ 새 AST 테스트가 실패 |

3번이 계약의 한계이고 5번이 그것을 메웁니다. **AST 테스트를 남기라는 이슈의
판단이 옳았고, 남기는 정도가 아니라 한 건 더 필요했습니다.**

## 판단한 것

- **`exclude_type_checking_imports = true`** — 불변식 1번이 `if TYPE_CHECKING:`
  안의 상위 import 를 명시적으로 허용합니다(`vmkis.kis` 가 그렇게만 import 됩니다).
  이 옵션이 없으면 계약이 불변식 1번을 위반으로 잡습니다. 불변식 2번이 막는 것은
  **모듈 레벨** 간선이므로 의미도 맞습니다.
- **`utils` 계약의 금지 목록에 최상위 파사드 5개 추가** — 이슈 본문의 7개에
  `exceptions` · `types` · `public_types` · `helpers` · `simple` 을 더했습니다.
  특히 `vmkis.exceptions` 는 `client` 와 `responses` 를 재export하므로, 이것을
  경유하면 #18 이 없앤 간선이 그대로 되살아납니다.
- **상한 `<3`** — ruff 와 이유가 다릅니다. 계약은 `pyproject.toml` 에 명시되어
  있어 규칙셋이 조용히 바뀌지 않지만, 메이저 업그레이드에서 grimp 의 import 탐지
  범위(지연 import·TYPE_CHECKING 처리)가 바뀌면 **같은 계약의 의미가 달라집니다.**
- **pre-commit 훅에는 넣지 않았습니다** — 이슈 범위 밖이고, `lint-imports` 는
  설치된 패키지 그래프가 필요해 `language: system` + 동기화된 venv 를 전제합니다.
  CI 의 `lint` 잡이 이미 막습니다.

## 이슈 본문의 오류 1건

> `ARCHITECTURE.md` 불변식 4번("import-linter 도입 권장")을 완료로 갱신

`ARCHITECTURE.md` 불변식 4번은 **"`event/` 는 이 그림에 포함됩니다"** 입니다.
"import-linter 도입 권장"은
`docs/reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md:428` 의
**권장사항 4번**이고 보고서는 동결 문서입니다.

기계화된 것은 **불변식 2번**이므로 그쪽을 갱신했습니다.

## 변경 파일

- `pyproject.toml` — `lint` 그룹에 `import-linter`, `[tool.importlinter]` 계약 2개
- `.github/workflows/ci.yml` — `lint` 잡에 `Import contracts` 스텝
- `src/vmkis/utils/diagnosis.py` — `import vmkis` → `from vmkis import __env__`
- `tests/unit/utils/test_diagnosis.py` — 위에 맞춰 monkeypatch 대상 변경
- `src/vmkis/client/messaging.py` — 지연 import 사유 주석 (불변식 3번)
- `tests/unit/test_import_contracts.py` — **신규.** 그래프 커버리지 + 지연 import 위치
- `docs/architecture/ARCHITECTURE.md` — 불변식 2번에 기계화·한계·세 번째 간선 기록

## 테스트 결과

```text
uv run lint-imports         Contracts: 2 kept, 0 broken.  (92 files, 428 dependencies)
uv run pytest -m 'not requires_api and not performance'
                            1023 passed, 7 skipped, 47 deselected
coverage                    92%  (게이트 90)
ruff check / format         통과
uv lock --check             통과
```

## 남은 것

둘 다 `needs-decision` 이슈로 냈습니다. **"다음에 정하자"를 일지에만 적으면
아무도 다시 찾지 않습니다.**

- [#63](https://github.com/visualmoney/vm-stock-kis/issues/63)
  `event → api` 간선 판정 — 계약 확장을 막는 유일한 미결입니다.
- [#64](https://github.com/visualmoney/vm-stock-kis/issues/64)
  `__init__.py` 없는 디렉터리 13개 — `root_packages` 를 손으로 유지해야 하는
  **원인**입니다. 가드 테스트는 증상만 막습니다.
