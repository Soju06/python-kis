# 2026-08-30 - #21 codegen 2차: 응답 블록·페이지네이션 개발 일지

## 작업 내용

추출기에 **응답 블록**과 **연속조회 커서**를 넣고, 생성기가 블록별 클래스를
만들도록 확장했습니다. 파일럿 8개를 재생성하고 회귀 4건을 추가했습니다.

## 무엇에 걸렸는가

### 1. 첫 판이 블록 102개를 조용히 버리고 있었습니다

`getBody().outputN` 을 세어 보니 이랬습니다.

```text
블록 1개 : 177개   2개 : 87개   3개 : 6개   4개 : 1개
```

**첫 판 생성기는 `output` 하나만 가정했습니다.** 94개 엔드포인트에서
블록 102개가 사라지고 있었습니다.

`inquire_daily_ccld` 가 128줄 → **219줄**이 된 것이 그 차이입니다. 늘어난
91줄이 `output2`(체결 요약)입니다 — 첫 판은 체결 **목록**만 만들고 요약을
버렸습니다.

**그런데 테스트는 통과했습니다.** 36건 전부 초록이었습니다. 없는 것을 세는
검사가 없으면 없어진 줄 모릅니다 — 이 세션에서 다섯 번째로 만나는 형태입니다.

### 2. 리스트/단건은 절반만 알 수 있습니다

판별 신호는 샘플이 DataFrame 을 만드는 방식입니다.

```python
pd.DataFrame(res.getBody().output)     # -> list   (그대로 넘김)
pd.DataFrame([res.getBody().output])   # -> single (감싸는 이유는 dict 라서)
```

중간 변수를 거치는 경우가 많아 변수→블록 매핑을 먼저 만들고 봐야 했습니다.

결과가 이렇습니다.

```text
list     163 / 373 = 43.7%
unknown  163 / 373 = 43.7%
single    47 / 373 = 12.6%
```

**`unknown` 43.7% 를 추측으로 채우지 않았습니다.** 그쪽 샘플은 이렇게
방어하고 있습니다.

```python
output_data = res.getBody().output
if not isinstance(output_data, list):
    output_data = [output_data]
```

이게 무슨 뜻인지가 중요합니다 — **원본 생성기도 몰랐다**는 뜻입니다.
"KIS 가 dict 를 준다"는 증거가 아니라 "확신이 없어 방어했다"는 증거입니다.
샘플이 답을 갖고 있지 않으니 우리도 알 수 없습니다.

### 3. 그리고 틀리면 런타임에 터집니다

`vmkis` 쪽을 확인했습니다.

```python
class KisList(...):
    def transform(self, data):
        if not isinstance(data, list):
            raise TypeError(f"list 형을 기대하였지만, {type(data).__name__} 형이 ...")
```

**`KisList` 는 dict 를 견디지 않습니다.** 그래서 `unknown` 은 "나중에 다듬을
것"이 아니라 **실제 위험**입니다. 생성물에 경고 주석을 박고 사람에게 넘깁니다.

> `KisList` 가 dict 를 받아 주도록 고치는 방법도 있지만 **하지 않았습니다.**
> 그건 라이브러리 동작 변경이고, "KIS 가 정말 dict 를 준다"는 근거가 저에게
> 없습니다. 근거 없이 관대하게 만들면 진짜 오류를 삼키게 됩니다.

### 4. 페이지네이션은 공짜로 나왔습니다

블록을 찾다가 `ctx_area_fk200` · `ctx_area_nk100` 이 눈에 띄었습니다.
**연속조회 커서**이고 숫자가 폭입니다. `KisEndpoint.page_size` 가 정확히
그 값을 받습니다.

```text
커서 있음 40 / 272   폭 분포: 200(25) · 100(14) · 50(1)
```

찾으려던 것이 아닌데 같은 자리에 있었습니다. **AST 를 한 번 걷는 김에
가져오는 것이 나중에 다시 걷는 것보다 쌉니다.**

### 5. `COLUMN_MAPPING` 은 블록을 나누지 않습니다

블록별 클래스를 만들 수 있게 됐지만 **필드는 여전히 한 덩어리**입니다.
`chk_*.py` 의 `COLUMN_MAPPING` 이 응답 전체를 한 표로 담기 때문입니다.

그래서 블록이 여럿이면 같은 필드 집합을 각 클래스에 붙이고 **주석으로
표시**합니다. 자동으로 가를 방법이 없습니다 — 필드 이름만으로 어느 블록
소속인지 알 수 없습니다.

이것이 이 접근의 **상한**입니다. 블록 2개 이상인 94개는 사람이 갈라야 합니다.

## 회귀 확인 — 결함을 되살렸습니다

생성기를 첫 판처럼 `blocks = {"output": "unknown"}` 로 되돌렸습니다.

```console
$ python -m pytest tests/unit/test_codegen_pilot.py -q
FAILED ...::test_multi_block_endpoint_keeps_every_block
1 failed, 39 passed
```

새 검사 4건이 각각 다른 것을 봅니다.

| 검사 | 무엇을 막는가 |
|---|---|
| `test_multi_block_endpoint_keeps_every_block` | 블록을 버리는 회귀 |
| `test_pagination_cursor_becomes_page_size` | 커서를 못 읽는 회귀 |
| `test_endpoint_without_cursor_has_no_page_size` | **없는데 아무 값이나 넣는 것** |
| `test_undecided_blocks_are_marked_not_guessed` | 생성기가 추측으로 채우는 것 |

셋째와 넷째가 중요합니다 — 앞의 둘만 있으면 "무조건 200 을 넣는" 구현도
통과합니다.

## 변경 파일

- `scripts/extract_kis_specs.py` — `output_blocks` · `page_size` 추출
- `scripts/generate_endpoint.py` — 블록별 클래스, `KisList`/`KisObject` 구분,
  `page_size` 전달, `unknown` 표시
- `scripts/codegen/pilot/*.py` — 8개 재생성
- `tests/unit/test_codegen_pilot.py` — 회귀 4건 추가 (36 → 40)

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1162 passed, 24 skipped

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 223 files already formatted / Contracts: 2 kept, 0 broken.
```

## 아직 사람 몫

| | 왜 |
|---|---|
| `unknown` 블록 163개의 리스트/단건 | 원본이 모릅니다. 실제 응답을 봐야 합니다 |
| 다중 블록 94개의 필드 분배 | `COLUMN_MAPPING` 이 나누지 않습니다 |
| 파라미터 검증 규칙 | 원문 로직이라 옮기지 않습니다 |
| scope 바인딩 | Protocol 판정이 필요합니다 (#45 판정표) |
| 필드명 한국어→영어 | 기계가 정하면 공개 API 이름이 흔들립니다 |
| `tr_id` 분기 **조건** | TR ID 는 모으지만 조건은 주석으로 남깁니다 |

**전체 이관 착수 여부는 여전히 별개 판단입니다.** 이번 작업은 그때의 비용을
낮춘 것이지 결정을 대신한 것이 아닙니다.
