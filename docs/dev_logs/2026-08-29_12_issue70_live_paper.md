# 2026-08-29 - #70 real/virtual → live/paper 코드 개명 개발 일지

## 작업 내용

`src/` 17개 · `tests/` 35개 · `examples/` 8개 · 문서 10개에서 `real`/`virtual`
어휘를 `live`/`paper` 로 바꿨습니다. **별칭도 경고도 남기지 않았습니다.**

## 무엇에 걸렸는가

### 1. `tr_real`/`tr_virtual` — 이슈가 남겨 둔 결정

본문은 *"바꾸면 KIS 문서와 코드 사이에 번역층이 생긴다"*를 반대 논거로 적어
두었습니다. **그 논거가 성립하지 않습니다 — KIS 는 실전/모의라고 씁니다.**
`real`/`virtual` 은 이미 우리가 고른 번역입니다. 번역층은 새로 생기는 것이
아니라 이미 있었고, 이 이슈는 그 번역어를 바꾸는 일입니다.

결정적인 것은 **경계가 없다**는 점이었습니다. `tr_*` 는 도메인 리터럴과 같은
파일, 같은 함수에 있습니다.

```python
DOMAIN_TYPE = Literal["live", "paper"]          # 바뀜
def resolve(self, paper: bool):                 # 바뀜
    if paper and self.tr_virtual is not None:   # 안 바뀌면 여기서 읽는 사람이 멈춤
```

바꿨습니다. 근거를 이슈 본문에 적었습니다(완료 기준 2번).

### 2. 한글 조사가 단어 경계를 없앱니다

일괄 치환 후 `src/` 를 다시 훑었더니 3건이 남아 있었습니다.

```python
raise ValueError("virtual_auth에는 모의도메인 인증 정보를 입력해야 합니다.")
raise ValueError("virtual_id를 입력해야 합니다.")
raise ValueError("virtual_appkey를 입력해야 합니다.")
```

`re` 의 `\w` 는 **유니코드 문자를 단어 문자로 봅니다.** `에`·`를` 이 뒤에
붙으면 `\bvirtual_auth\b` 의 뒤쪽 경계가 성립하지 않아 치환이 건너뜁니다.

`tests/unit/test_kis.py:498` 이 그중 하나를 `pytest.raises(match=...)` 로
검사하고 있어서, **놓쳤다면 테스트가 잡아 줬을 것**입니다. 그러나 나머지 둘은
검사하는 테스트가 없었습니다. **치환 후에는 반드시 다시 grep 합니다.**

### 3. 영어 산문의 `real` — 마크다운에는 맨몸 규칙을 먹이지 않았습니다

`docs/user/en/` 은 영어입니다. `\breal\b` 를 일괄로 먹이면 *"No real money is
involved"* 같은 문장이 *"No live money"* 가 됩니다. 치환 규칙을 두 벌로 나눴습니다.

| 규칙 | 적용 대상 |
|---|---|
| 식별자 규칙 21개 (`tr_real`, `virtual_appkey`, `REAL_DOMAIN` …) | 코드 + 문서 |
| 맨몸 `\breal\b` / `\bvirtual\b` | **코드만** (`*.py`, `.env.sample`) |

문서는 남은 것을 눈으로 훑어 **코드 이름을 인용한 곳만** 고쳤습니다(완료 기준
6번의 문구가 정확히 이것입니다). 영어 산문의 "Real Trading" 제목 같은 것은
그대로 뒀습니다.

### 4. 오탐이 될 뻔한 것 — `real_metadata`

`tests/unit/utils/test_diagnosis.py` 의 `import importlib.metadata as
real_metadata` 는 **"가짜가 아닌 진짜"** 라는 뜻입니다. 실전/모의와 무관합니다.

**우연히 살았습니다.** `\breal\b` 는 `real_metadata` 에 걸리지 않습니다 —
뒤의 `_` 가 단어 문자라 경계가 성립하지 않기 때문입니다. 의도한 방어가 아니라
정규식의 부수효과였고, 이 파일은 실제로 한 줄도 바뀌지 않았습니다. 이름이
`real metadata` 나 `realMetadata` 였다면 조용히 바뀌었을 것입니다.

같은 이유로 `"realtok"`, `"real_token"`, `"real_user"`, `"real_id"` 같은
**불투명한 테스트 픽스처 값**도 그대로 뒀습니다. 판정 기준을 이렇게 세웠습니다 —
**이름(식별자·인자·속성·문서가 인용한 API 이름)은 바꾸고, 값(임의의 문자열
데이터)은 두지 않습니다.**

### 5. `helpers` 의 번역표가 예고대로 사라졌습니다

#75 가 남겨 둔 것입니다.

```python
#: #70 이 코드 쪽을 live/paper 로 개명하면 이 표는 사라집니다.
_MODE_TO_DOMAIN = {"live": "real", "paper": "virtual"}
```

치환 후 `{"live": "live", "paper": "paper"}` — 항등 사상이 됐습니다. `_MODE_TO_DOMAIN`
과 `_to_endpoints()` 를 지우고 호출부를 `dict(config.endpoints or {})` 로 바꿨습니다.
키 검증은 `config._parse_endpoints` 가 `MODES` 로 이미 하고 있습니다.
`Endpoint`·`KisConfig` import 가 미사용이 되어 함께 정리했습니다.

### 6. import 정렬이 세 번째로 걸렸습니다

`__env__` 의 상수 이름이 바뀌자 `kis.py` 의 import 블록 정렬이 깨졌습니다
(`LIVE_*` 가 `USER_AGENT` 앞으로, `PAPER_*` 가 뒤로). `ruff check --fix` 로
끝났습니다 — #73·#72 와 달리 주석이 딸려 있지 않아 손댈 것이 없었습니다.

## 검증

개명이 실제로 먹었는지, 그리고 **옛 이름이 정말 사라졌는지**를 확인했습니다.

```console
$ python -c "..."
LIVE_DOMAIN     : https://openapi.koreainvestment.com:9443
PAPER_DOMAIN    : https://openapivts.koreainvestment.com:29443
KisAuth 필드     : ['id', 'appkey', 'secretkey', 'account', 'paper']
VmKis.paper 존재 : True
VmKis.virtual 존재: False           ← 별칭 없음
resolve(paper=True) : ('VTTC8434R', 'paper')
resolve(paper=False): ('TTTC8434R', 'live')
KisAuth(virtual=) -> TypeError — unexpected keyword argument 'virtual'
```

**통과만 보면 안 됩니다.** 테스트를 같은 스크립트로 함께 개명했으므로, 테스트가
전부 통과하는 것은 "개명이 일관됐다"는 뜻이지 "개명이 됐다"는 뜻이 아닙니다.
위 스모크가 그 구멍을 막습니다.

```console
$ python -m pytest tests/unit tests/integration -q
1062 passed, 24 skipped

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 210 files already formatted / Contracts: 2 kept, 0 broken.

$ python -m compileall -q examples/
OK
```

## 변경 파일

치환 스크립트가 60개 파일 635줄을 바꿨고, 그 뒤 손으로 고친 것이 아래입니다.

- `src/vmkis/kis.py` - 한글 조사 뒤 식별자 3건
- `src/vmkis/helpers.py` - `_MODE_TO_DOMAIN` / `_to_endpoints` 제거
- `tests/` 4개 - 지역 변수·속성·docstring (`paper_vmkis`, `live_limiter` 등)
- 문서 10개 - 코드 이름 인용부
- `docs/user/USER_GUIDE.md` - 아래 참고
- `CHANGELOG.md` - 마이그레이션 표 2개

## 범위 밖에서 발견한 것

### `docs/user/USER_GUIDE.md` 의 모의투자 절 — 고쳤습니다

```python
kis.virtual = True  # 또는 kis.virtual_account()
```

`virtual` 은 **읽기 전용 프로퍼티**였고 `virtual_account()` 는 없습니다. 즉 이
스니펫은 원래부터 `AttributeError` 입니다. 이름만 바꾸면 **버그를 세탁**하게
되므로, 실제 동작(인증 둘을 넘기면 모의 클라이언트가 되고 전환은 불가)을 적었습니다.

### 예제 7개가 `create_client(..., profile=)` 를 호출합니다 — 별도 이슈

`create_client` 의 인자는 `account` 입니다. `profile` 은 없습니다. #75 가
`01_basic/` 3개만 고치고 나머지를 놓쳤습니다. 지금 실행하면 `TypeError` 입니다.
**이 PR 에서 고치지 않았습니다** — 원인이 다른 결함을 큰 개명 PR 에 섞으면
되돌릴 때 갈라내지 못합니다. 새 이슈로 올렸습니다.

### `docs/SIMPLEKIS_GUIDE.md` · `examples/tutorial_basic.ipynb` — #78 로

`load_config` 출력, `save_config_interactive` 프롬프트 문구,
`VmKis(..., virtual=True)`(그런 인자가 없습니다) 가 전부 낡았습니다. 이름만
바꾸면 역시 세탁이 되므로 그대로 두고 #78 에 넘겼습니다.

## 남은 완료 기준 — `0.1.0` 릴리스

이슈의 완료 기준에 `0.1.0` 릴리스가 있습니다. 이 저장소의 버전은 **git 태그**에서
만들어지므로(`docs/developer/VERSIONING.md`), 태그를 다는 것은 코드 변경이 아니라
**배포 행위**입니다. 이 PR 에서는 하지 않았습니다. CHANGELOG 는 준비돼 있습니다.
