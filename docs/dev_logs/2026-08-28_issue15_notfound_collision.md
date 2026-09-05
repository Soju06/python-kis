# 2026-08-28 - Issue #15 `KisNotFoundError` 이름 충돌 개발 일지

**대상 이슈**: [#15](https://github.com/visualmoney/vm-stock-kis/issues/15)

---

## 요약

```text
975 passed, 7 skipped (게이팅) — 회귀 테스트 9개 추가
TOTAL 90.78%
```

**이슈가 서술한 것보다 심각했습니다.** "어느 것을 import 했는지에 따라 다르게
동작한다"가 아니라, **공개 API 를 따른 사용자의 핸들러가 절대 실행되지
않았습니다.**

---

## 착수 전 조사 — 이슈가 요구한 사용 빈도

이슈는 "어느 쪽을 개명할지는 사용 빈도 조사 후 결정"하라고 했습니다. 재보니
**한쪽은 완전히 죽어 있었습니다.**

| | `responses` 쪽 (조회 결과 없음) | `client` 쪽 (HTTP 404) |
|---|---|---|
| `raise` 되는 곳 | `responses/response.py:41` | **0곳** |
| import 하는 곳 | src 2 + tests 3 | **0곳** |
| docstring 언급 | 약 50곳 (`조회 결과가 없는 경우`) | 0곳 |
| `except` 로 잡는 곳 | `api/stock/trading_hours.py:205` | 0곳 |

### 그런데 공개 모듈은 죽은 쪽을 내보내고 있었습니다

```console
$ uv run python -c "..."
  vmkis.exceptions.KisNotFoundError 는: vmkis.client.exceptions
  실제로 raise 되는 것    : vmkis.responses.exceptions
  둘이 같은가             : False
```

`vmkis/exceptions.py` 가 `client.exceptions` 에서 통째로 import 하면서
`KisNotFoundError` 도 딸려 왔습니다.

```python
from vmkis.exceptions import KisNotFoundError

try:
    kis.stock("005930").quote()
except KisNotFoundError:      # ← 절대 잡히지 않음
    ...
```

약 50개 docstring 이 `Raises: KisNotFoundError: 조회 결과가 없는 경우` 라고
안내하는데, 사용자가 공개 모듈에서 그 이름을 가져오면 **다른 클래스**를
잡게 됩니다.

---

## 결정 — 이슈의 제안과 반대 방향

이슈는 "**조회 결과 없음 쪽**을 `KisResultNotFoundError` 등으로 개명"을
제안했습니다. **죽은 쪽(HTTP 404)을 개명하는 것으로 뒤집었습니다.**

| | 이슈 제안 | 채택 |
|---|---|---|
| 개명 대상 | `responses` (살아 있는 쪽) | **`client` (죽은 쪽)** |
| docstring 수정 | 약 50곳 | **0곳** |
| 공개 모듈 | 여전히 안 잡히는 쪽을 노출 | **실제 발생하는 쪽** |
| 사용자 코드 영향 | 잡던 이름이 바뀜 | **안 잡히던 게 잡히기 시작** |

`client` 쪽은 `raise` 0회 / import 0곳이므로 개명해도 깨질 코드가 없습니다.
그리고 `KisNotFoundError` 라는 이름은 **실제로 그 상황에서 발생하는 예외**가
가져가는 것이 맞습니다.

### 조치

1. `client.exceptions.KisNotFoundError` → **`KisHTTPNotFoundError`**
2. `vmkis/exceptions.py` 가 `KisNotFoundError` 를 **`responses` 에서** 가져오도록
3. `KisHTTPNotFoundError` 도 공개 모듈에 함께 노출 (둘 다 잡을 수 있게)
4. 옛 경로(`vmkis.client.exceptions.KisNotFoundError`)는 PEP 562 모듈 `__getattr__`
   로 `DeprecationWarning` 과 함께 유지. 1.0.0에서 제거
5. 두 클래스의 docstring 에 **차이를 표로** 명시

### 별칭을 `__all__` 에 넣지 않았습니다

`from vmkis.client.exceptions import *` 가 옛 이름을 계속 퍼뜨리기 때문입니다.
`PyKis` → `VmKis` 별칭 때와 같은 판단입니다.

---

## 회귀 테스트

`tests/unit/test_notfound_collision.py` 신규 9개.

| 테스트 | 검증 |
|---|---|
| `test_public_notfound_is_the_one_actually_raised` | **이 버그의 핵심.** 공개 이름이 실제 발생 클래스인가 |
| `test_public_notfound_is_not_the_http_one` | 반대쪽이 아닌가 |
| `test_neither_catches_the_other` | 상속 계층이 달라 서로 못 잡음 — 원래 버그의 본질 |
| `test_old_client_path_still_works_with_warning` | 옛 경로 + 경고 |
| `test_alias_is_not_in_all` | `import *` 오염 방지 |

---

## 변경 파일

- `src/vmkis/client/exceptions.py` — 개명, 차이 문서화, deprecated 별칭
- `src/vmkis/exceptions.py` — 공개 재export 를 실제 발생 클래스로
- `tests/unit/test_notfound_collision.py` — 신규
- `tests/unit/test_exceptions.py` — 옛 별칭 사용을 새 이름으로
- `CHANGELOG.md` — `[미출시]` 절 신설 (0.0.1 은 이미 배포됨)

## 다음 할 일

- [ ] `MIGRATION_GUIDE.md` 에 이 변경을 넣을지 판단.
      0.0.1 사용자가 사실상 없어 지금은 CHANGELOG 로 충분해 보인다
- [ ] `docs/user/EXTENDING_API.md` 의 함정 목록에 "두 `NotFound` 의 차이"를
      추가할지 검토
- [ ] `KisHTTPNotFoundError` 는 여전히 **아무도 발생시키지 않는다.**
      `kis.py` 가 HTTP 상태 코드별로 예외를 세분화하지 않고 `KisHTTPError` 만
      던지기 때문. 401/403/404/429/5xx 를 실제로 구분해 던질지는 별건
