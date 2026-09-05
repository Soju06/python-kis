# 2026-08-30 - #21 codegen 파일럿 개발 일지

## 작업 내용

잃어버린 AST 파서를 되살려 커밋하고, 이슈의 수치를 다시 쟀으며, 엔드포인트 8개를
생성해 검사 테스트까지 붙였습니다. **생성물은 아직 패키지에 넣지 않았습니다.**

## 무엇에 걸렸는가

### 1. 이 이슈의 근거가 저장소에 없었습니다

이슈는 "AST 파서 400줄은 프로토타입 완성 상태"라며 파싱률 98.9% 등을 근거로
삼는데, **그 파서가 커밋된 적이 없습니다.**

```console
$ ls scripts/
generate_api_reference.py
```

중단 조건이 *"파싱률이 급락하면"* 인데 **잴 도구가 없었습니다.** 첫 작업이
파서를 다시 만드는 것이 된 이유입니다. 이제 `scripts/extract_kis_specs.py` 가
있고 누구나 다시 잴 수 있습니다.

> **교훈**: 수치를 근거로 이슈를 쓸 때는 **그 수치를 낸 도구를 함께 커밋**해야
> 합니다. 안 그러면 근거가 아니라 주장입니다.

### 2. "실패 3건"이 아니라 "웹소켓 60건"이었습니다

파서를 처음 돌리자 파싱률이 **81.9%** 로 나왔습니다. 실패 60건이 전부
`API_URL 없음` 이었습니다.

열어 보니 실패가 아니었습니다.

```python
def ccnl_krx(tr_type: str, tr_key: str, env_dv: str = "real") -> tuple[dict, list[str]]:
    """국내주식 실시간체결가 (KRX)[H0STCNT0] 구독 함수"""
```

**웹소켓 구독 함수는 `API_URL` 이 없는 것이 정상입니다.** 분류를 넣자
**REST 272개 중 272개 = 100%** 가 됐습니다.

이슈가 "REST 274개, 실패 3건"이라고 적은 것은 (1) auth 2개를 REST 로 세고
(2) 웹소켓 60개를 애초에 세지 않은 결과로 보입니다. **웹소켓을 실패로 세든
빼든, 그 60개가 어디로 갔는지 이슈 본문만으로는 알 수 없었습니다.**

### 3. 이름이 유일하지 않습니다 — 이슈에 없던 사실

가장 어려운 케이스로 지목된 `inquire_daily_ccld` 를 생성했더니 **해외선물**
엔드포인트가 나왔습니다. 이슈가 말한 것은 국내주식입니다.

```text
inquire_daily_ccld  ['domestic_bond', 'domestic_stock', 'overseas_futureoption']
inquire_price       ['domestic_bond', 'domestic_futureoption', 'domestic_stock', 'etfetn', 'overseas_futureoption']
order_rvsecncl      [5곳]
```

**332개 중 30종이 이름 충돌**입니다. 이름으로 키를 잡는 도구는 **9%를 조용히
잃습니다.** 제 생성기가 정확히 그랬고, 파일 하나를 눈으로 열어 보고서야
알았습니다.

`category/name` 으로 키를 바꾸고, 모호하면 **에러로 멈추게** 했습니다. 파일명도
`domestic_stock__volume_rank.py` 로 카테고리를 답니다 — 생성물끼리 덮어쓰면
같은 사고가 반복됩니다.

추출기 리포트에도 충돌 종수를 찍게 했습니다. **다음 사람이 같은 데 빠지지
않도록 숫자가 먼저 보여야 합니다.**

### 4. `NUMERIC_COLUMNS` 는 근거로 쓸 수 없습니다

이슈는 파일럿 항목에 *"`finance_balance_sheet`, `finance_income_statement` —
`NUMERIC_COLUMNS` 활용 검증"* 을 넣었습니다. 재 봤습니다.

```text
NUMERIC_COLUMNS 가 비어 있는 엔드포인트   194 / 272
숫자로 표시된 유니크 필드                 116
엔드포인트마다 엇갈리는 필드              71
```

**71개 필드가 어떤 엔드포인트에선 숫자, 다른 데선 아닙니다.** 71%의
엔드포인트는 아예 비어 있습니다. 타입 판정의 근거가 되지 못합니다.
접미사 표가 유일한 신호입니다.

### 5. 접미사 표 — 이슈의 54%를 59.9%로

이슈는 접미사 4개(`_amt` `_qty` `_dt` `_yn`)를 예로 들고 커버리지 54%를
주장했습니다. 유니크 필드 2,499개의 접미사 분포를 실측해 32개까지 채웠습니다.

```text
_amt 356   _qty 127   _cd 127   _dt 89   _rate 81   _name 81
_pbmn 78   _yn 75     _vol 63   _smtl 44 _date 35   _code 35 ...
```

**59.9%** 입니다. 남은 40%는 `KisString` 으로 둡니다 — `KisString` 은 어떤
문자열도 받으므로 **런타임 파싱 에러가 나지 않습니다.** 커버리지는 편의의
문제이지 정확성의 문제가 아닙니다.

### 6. TR ID 모양을 추측했다가 틀렸습니다

검사 테스트에 `^[A-Z0-9]{8,10}$` 를 넣었더니 `FHKST66430100`(13자)에서
깨졌습니다. 스펙 314개를 실측하니 **9자 128개 · 13자 186개, 그 둘뿐**이었습니다.
정규식을 그렇게 고쳤습니다. **모양을 지어내지 말고 세야 합니다.**

### 7. 포매팅은 생성기가 하지 않습니다

생성기가 빈 줄까지 맞추게 만들다 템플릿이 읽기 어려워졌습니다. 생성 후
`ruff check --fix` + `ruff format` 을 돌리는 것으로 바꿨습니다. **생성기는
내용만 책임집니다.**

## 법적 경계 — 사람이 아니라 기계가 지킵니다

원본(`koreainvestment/open-trading-api`)에 **LICENSE 파일이 없습니다.**
README 는 "참고용으로 제공"이라고만 적습니다. 이슈의 판단대로 **사실만**
옮깁니다 — 경로 · TR ID · 필드명 · 한글 라벨.

그 규칙을 두 겹으로 강제했습니다.

1. **추출기가 원문 설명을 애초에 안 담습니다.** `--dump-prose` 같은 기능을
   의도적으로 넣지 않았습니다. 스펙 JSON 에 없는 것은 생성기가 쓸 수 없습니다
2. **`tests/unit/test_codegen_pilot.py` 가 생성물을 검사합니다** — 원본 런타임
   어휘(`_url_fetch`, `pd.DataFrame`, `kis_auth`)와 출력 문구(`Call Next`,
   `확인요망`)가 섞였는지, 필드 docstring 이 **라벨**인지 문장인지

*"docstring verbatim 복사 금지"* 는 사람이 눈으로 지키는 규칙인데,
**300개 규모에서 눈은 지키지 못합니다.**

## 회귀 확인 — 누출 검사기를 실제로 뚫어 봤습니다

원본에서 한 줄을 진짜로 가져와 생성물에 붙였습니다.

```console
$ # res = ka._url_fetch(API_URL, tr_id, tr_cont, params)   ← 원문에서 복사
$ python -m pytest tests/unit/test_codegen_pilot.py -q
AssertionError: domestic_stock__volume_rank.py 에 원본 어휘가 섞였습니다: ['_url_fetch']
1 failed, 35 passed
```

**첫 시도는 실패했습니다.** `params` dict 두 줄을 붙였더니 4건이 실패했는데
누출 검사가 아니라 **문법 오류로 import 가 깨져서**였습니다. 누출 검사기는
아무것도 안 하고 있었습니다. 바늘이 들어간 줄로 다시 해서 확인했습니다.

검사기 자신이 죽어도 초록으로 보이므로 `test_guard_catches_leaked_prose` 를
따로 뒀습니다.

## 이슈 수치 대조

| | 이슈 (2026-08-27) | 실측 (2026-08-30) |
|---|---|---|
| 폴더 | 334 | 334 (auth 2 제외 → 332) |
| REST | 274 | **272** (이슈는 auth 를 REST 로 셈) |
| 웹소켓 | — | **60** ← 본문에 분류가 없었습니다 |
| REST 완전 파싱 | 271/274 = 98.9% | **272/272 = 100%** |
| 응답 필드 | 7,979 (유니크 2,801) | **5,485 (유니크 2,499)** — 이슈 수치는 웹소켓 포함으로 보입니다 |
| 접미사 타입 커버리지 | 54% | **59.9%** |
| POST(주문) | 18 | **18** ✅ |
| 이름 충돌 | — | **30종** |
| `NUMERIC_COLUMNS` | 파일럿 검증 항목 | **쓸 수 없음** |

**중단 조건 어느 것도 걸리지 않았습니다.** 파싱률은 오히려 올랐습니다.

## 생성물 — 8개

```text
 83줄  domestic_stock__volume_rank.py
 94줄  domestic_stock__fluctuation.py
 66줄  domestic_stock__market_cap.py
 51줄  domestic_stock__chk_holiday.py
128줄  domestic_stock__inquire_daily_ccld.py
 65줄  domestic_stock__finance_balance_sheet.py
 70줄  domestic_stock__finance_income_statement.py
 69줄  domestic_stock__news_title.py
```

`chk_holiday` 가 잘 나온 예입니다 — `_dt` → `KisDate`, `_yn` → `KisBool` 이
전부 맞았습니다.

## 생성기가 **하지 않는** 것

파일럿의 값은 "무엇이 자동화되는가"보다 **"무엇이 안 되는가"** 에 있습니다.

| | 왜 |
|---|---|
| `output` 이 리스트인지 단건인지 | 샘플이 `pd.DataFrame(...)` 으로만 알려줍니다. `--single` 로 사람이 지정 |
| 파라미터 검증 규칙 | 샘플의 `raise ValueError(...)` 는 **원문 로직**입니다. 옮기지 않습니다 |
| scope 바인딩 | Protocol 필요 여부 판정이 필요합니다 ([#45](https://github.com/visualmoney/vm-stock-kis/issues/45) 판정표) |
| 필드명 한국어→영어 | 기계가 정하면 공개 API 이름이 흔들립니다 |
| 4-way tr_id 분기 조건 | TR ID 는 전부 모으지만 **어떤 조건에서 갈리는지**는 주석으로 남기고 사람에게 넘깁니다 |

### #45 가 여기서 값을 냈습니다

파일럿 8개는 전부 단일 시장이고 공개 타입이 아니므로, [#45](https://github.com/visualmoney/vm-stock-kis/issues/45)
의 판정표(T1/T2/T3)로 **Protocol 이 필요 없습니다.** 생성기가 Protocol 을 만들지
않아도 되는 근거가 문서에 있습니다. 기준이 없었다면 생성기가 무엇을 만들어야
하는지부터 논쟁이 됐을 것입니다.

## 왜 패키지에 넣지 않았는가

`scripts/codegen/pilot/` 은 **휠에 들어가지 않습니다**(확인함). 이유는 셋입니다.

1. 파일럿의 목적은 **생성기 검증**이지 8개 엔드포인트 출시가 아닙니다
2. 공개 API 추가는 CHANGELOG · 문서 · scope 바인딩을 동반합니다 —
   [#85](https://github.com/visualmoney/vm-stock-kis/issues/85) `0.1.0` 이 대기
   중인 시점에 끼워 넣을 일이 아닙니다
3. 위 "하지 않는 것" 5가지가 남아 있어 **지금 넣으면 손으로 고쳐야 하고,
   손으로 고친 생성물은 다음 생성 때 사라집니다**

## 변경 파일

- `scripts/extract_kis_specs.py` — 신규. 스펙 추출 + 수치 리포트
- `scripts/generate_endpoint.py` — 신규. vmkis 스타일 모듈 생성
- `scripts/codegen/pilot/*.py` — 생성물 8개 (패키지 아님)
- `tests/unit/test_codegen_pilot.py` — 신규. 검사 36건

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1156 passed, 24 skipped        # 이전 1120 + 신규 36

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 223 files already formatted / Contracts: 2 kept, 0 broken.
```

## 확인하지 않은 중단 조건

*"스펙 사실 추출을 금지하는 약관 신설"* — KIS Developers 약관을 확인하지
않았습니다. 코드로 확인할 수 있는 것이 아니고, 전체 이관에 착수하기 전에
사람이 봐야 합니다.
