# 2026-08-29 - #70 real/virtual → live/paper 코드 개명

## 사용자 요청

> 머지하고 #70 착수해줘

(#72 PR #82 스쿼시 머지 후 이어서 착수)

## 분석

### 실측 — 본문의 369건을 다시 셌습니다

```console
$ grep -rnoE '\b(real|virtual)[a-z_]*' src/ | ...
   96 virtual          41 real            22 virtual_appkey
   16 virtual_auth     14 virtual_token   10 virtual_id
    9 virtual_secretkey 6 virtual_token_path
    4 real_auth         3 virtual_not_supported
    1 realtime          ← 건드리지 않습니다

$ grep -rno 'tr_real\|tr_virtual' src/ | wc -l
118

$ grep -rnoE '\b[A-Z_]*(REAL|VIRTUAL)[A-Z_]*\b' src/
   3 REAL_DOMAIN  3 VIRTUAL_DOMAIN
   3 REAL_API_REQUEST_PER_SECOND  3 VIRTUAL_API_REQUEST_PER_SECOND
```

여기에 `tests/` 35개 파일이 붙습니다. `src/` 17개 + `tests/` 35개.

### 결정 1 — `tr_real`/`tr_virtual` 도 바꿉니다 (118건)

본문이 "착수 시 정하고 근거를 본문에 적는다"고 남겨 둔 항목입니다.

**바꿉니다.** 반대 논거였던 "KIS 문서와 코드 사이에 번역층이 생긴다"가
성립하지 않습니다 — **KIS 는 실전/모의라고 씁니다.** `real`/`virtual` 은 이미
우리가 고른 번역입니다(#55 의 결론이 정확히 이것입니다). 번역층은 새로 생기는
것이 아니라 이미 있고, 이 이슈는 그 번역어를 바꾸는 것입니다.

바꾸지 않으면 **우리 코드 안에 어휘가 두 벌** 생깁니다. `client/endpoint.py`
한 파일에서 이렇게 됩니다.

```python
DOMAIN_TYPE = Literal["live", "paper"]      # 바뀜

def resolve(self, paper: bool):             # 바뀜
    if paper and self.tr_virtual is not None:   # 안 바뀜 ← 읽는 사람이 멈춤
        domain = "paper"
```

`tr_real`/`tr_virtual` 은 `DOMAIN_TYPE` 과 **같은 파일, 같은 함수**에 있습니다.
따로 둘 수 있는 경계가 아닙니다.

### 결정 2 — 테스트 환경변수 `VMKIS_VIRTUAL_*` 도 바꿉니다

`src/` 는 이 이름들을 모릅니다. `tests/env.py` 와 `tests/.env.sample` 에만
있습니다. 그래도 바꾸는 이유는, 기여자가 **가장 먼저 만나는 자리**에 옛 어휘를
남기면 어휘가 두 벌이 되는 것은 마찬가지이기 때문입니다.

**기존 `.env` 를 가진 사람은 키 이름을 바꿔야 합니다.** 조용히 깨지지는
않습니다 — `require_credentials` 가 누락된 이름을 그대로 찍습니다.

```text
누락: VMKIS_PAPER_ACCOUNT_NUMBER, ... — 저장소 루트에 .env 를 만들어 채우세요.
```

### 손대지 않는 것

| | 왜 |
|---|---|
| `realtime` / `KisRealtimePrice` (1건) | 다른 개념. 본문도 근거에서 뺐습니다 |
| 한국어 "실전"/"모의" | KIS 의 표기입니다. 우리가 고른 번역만 바꿉니다 |
| `configs/*.yaml`, `_MODE_KEY` 값 | #75 범위 |
| `docs/dev_logs/`, `docs/prompts/`, `docs/reports/`, `archive/` | 동결 문서 |

### 영어 산문에서의 `real` 위험

`docs/user/en/` 은 영어입니다. `\breal\b` 를 일괄 치환하면 *"real money"*
같은 산문까지 바뀝니다. **마크다운에는 식별자 규칙만 적용하고 산문은 눈으로
봅니다.**

## 계획

1. 식별자 치환 규칙을 순서 있는 표로 정의 (긴 것부터)
2. `src/` · `tests/` · `examples/*.py` 에 전체 규칙 적용
3. 마크다운에는 식별자 규칙만 적용 후 산문 육안 검토
4. 테스트 + `import vmkis` 확인
5. CHANGELOG 마이그레이션 표
6. 이슈 본문에 `tr_*` 결정 기록

## 결과

`src/` 17 · `tests/` 35 · `examples/` 8 · 문서 10개 개명. 별칭 없음.
상세는 [docs/dev_logs/2026-08-29_12_issue70_live_paper.md](../dev_logs/2026-08-29_12_issue70_live_paper.md).
