# 2026-08-30 - #21 평문 커서 누락 — 파일럿 완료 조건 점검 개발 일지

## 작업 내용

*"#21은 종료 조건을 만족하는지?"* 를 확인하려고 파일럿 8개를 **본문이 지정한
검증 목적** 대비로 훑었고, **하나가 안 되고 있었습니다.** 고쳤습니다.

## 무엇에 걸렸는가

### 1. "다 됐다"고 말하기 전에 항목별로 확인했습니다

본문은 8개 각각에 **왜 그것을 골랐는지**를 적어 두었습니다. 그 목적 대비로
표를 만들자 `chk_holiday` 가 비었습니다.

```text
chk_holiday   page_size=None   ← "평문 CTX_AREA_FK 페이지네이션 (#16과 연관)"
```

`None` 이면 페이징이 없다는 뜻인데, **원본에는 커서가 있습니다.**

### 2. 정규식이 폭 숫자를 요구했습니다

```python
_CURSOR = re.compile(r"ctx_area_[fn]k(\d+)")
```

KIS 커서에는 네 가지 변형이 있고 그중 하나가 **접미사 없는 `CTX_AREA_FK`**
입니다. `\d+` 는 숫자를 **요구**하므로 그 변형을 통째로 건너뜁니다.

그리고 하필 그것이 **`#21` 이 파일럿 항목으로 지목한 엔드포인트**였습니다.
본문이 "평문 `CTX_AREA_FK`"라고 명시까지 했는데, 제가 정규식을 쓸 때 그 문장을
읽지 않았습니다.

### 3. 고쳤더니 이번엔 `0` 이 falsy 였습니다

`(\d*)` 로 바꾸고 평문을 `NO_SUFFIX = 0` 으로 표현하게 했는데, 생성기가
여전히 `page_size` 를 안 냈습니다.

```python
if spec.get("page_size"):        # 0 은 falsy 입니다
```

**`0` 은 "값이 없다"가 아니라 "폭을 모르는 평문 커서"입니다.** `None`(페이징
없음)과 구분되어야 하는데 `if x:` 가 둘을 뭉갰습니다. `is not None` 으로
고쳤습니다.

> `NO_SUFFIX = 0` 은 `#16` 이 `KisPage` 에 도입한 표현입니다. 라이브러리가
> 이미 쓰는 어휘를 생성물이 따르게 했습니다 — 제가 다른 센티널을 만들면
> 같은 개념이 두 벌이 됩니다.

### 4. 분포가 #16 의 전수 조사와 정확히 일치했습니다

고친 뒤 다시 세니 이렇습니다.

| | #16 (2026-08월 기록) | 이번 실측 |
|---|---|---|
| `CTX_AREA_FK100` | 15 | **15** |
| `CTX_AREA_FK200` | 25 | **25** |
| `CTX_AREA_FK` (평문) | 2 | **2** |
| `CTX_AREA_FK50` | 1 | **1** |

**독립적으로 같은 수가 나왔습니다.** 추출기가 옳게 세고 있다는 가장 강한
증거입니다 — 제 숫자와 8개월 전 사람이 손으로 센 숫자가 맞았습니다.

### 5. 회귀 하나가 결함 둘을 잡습니다

`test_plain_cursor_endpoint_keeps_no_suffix_page_size` 를 넣고 **양쪽을
따로 되살려** 확인했습니다.

```console
결함 A(정규식이 폭을 요구) -> FAILED
결함 B(falsy 0)            -> FAILED
```

같은 테스트가 두 원인을 다 잡습니다. 그리고 `0 == False` 라서 값 비교만으로는
부족해 `is not None` 을 따로 단언합니다.

## 파일럿 8개 최종 점검

| 엔드포인트 | 본문이 지정한 목적 | 결과 |
|---|---|---|
| `volume_rank` | 단일 output 대표 | 블록1 · 필드19 |
| `fluctuation` · `market_cap` | 순위 계열 반복성 | 블록1 · 동형 |
| `chk_holiday` | **평문 `CTX_AREA_FK`** (#16) | `page_size=NO_SUFFIX` ← 이번에 고침 |
| `inquire_daily_ccld` | **최난도**: 4-way + FK100 + output1/2 | TR4 · 블록2 · `page_size=100` |
| `finance_*` 2건 | `NUMERIC_COLUMNS` 활용 | **활용 불가 판정** (194/272 가 비어 있음) |
| `news_title` | `outblock1` 불규칙 | 껍데기 키 제거 + 경고 기록 |

`finance_*` 만 "성공"이 아닌 "결론"입니다. 검증하려던 가설이 틀렸다는 것이
결과입니다.

## 규모 — 예상보다 작습니다

본문은 생성기 약 1,500 LOC 를 예상했습니다.

```text
scripts/extract_kis_specs.py    623
scripts/generate_endpoint.py    349
tests/unit/test_codegen_pilot.py 319
                               ----
                               1291
```

생성기 본체는 349줄입니다. **덜 만든 것이 아니라 원본이 답하지 못하는 것을
구현하지 않았기 때문입니다** — 파라미터 검증(원문 로직), scope 바인딩(설계
판단), 필드명 번역(설계 판단). 그것들을 짜 넣었으면 1,500 줄이 됐을 것이고,
**추측으로 채운 1,500 줄이 됐을 것입니다.**

## 변경 파일

- `scripts/extract_kis_specs.py` — 커서 정규식 네 변형 + `NO_SUFFIX`
- `scripts/generate_endpoint.py` — `is not None`, `NO_SUFFIX` import 방출
- `scripts/codegen/pilot/*.py` — 8개 재생성
- `tests/unit/test_codegen_pilot.py` — 회귀 1건 (42 → 43)

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1165 passed, 24 skipped

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 223 files already formatted / Contracts: 2 kept, 0 broken.
```

## 그래서 종료 조건은

**본문이 정의한 파일럿 범위는 이제 충족합니다.** 8개 전부, 각자의 목적 대비로.
중단 조건 3개도 측정으로 해소했고 약관도 검토했습니다.

다만 본문에는 `## 완료 기준` 절이 없고 **`## 파일럿 범위 (이 이슈)`** 가
그 역할을 합니다. 그 절이 *"전체 이관이 아니라 8개 파일럿만 다룹니다"* 라고
명시하므로 **전체 이관은 애초에 이 이슈 밖**입니다.

닫을 때 주의할 것 하나 — `#70` 이 완료 기준 하나를 미완료로 둔 채 닫혀서
`#85` 를 따로 만들어야 했습니다. **전체 이관 판단을 후속 이슈로 옮기지 않고
닫으면 같은 일이 반복됩니다.**
