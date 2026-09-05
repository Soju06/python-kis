# 2026-08-29 - #73 helpers import 실패를 조용한 None 대신 예외로 개발 일지

## 작업 내용

`vmkis/__init__.py` 의 `try/except ImportError: ... = None` 폴백 2벌을 지우고,
그것이 되살아나면 실패하는 테스트를 넣었습니다.

```diff
-try:
-    from vmkis.simple import SimpleKIS
-except ImportError:
-    SimpleKIS = None
-
-try:
-    from vmkis.helpers import create_client, save_config_interactive
-except ImportError:
-    create_client = None
-    save_config_interactive = None
+from vmkis.helpers import create_client, save_config_interactive
+from vmkis.simple import SimpleKIS
```

## 무엇에 걸렸는가

### 1. 이슈 본문이 코드보다 낡아 있었습니다

본문은 폴백에 `load_config = None` 이 있다고 적었지만 그 줄은 이미 없습니다.
#75(`af582e2`)가 `helpers.load_config` 를 `vmkis.config.load_kis_config` 로
옮기면서 루트 공개도 내렸습니다. **이슈를 읽고 바로 `sed` 를 짜지 말고 파일을
먼저 열어야 합니다.** 완료 기준 자체는 그대로 유효했습니다.

### 2. `SimpleKIS` 폴백은 애초에 걸릴 수 없는 자리였습니다 — 그래서 더 나쁩니다

범위 판단을 하려고 `simple.py` 를 열었더니 import 가 이것뿐입니다.

```python
from vmkis.kis import VmKis
```

그런데 `__init__.py` 는 **그 위에서 이미** `from vmkis.kis import VmKis` 를
무조건 합니다. 즉 `vmkis.kis` 가 실패하면 `SimpleKIS` 의 `try` 에 닿기 전에
패키지가 죽습니다. 이 `except ImportError` 가 잡을 수 있는 것은 **`simple.py`
자신의 버그**뿐이고, 그건 정확히 숨기면 안 되는 것입니다.

폴백이 "의존성이 없을 때를 대비한 안전장치"처럼 보이지만 실제로 대비하는
대상이 하나도 없었습니다. **결함 은닉 기능만 남은 코드**입니다. 같은 결함
등급이므로 #73 범위에 넣었고, 판단 근거를 이슈 본문에도 적었습니다.

### 3. 테스트에서 고장을 어떻게 흉내낼 것인가

`vmkis.helpers` 를 실제로 망가뜨리지 않고 "import 가 실패하는 상태"를 만들어야
했습니다. `sys.modules[name] = None` 이 그 일을 합니다 — CPython 이 그 이름의
import 를 `ImportError` 로 중단시키는 표준 동작입니다.

```python
sys.modules["vmkis.helpers"] = None
import vmkis          # 폴백이 있으면 통과하고, 없으면 ImportError
```

**하위 프로세스가 필요합니다.** 테스트 세션에서는 `vmkis` 가 이미 import 되어
`sys.modules` 에 캐시돼 있어서, 같은 프로세스 안에서는 `__init__.py` 가 아예
다시 실행되지 않습니다. 그 상태로 짜면 테스트가 **아무것도 검사하지 않고
통과**합니다.

### 4. 폴백을 지우니 import 블록이 하나로 합쳐져 정렬이 어긋났습니다

`try:` 문이 사이에 있을 때는 그것이 블록 경계 역할을 해서 ruff 의 `I001` 이
조용했습니다. 폴백을 지우자 `__env__` 부터 `simple` 까지가 **한 블록**이 되어,
`ruff check --fix` 가 알파벳순으로 재배열했습니다. 그 결과가 이렇습니다.

- `helpers` 가 `kis` 앞으로 올라가 `# 핵심 인증/클래스` 그룹을 쪼갬
- `simple` 은 맨 뒤로 밀려나 helpers 와 떨어짐 — 새로 쓴 주석의 "이 두 줄"이
  가리킬 대상이 사라짐

`# isort: split` 으로 핵심 블록과 초보자용 유틸 블록을 갈랐습니다. 왜 그 지시자가
있는지를 주석에 적어 뒀습니다. **없으면 다음 사람이 "쓸데없는 주석"으로 지웁니다.**

## 회귀 확인 — 결함을 되살렸습니다

`try/except` 를 그대로 되돌리고 돌린 결과입니다.

```console
$ python -m pytest tests/unit/test_helpers_import_contract.py -q
FAILED ...::test_broken_submodule_is_not_swallowed[vmkis.helpers]
FAILED ...::test_broken_submodule_is_not_swallowed[vmkis.simple]
2 failed, 1 passed
```

실패 메시지가 증상을 그대로 재현합니다.

```text
`vmkis.simple` 이 고장 났는데 `import vmkis` 가 통과했습니다.
공개 이름이 조용히 None 이 됩니다:
SWALLOWED <function create_client ...> <function save_config_interactive ...> None
```

`test_public_helper_names_are_usable` 1건은 폴백이 있어도 통과합니다 —
정상 설치에서는 폴백이 걸리지 않으니 당연합니다. **그 1건만 있었다면 이 이슈를
못 잡습니다.** 반대편(이름을 떨어뜨리지 않았는지)을 지키는 용도로만 둡니다.

## `pyproject.toml` — 필수 사유가 순환이었습니다

```text
pyyaml 이 필수인 이유  ← "없으면 __init__.py 가 삼켜서 조용히 None 이 되니까"
```

**나쁜 실패 모드를 덮으려고 의존성을 고정한 것**입니다. 폴백이 사라졌으니 그
근거도 사라집니다. 실제 근거로 바꿔 적었습니다 — 예제 9개와 문서 첫 화면이
`from vmkis import create_client` 로 시작하고, pyyaml 은 전 플랫폼 휠이 있어
필수로 두는 비용이 거의 없습니다.

## 변경 파일

- `src/vmkis/__init__.py` - 폴백 2벌 제거, `# isort: split`, 이력 주석
- `tests/unit/test_helpers_import_contract.py` - 신규. 회귀 3건
- `pyproject.toml` - pyyaml 필수 사유 주석 교체

## 테스트 결과

```console
$ python -m pytest tests/unit -q
1035 passed, 5 skipped

$ ruff check src/ tests/unit/test_helpers_import_contract.py
All checks passed!

$ lint-imports
Contracts: 2 kept, 0 broken.
```

## 옆에서 발견한 것 — #78 에 넘겼습니다

`docs/SIMPLEKIS_GUIDE.md:136` 이 아직 이렇게 적고 있습니다.

```python
from vmkis.helpers import load_config
```

#75 에서 지운 이름입니다. 따라 하면 `ImportError` 입니다. #78("사용자 문서가
존재하지 않는 VmKis 시그니처를 적고 있습니다")과 같은 등급이라 그쪽에
코멘트로 넘겼습니다. **이 PR 에서 함께 고치지 않았습니다** — 범위를 조용히
넓히면 되돌릴 때 무엇이 무엇 때문인지 갈라내지 못합니다.
