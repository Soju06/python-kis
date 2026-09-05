# 2026-08-29 - #75 설정 계층 구현 개발 일지

## 작업 내용

3블록 설정 스키마(`apps` / `accounts` / `default_account`)를 구현했습니다.
`src/vmkis/config.py` 를 새로 만들고 규칙 R1~R9 을 넣었으며, `load_config` 와
`_validate_profile`(#69)을 **삭제**했습니다. 하위 호환은 넣지 않았습니다.

## 걸린 것

### 1. `.gitignore` 로 디렉터리를 제외하면 그 안의 예외가 통하지 않습니다

템플릿을 `configs/` 안에 둘지 저장소 루트에 둘지가 문제였는데, 안에 두려면
`.gitignore` 를 어떻게 쓰느냐가 먼저 걸렸습니다.

```console
=== 'configs/' + !configs/template... ===
  (템플릿이 무시됨)
=== 'configs/*' + !configs/template... ===
  ?? configs/template_account_profiles.yaml     ← 추적됨
```

**git 은 제외된 디렉터리로 아예 내려가지 않습니다.** `configs/` 가 아니라
`configs/*` 여야 `!` 예외가 삽니다. 실측하지 않았으면 "예외를 썼는데 왜 안
잡히지"로 한참 헤맸을 것입니다.

### 2. 템플릿 위치가 토큰 안전성을 바꿉니다

처음에는 템플릿을 저장소 루트에 뒀습니다. 사용자가 지적해 다시 보니, 토큰 폴더가
**설정 파일 기준**이라 루트에 둔 템플릿을 제자리에서 채우면 토큰이 저장소
루트(`./token/`)에 떨어집니다. 그건 `.gitignore` 에 없습니다.

`configs/` 안에 두면 토큰이 `configs/token/` 으로 가고 자동으로 무시됩니다.
덤으로 첫 클론에 `configs/` 가 이미 있어 `mkdir` 이 필요 없습니다.

**위치 선택이 스타일 문제인 줄 알았는데 시크릿 유출 경로였습니다.**

### 3. 사용자 초안의 `token_path` 를 파생으로 바꿨습니다

초안은 앱마다 경로를 적게 하고 *"⚠️ 앱키별로 다르게 지정해야 한다"* 고
경고했습니다. **사용자가 지켜야 하는 불변식은 사용자가 안 지킵니다.** 두 앱이 같은
파일을 가리켜도 아무도 못 막고, 증상은 "가끔 인증이 풀린다"로 나타나 원인 추적이
어렵습니다. `token/<app>.json` 으로 파생시켜 충돌을 구조적으로 불가능하게 했습니다.

### 4. 영문 문서가 **한 번도 맞은 적이 없는** API 를 적고 있었습니다

`load_config` 참조를 고치러 갔다가 발견했습니다.

```python
docs/user/en/README.md
config = load_config("config.yaml")
kis = VmKis(**config['kis'])          # load_config 가 {'kis': ...} 를 준 적이 없습니다
```

```python
kis = VmKis(app_key=..., app_secret=..., account_number=..., server=...)
# 네 인자 모두 존재하지 않습니다. 실제로는 appkey / secretkey / account 입니다
```

**예제가 한 번도 실행된 적이 없다는 뜻입니다.** 설정에 직결된 곳(`en/README`,
`en/QUICKSTART`, `en/FAQ`)은 이번에 정정했고, 설정과 무관한 문맥
(`REGIONAL_GUIDES`, `API_STABILITY_POLICY`)은
[#78](https://github.com/visualmoney/vm-stock-kis/issues/78) 로 남겼습니다.
그 이슈의 완료 기준에 **"문서 예제가 실제로 import 되는지 검사하는 방법"** 을
넣었습니다 — 검사가 없으면 같은 일이 반복됩니다.

### 5. 테스트 대역이 새 계약을 따라야 했습니다

`websocket.py` 가 주소를 상수에서 직접 읽던 것을 `self.kis.ws_url(...)` 로 바꾸자
`DummyKis` 가 깨졌습니다.

```text
ERROR: RTC Unexpected error: 'DummyKis' object has no attribute 'ws_url'
```

설정으로 주소를 재정의할 수 있으려면 상수를 직접 읽어서는 안 되고 클라이언트를
거쳐야 합니다. 대역도 그 계약을 따라야 하므로 `ws_url` 을 추가하고 **왜** 추가하는지
주석에 남겼습니다.

### 6. `@overload` 5개 + 실구현 1개

`VmKis.__init__` 이 그런 구조라 인자 2개(`user_agent`, `endpoints`) 추가가
시그니처 6곳을 건드립니다. #70 이 곧 같은 시그니처를 다시 쓸 예정이라 미루고 싶었지만,
**파싱만 하고 안 읽는 키를 내보내는 것**은 CONFIG_SCHEMA.md 가 스스로 금지한
것이라 배선까지 했습니다. 6곳이 모두 `use_websocket` 으로 끝나 삽입 지점은
균일했습니다.

## 되돌려 확인

R2·R6·R9 를 무력화했습니다.

```console
$ uv run pytest tests/unit/test_config.py -q
7 failed, 17 passed
```

그 상태에서 실제로 무슨 값이 들어가는지 찍었습니다.

```console
설정 파일이 적은 것 : account_no: 00000000 / product_code: 01  (따옴표 없음)
실제로 들어간 값    : account_no=0 (int), product_code=1 (int)
KisAuth 가 받을 계좌: '0-1'

=> 계좌번호가 사라졌습니다. 경고 한 줄 없습니다.
```

이것이 R9 이 존재하는 이유입니다 — 사용자의 오타가 아니라 **YAML 의 함정**이라,
오류 메시지가 "따옴표를 씌우세요"라고 말해야 합니다.

복원 후 `grep -c DEFECT-REVIVAL` 이 0인 것과 전체 통과를 확인했습니다.

## 변경 파일

- `src/vmkis/config.py` - **신설.** 3블록 파싱, R1~R9, 토큰/엔드포인트 해석
- `src/vmkis/helpers.py` - `create_client` 를 새 계층 위로. `load_config` 삭제.
  설정을 `KisAuth` 로 번역하는 것만 남김
- `src/vmkis/kis.py` - `user_agent`/`endpoints` 인자(시그니처 6곳),
  `base_url()`/`ws_url()` 해석기, 세션 UA 배선
- `src/vmkis/client/websocket.py` - 상수 직접 참조 → `self.kis.ws_url(...)`
- `src/vmkis/__init__.py` - `load_config` 공개 해제
- `configs/template_account_profiles.yaml` - 신설. `config.example*.yaml` 3개 삭제
- `.gitignore` - `configs/*` + 템플릿 예외
- `examples/01_basic/*.py` 4개 - `create_client` 한 줄로
- `tests/unit/test_config.py` - 신설 (R1~R9 + 모양 검사)
- `tests/unit/test_config_examples.py` - 템플릿 검증으로 전환
- `tests/unit/test_helpers.py` - 번역만 검사하도록 축소
- `tests/unit/test_compat_aliases.py` - 폴백 대상이 `PROFILE` → `ACCOUNT`
- `tests/unit/client/test_websocket.py` - `DummyKis.ws_url`
- 문서: `QUICKSTART.md`, `CONTRIBUTING.md`, `examples/README.md`,
  `examples/01_basic/README.md`, `docs/user/en/{README,QUICKSTART,FAQ}.md`

## 테스트 결과

```console
uv run pytest -m 'not requires_api'    1088 passed, 8 skipped, 17 deselected
coverage                               91.79%  (게이트 90)
config.py                              리포트에 없음 = 100% (skip_covered = true)
ruff check / format                    통과
lint-imports --no-cache                2 kept, 0 broken
```

`config.py` 를 100% 로 올린 것은 마지막에 **"매핑이 아니다" 거부 경로 8줄**이 안
덮여 있는 것을 보고 채운 결과입니다. 이 모듈의 본업이 거부인데 거부 분기가
검사되지 않는 것은 앞뒤가 맞지 않습니다.

## 다음 할 일

- [ ] #70 코드 개명 — `_MODE_TO_DOMAIN` 번역표(`helpers.py`)가 그때 사라집니다
- [ ] #78 문서의 가짜 시그니처 정리
- [ ] #72 python-dotenv, #73 조용한 `None` 폴백
