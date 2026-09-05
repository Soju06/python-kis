# 2026-08-29 - #78 문서가 없는 API 를 적고 있던 문제 개발 일지

## 작업 내용

문서 8개의 python 예제를 실제 API 에 맞췄고, **문서 예제를 CI 에서 검사하는
테스트**를 넣었습니다(완료 기준 2번).

## 무엇에 걸렸는가

### 1. 검사기를 먼저 만든 것이 이 작업의 전부였습니다

이슈 본문은 3곳을 지목했습니다. 512줄짜리 `REGIONAL_GUIDES.md` 를 눈으로 훑을
생각을 하다가 **검사기를 먼저 짰습니다.** 결과가 이렇습니다.

| | 건수 |
|---|---|
| 이슈 본문이 적어 둔 것 | 3 |
| 앞선 세션의 코멘트가 더한 것 | 2 |
| **검사기가 새로 찾은 것** | **7** |

새로 나온 것들입니다.

```text
docs/FAQ.md:54    VmKis(paper=True)          ← VmKis 에 paper 인자가 없습니다
docs/FAQ.md:45    VMKIS_REAL_TRADING          ← 그런 환경변수가 없습니다
docs/FAQ.md:385   from vmkis import setLevel  ← 루트에 없습니다 (vmkis.logging)
docs/developer/DEVELOPER_GUIDE.md:597  vmkis.responses.types.KisQuote  ← 없습니다
docs/guidelines/REGIONAL_GUIDES.md:304 from vmkis.mock import MockKisClient ← 모듈 자체가 없습니다
docs/rules/TEST_RULES_AND_GUIDELINES.md:8  KisAuth(virtual=)  ← #70 에서 놓친 곳
CONTRIBUTING.md:231  from vmkis.types import Quote  ← public_types 입니다
```

`docs/rules/` 는 **어제 #70 개명에서 제가 빠뜨린 디렉터리**입니다. 대상 목록을
손으로 적었기 때문입니다. 검사기는 손으로 적지 않습니다.

### 2. `FAQ.md:54` 는 제가 어제 더 나쁘게 만든 자리입니다

#70 에서 `virtual=True` → `paper=True` 로 일괄 치환했는데, 그 줄이 하필
**`VmKis(...)` 호출 안**이었습니다. `paper` 는 `KisAuth` 의 인자입니다.

```python
kis = VmKis(id=..., appkey=..., secretkey=..., paper=True)   # 그때도 지금도 TypeError
```

**틀린 이름을 다른 틀린 이름으로 바꾼 것**입니다. 개명 PR 에서 "이름만 바꾸면
버그를 세탁한다"고 두 곳(`USER_GUIDE`, 노트북)은 잡아냈는데, 이건 못 봤습니다.
눈으로 보는 방식의 한계가 그대로 드러납니다.

### 3. `REGIONAL_GUIDES` 의 "글로벌" 절은 시그니처 문제가 아니었습니다

`server: mock` 설정 블록, `mock:` 블록, `vmkis.mock.MockKisClient`, 단위 테스트
예제까지 — **기능 하나가 통째로 허구**였습니다. 존재한 적이 없습니다.

이름을 고칠 수가 없습니다. 고칠 이름이 없으니까요. **허구를 지우고 실제로 되는
것을 적었습니다** — `requests_mock` 으로 HTTP 계층을 막거나(이 저장소 테스트가
그렇게 합니다) 모의투자 계좌를 쓰는 것.

같은 이유로 3.1·3.2 비교표의 "글로벌 (모의)" 열도 지웠습니다.

### 4. 코드가 틀린 경우를 만났습니다 → #87

FAQ Q3 에 **동작하는** 예제를 적으려고 형태를 하나씩 돌려 봤습니다.

```text
실패  VmKis(None, paper_auth)     ← create_client 가 모의 계좌에 쓰는 바로 그 형태
OK    VmKis(live_auth, paper_auth)
OK    VmKis(live_auth)
OK    VmKis(id=, account=, appkey=, secretkey=)
OK    VmKis(kw + paper_*)
```

`create_client` 가 **모의 계좌에서 항상 `ValueError: id를 입력해야 합니다`** 로
죽습니다. 그리고 **템플릿 설정의 기본 계좌가 모의**입니다.

문서가 틀린 게 아니라 코드가 틀린 경우입니다. 고치려면 "실전 인증 없는 모의
전용 클라이언트"를 인정할지부터 정해야 해서(실전 도메인 토큰 발급 경로가 얽혀
있습니다) [#87](https://github.com/visualmoney/vm-stock-kis/issues/87) 로 열었습니다.
문서에는 지금 **되는 형태만** 적고, 안 되는 형태를 각주로 달았습니다.

### 5. "모듈이 없다"를 실패로 만들면 안 됩니다

첫 판에서 `DEVELOPER_GUIDE` 의 확장 가이드가 걸렸습니다.

```python
from vmkis.api.my_api import ...        # 자리표시자입니다
```

**확인할 수 없는 것과 틀린 것은 다릅니다.** import 되는 모듈 안에서만 이름을
검증하도록 바꿨습니다. `vmkis.helpers` 는 존재하므로 `load_config` 가 없다는 것은
여전히 잡힙니다.

`vmkis.mock` 은 그 규칙 때문에 검사기가 놓칩니다 — 그건 손으로 지웠습니다.
자동 검사가 모든 것을 대신하지는 않습니다.

### 6. 검사기 자신의 버그

`ast.walk` 은 **`lineno` 가 없는 `Module` 노드를 가장 먼저 냅니다.** 위치
문자열을 루프 첫 줄에서 계산했더니 문서 20개가 `AttributeError` 로 무더기
실패했습니다. 잠깐 "문서가 다 틀렸나" 싶었지만 전부 제 버그였습니다.
위치는 **실제로 쓸 때만** 계산하도록 고쳤습니다.

### 7. 파싱 안 되는 블록은 통과시킵니다

문서 코드블록에는 `...` 나 발췌가 섞입니다. `SyntaxError` 를 실패로 만들면
문서 쓰는 사람이 검사를 꺼 버립니다. 건너뜁니다 — 그만큼 못 잡습니다.

## 회귀 확인

**① 실제 문서에 결함을 되살렸습니다.**

```console
$ sed -i 's|VmKis(id=...)|VmKis(app_key="...", app_secret="...")|' docs/guidelines/API_STABILITY_POLICY.md
$ python -m pytest tests/unit/test_docs_signatures.py -q
docs/guidelines/API_STABILITY_POLICY.md:182 — VmKis(...) 에 `app_key=` 를 넘깁니다. ...
```

**② 알려진 결함 5종을 테스트 안에 박아 뒀습니다.**

`load_config` · `setLevel` · `app_key=` · `KisAuth(virtual=)` · `VmKis(paper=)`.
문서가 앞으로 어떻게 바뀌든 검사기 성능이 계속 검증됩니다.

**③ 검사기가 아무것도 못 보는 상태도 막았습니다.**

```python
assert len(files) >= 20
assert blocks >= 100          # 코드펜스 정규식이 죽으면 여기서 걸립니다
```

## 변경 파일

- `docs/guidelines/REGIONAL_GUIDES.md` — 설정 블록 2개, `VmKis` 호출, 허구 Mock 절, 비교표 2개
- `docs/guidelines/API_STABILITY_POLICY.md` · `docs/rules/TEST_RULES_AND_GUIDELINES.md`
- `docs/FAQ.md` — Q3 두 방법, Q18 import
- `docs/SIMPLEKIS_GUIDE.md` — 3절 재작성 (`load_kis_config`, 실제 대화형 화면)
- `docs/developer/DEVELOPER_GUIDE.md` — `KisQuote`, Mock 예제
- `CONTRIBUTING.md` — `vmkis.types` → `vmkis.public_types`
- `examples/tutorial_basic.ipynb`
- `tests/unit/test_docs_signatures.py` — 신규. 43건

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1105 passed, 24 skipped        # 이전 1050 + 신규 43 + #84 분

$ ruff check . && ruff format --check .
All checks passed! / 211 files already formatted
```

## 손대지 않은 것

`docs/generated/` 에 같은 결함이 9건 있습니다(`KisAuth(virtual=)` 등). INDEX 가
"자동 생성물"이라고 적고 있으므로 **손으로 고칠 대상이 아닙니다** — 재생성해야
합니다. 검사기의 제외 목록에 넣었고, 생성기가 아직 있는지는 확인하지
않았습니다. 없다면 그건 동결 문서이지 생성물이 아니므로 따로 정리할 일입니다.
