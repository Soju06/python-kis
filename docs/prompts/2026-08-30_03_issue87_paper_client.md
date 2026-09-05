# 2026-08-30 - #87 create_client 가 모의 계좌에서 항상 실패하는 문제

## 사용자 요청

> #87 착수

(#21 PR #90 머지 후. #85 `0.1.0` 이 이 이슈 하나에 막혀 있습니다.)

## 분석

### 방향 셋 중 무엇을 고를 것인가 — 사실이 정합니다

이슈 본문이 남긴 선택지입니다.

1. `auth=None` 이면 `paper_auth` 의 자격증명으로 폴백 — **모의 전용 클라이언트 인정**
2. `create_client` 가 모의 계좌에도 실전 인증을 함께 넘기도록
3. `VmKis(None, paper_auth)` 를 명시적으로 금지

**엔드포인트 21개를 세어 보니 답이 정해졌습니다.**

```text
tr_paper 가 없는 엔드포인트 : 13 / 21
  DOMESTIC_QUOTE · FOREIGN_QUOTE · PRODUCT_INFO
  DOMESTIC_DAILY_CHART · FOREIGN_DAILY_CHART · DOMESTIC_DAY_CHART · FOREIGN_DAY_CHART
  ...
```

`client/endpoint.py` 가 그 성질을 문서화하고 있습니다.

> `None` 이면 **모의투자를 지원하지 않는 TR** 입니다. 이때 모의 계좌로
> 호출해도 실전 도메인으로 보냅니다(시세 조회 등이 이 경우입니다).

즉 **모의 클라이언트도 실전 앱키와 실전 토큰이 필요합니다.** 1번은
`kis.stock().quote()` 에서 죽는 클라이언트를 만들어 냅니다 — 생성은 되고 나중에
터지는, #73 에서 없앤 바로 그 실패 모드입니다.

→ **2 + 3 을 함께 합니다.**

### 이 버그가 8개월 산 이유 — 테스트가 박제하고 있었습니다

```python
class DummyVmKis:
    def __init__(self, *args, **kwargs):
        calls.append((args, kwargs))

monkeypatch.setattr(helpers, "VmKis", DummyVmKis)
...
assert args[0] is None          # ← 실제 생성자가 거부하는 바로 그 형태
```

호출 **형태**를 검사하느라 생성자를 통째로 대역으로 바꿨고, 그 대역은 무엇이든
받았습니다. **테스트는 초록이고 사용자는 `ValueError` 를 받았습니다.**

### 유래

`VmKis(None, auth)` 는 `06a63f2`(python-kis → vmkis 개명)에서 들어왔습니다.
**이 저장소에서 동작한 적이 없습니다.**

## 계획

1. `VmKis.__init__` — `auth=None, paper_auth=주어짐` 을 **원인을 말하는 예외**로
2. `helpers.create_client` — 설정에서 실전 계좌를 찾아 함께 넘김. 없으면
   **무엇을 추가해야 하는지** 말하고 멈춤
3. `configs/template_account_profiles.yaml` — 실전 앱 주석 해제. **템플릿
   기본값으로 정규 경로가 끝까지 가야 합니다**
4. 테스트 — 모킹하지 않고 **진짜 생성자를 타는** 것을 추가
5. 문서 — `CONFIG_SCHEMA`(R10) · `QUICKSTART` · `FAQ`

## 결과

방향 2+3 채택. 템플릿·문서까지 정리. 상세는
[docs/dev_logs/2026-08-30_03_issue87_paper_client.md](../dev_logs/2026-08-30_03_issue87_paper_client.md).
