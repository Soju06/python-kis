# 2026-08-30 - #87 create_client 가 모의 계좌에서 항상 실패하던 문제 개발 일지

## 작업 내용

`create_client` 가 모의 계좌에 실전 인증을 함께 넘기도록 고치고, 생성자의
오해를 부르는 예외 메시지를 바꿨으며, 템플릿과 문서를 새 규칙에 맞췄습니다.

## 무엇에 걸렸는가

### 1. 방향은 세는 순간 정해졌습니다

이슈가 선택지 셋을 남겼는데, `KisEndpoint` 21개를 세니 답이 하나였습니다.

```text
tr_paper 가 없는 엔드포인트 : 13 / 21   ← 모의 계좌도 실전 도메인으로 갑니다
```

`client/endpoint.py` 가 이미 그렇게 적어 두었습니다.

> `None` 이면 **모의투자를 지원하지 않는 TR** 입니다. 이때 모의 계좌로
> 호출해도 실전 도메인으로 보냅니다(시세 조회 등이 이 경우입니다).

**모의 클라이언트도 실전 앱키와 실전 토큰이 필요합니다.** 그래서 1번 방향
("모의 전용 클라이언트를 인정")은 **`kis.stock().quote()` 에서 죽는 클라이언트**를
만들어 냅니다 — 생성은 되고 나중에 터지는, 어제 #73 에서 없앤 바로 그 실패
모드입니다. 고르지 않았습니다.

### 2. 테스트가 버그를 박제하고 있었습니다 — 이 세션 세 번째

```python
class DummyVmKis:
    def __init__(self, *args, **kwargs):
        calls.append((args, kwargs))

monkeypatch.setattr(helpers, "VmKis", DummyVmKis)
...
assert args[0] is None          # ← 진짜 생성자가 거부하는 바로 그 형태
```

호출 **형태**를 보려고 생성자를 통째로 대역으로 바꿨는데, 그 대역은 무엇이든
받습니다. **테스트는 초록이고 사용자는 `ValueError` 를 받았습니다.**

`test_real_vmkis_is_actually_constructed` 를 추가했습니다 — 모킹 없이 끝까지
만듭니다. 자격증명은 **형식만** 맞으면 되고 네트워크는 타지 않습니다(토큰
발급이 지연되기 때문입니다).

> 이 세션에서 같은 종류를 세 번 만났습니다.
> `#84` CI 가 스모크를 skip · `#78` 검사기가 아무것도 안 봄 ·
> 여기 대역이 생성자를 가림. **"통과"는 "검사했다"가 아닙니다.**

### 3. `id를 입력해야 합니다` 가 원인을 가렸습니다

```python
if id is None:
    raise ValueError("id를 입력해야 합니다.")
```

사용자는 **id 를 빠뜨린 적이 없습니다.** 모의 인증을 통째로 넘겼고 그 안에
id 가 있습니다. 이 메시지로는 원인에 닿을 수 없습니다.

앞에 전용 검사를 넣어 **왜 실전 인증이 필요한지까지** 말하게 했습니다.

```text
모의 인증만으로는 클라이언트를 만들 수 없습니다. 실전 인증을 첫 번째 인자로
함께 주세요 — VmKis(live_auth, paper_auth). 시세 TR 은 모의도메인에 없어서
모의 계좌도 실전 도메인으로 나가고, 그때 실전 앱키와 실전 토큰이 필요합니다.
```

### 4. 유래 — 동작한 적이 없습니다

`git log -S 'VmKis(None, auth'` 로 추적했습니다. `06a63f2`(python-kis → vmkis
개명)에서 그대로 들어왔습니다. **이 저장소에서 한 번도 동작하지 않았습니다.**
`#74`·`#79` 가 그 줄 주변을 두 번 고쳤지만 형태는 그대로 옮겼습니다.

### 5. 템플릿을 고치지 않으면 이슈가 안 닫힙니다

이슈 제목이 *"템플릿 기본값이 그것입니다"* 입니다. 코드만 고치면 `cp 템플릿`
→ 채우기 → `create_client()` 는 여전히 막힙니다 — 이번엔 친절한 메시지로.

템플릿의 실전 앱 주석을 풀고 **왜 필요한지**를 그 자리에 적었습니다. 채워 넣은
템플릿으로 `create_client()` 가 끝까지 가는 것을 확인했습니다.

### 6. `test_template_defaults_to_paper` 를 다시 써야 했습니다

```python
active = [l for l in text.splitlines() if l.strip().startswith("mode:")]
assert active == ['    mode: "paper" # live | paper — 생략할 수 없습니다']
```

템플릿에 앱이 둘이 되면서 깨졌습니다. 그런데 **이 테스트가 지키려던 성질은
"mode 가 paper 하나뿐"이 아니라 "실수로 실전에 붙지 않는다"** 입니다. 문자열
비교를 그 성질로 바꿨습니다.

```python
config = load_kis_config(TEMPLATE)
assert config.account().is_paper
```

**문자열을 비교하는 테스트는 의도가 아니라 표기를 지킵니다.**

## 회귀 확인 — 결함을 되살렸습니다

```console
$ # helpers.py 를 `return VmKis(None, auth, **shared)` 로 되돌림
$ python -m pytest tests/unit/test_helpers.py ... -q
FAILED ...::test_paper_account_passed_as_second_auth
FAILED ...::test_paper_only_config_says_what_to_add
FAILED ...::test_real_vmkis_is_actually_constructed
3 failed, 31 passed
```

세 건이 각각 다른 것을 봅니다 — 호출 형태 · 안내 메시지 · **진짜 생성**.
셋째가 없었다면 #87 이 또 통과했을 것입니다.

## 남긴 결정

### 실전 계좌가 여럿이면 이름순 첫 번째

```python
return _to_auth(sorted(live, key=lambda a: a.name)[0])
```

실전 계좌 **선택**을 위한 설정 키는 만들지 않았습니다. 필요해진 다음에 만드는
편이 낫습니다 — 지금 만들면 아무도 안 쓰는 키가 하나 늡니다.

### 확인하지 못한 것 — 모의 앱키가 실전 도메인에서 통하는가

만약 통한다면 실전 앱 없이도 모의 클라이언트를 만들 수 있고, 이 이슈의 1번
방향이 살아납니다. **실계좌 자격증명이 있어야 확인할 수 있습니다.** 이슈에
남겼습니다.

## 변경 파일

- `src/vmkis/kis.py` — 모의 인증 단독 사용을 원인이 보이는 예외로
- `src/vmkis/helpers.py` — `_live_auth_for()` 추가, `create_client` 가 실전 인증을 함께 전달
- `configs/template_account_profiles.yaml` — 실전 앱/계좌 활성화 + 근거
- `tests/unit/test_helpers.py` — 실생성자 테스트 + 안내 메시지 테스트. 픽스처에 실전 앱
- `tests/unit/test_config_examples.py` · `test_compat_aliases.py` · `test_simple_helpers.py`
- `docs/guidelines/CONFIG_SCHEMA.md` (R10) · `QUICKSTART.md` · `docs/FAQ.md`

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1158 passed, 24 skipped

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 223 files already formatted / Contracts: 2 kept, 0 broken.
```

> `tests/integration/test_rate_limit_compliance.py::test_rate_limit_burst_then_throttle`
> 이 한 번 실패했다가 재실행 2회 통과했습니다. 타이밍 플레이크이고 이 변경과
> 무관합니다(#59 의 `SCHEDULING_SLACK` 계열). 재발하면 별도 이슈로 다룰 일입니다.
