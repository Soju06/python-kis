# 2026-08-30 - #21 codegen 3차: TR ID 분기 조건 개발 일지

## 작업 내용

TR ID 를 **그것이 선택되는 조건과 함께** 추출하고, 생성기가 실전/모의 축과
업무 축을 갈라 `KisEndpoint` / `dict[key, KisEndpoint]` 로 내도록 했습니다.

## 무엇에 걸렸는가

### 1. 설계를 새로 할 필요가 없었습니다

`client/endpoint.py` 의 docstring 이 이미 답을 적어 두었습니다.

> 그 표에서 **실전/모의 차원만 떼어내 `KisEndpoint` 로 옮기면** 나머지 차원은
> 그대로 `dict[key, KisEndpoint]` 로 남습니다.

`#43` 이 손으로 하던 것을 기계가 하게 하면 됩니다. **저장소가 이미 내린
결정을 다시 내리지 않는 것**이 이번 작업의 절반이었습니다.

결과가 `#21` 이 최난도로 지목한 엔드포인트에서 이렇게 나옵니다.

```python
#: pd_dv -> 엔드포인트.
#: 실전/모의 축은 KisEndpoint 가 tr_live/tr_paper 로 흡수합니다.
INQUIRE_DAILY_CCLD_ENDPOINTS: dict[str, KisEndpoint] = {
    "before": KisEndpoint(path=..., tr_live="CTSC9215R", tr_paper="VTSC9215R", page_size=100),
    "inner":  KisEndpoint(path=..., tr_live="TTTC0081R", tr_paper="VTTC0081R", page_size=100),
}
```

4-way 행렬이 **2×2 로 정확히 접혔습니다.**

### 2. `ast` 에 부모 링크가 없습니다

`tr_id = "X"` 에서 위로 올라가며 조건을 모으는 것이 자연스러운데, `ast` 노드는
부모를 모릅니다. `ast.walk` 은 평평하게 순회하므로 **어느 `if` 안이었는지
잃습니다.**

조건 스택을 들고 **하향식**으로 걷는 재귀로 바꿨습니다. `elif` 가
`orelse` 안의 `If` 로 표현된다는 것도 함께 다뤄야 했습니다.

### 3. `else` 가지는 조건을 적을 수 없습니다

```python
if env_dv == "real":   ...
elif env_dv == "demo": ...
else:                  raise ValueError(...)
```

순수 `else` 는 *"위 조건들이 전부 아니다"* 라서 **하나의 값으로 적을 수
없습니다.** 2분기면 "반대값"으로 채울 수 있지만 3분기 이상에서는 틀립니다.

`{axis: None}` 으로 두고 생성물에 경고를 답니다. **추측해서 채우면 조용히
틀린 표가 만들어집니다.**

### 4. 축 분포를 먼저 재고 시작했습니다

```text
env_dv 94   ← 실전/모의
ord_dv 29 · ovrs_excg_cd 8 · pd_dv 4 · nat_dv 4 · day_dv 3 · ord_type 2 · order_dv 2
```

`env_dv` 가 압도적이라 **도메인 축을 상수 하나로 하드코딩해도 안전**하다는
근거가 됐습니다. 재지 않았으면 축 판별 로직을 일반화하느라 시간을 썼을
것입니다 — 그리고 그 일반화는 쓰이지 않았을 것입니다.

### 5. 테스트가 dict 안을 못 보고 있었습니다

생성물이 `dict[str, KisEndpoint]` 가 되자 기존 검사 3건이 깨졌습니다.

```python
endpoints = [v for v in vars(module).values() if isinstance(v, KisEndpoint)]
```

**dict 안은 안 봅니다.** 고치지 않았다면 분기가 있는 엔드포인트는
"KisEndpoint 0개"로 보여 **검사가 조용히 통과**했을 것입니다. `_endpoints()`
헬퍼로 dict 값까지 훑게 했습니다.

### 6. "무조건 dict 로 감싸는" 구현도 통과합니다

`test_tr_id_branches_become_an_endpoint_table` 하나만 있으면 그렇습니다.
반대편을 막는 검사를 함께 넣었습니다.

```python
def test_single_branch_endpoint_stays_a_plain_constant():
    assert "VOLUME_RANK" in vars(module)
    assert not any(k.endswith("_ENDPOINTS") for k in vars(module))
```

## 회귀 확인 — 결함을 되살렸습니다

생성기를 첫 판처럼 조건을 버리게 되돌렸습니다.

```console
$ python -m pytest tests/unit/test_codegen_pilot.py -q
FAILED ...::test_tr_id_branches_become_an_endpoint_table
1 failed, 41 passed
```

## 전체 272개 기준

```text
TR ID 2개 이상            23
  실전/모의 축만          11   -> KisEndpoint 하나
  업무 축 있음            12   -> dict[key, KisEndpoint]
첫 판이 주석으로 흘렸을 TR 43
```

## 변경 파일

- `scripts/extract_kis_specs.py` — `tr_branches` (조건 스택 하향식 순회)
- `scripts/generate_endpoint.py` — `_render_endpoints()` 로 축 분리
- `scripts/codegen/pilot/*.py` — 8개 재생성
- `tests/unit/test_codegen_pilot.py` — `_endpoints()` 헬퍼 + 회귀 2건 (40 → 42)

## 테스트 결과

```console
$ python -m pytest tests/unit tests/integration -q
1164 passed, 24 skipped

$ ruff check . && ruff format --check . && lint-imports
All checks passed! / 223 files already formatted / Contracts: 2 kept, 0 broken.
```

## 이것으로 자동화 가능한 것은 끝났습니다

파일럿 인계 코멘트의 "사람 몫" 6개 중 **원본에 정보가 있던 3개를 전부**
가져왔습니다 (응답 블록 · 페이지네이션 · TR 분기).

남은 셋은 성질이 다릅니다.

| | 왜 자동화할 수 없는가 |
|---|---|
| `unknown` 블록 163개의 리스트/단건 | **원본도 모릅니다.** 실제 응답을 봐야 합니다 |
| 다중 블록 94개의 필드 분배 | `COLUMN_MAPPING` 이 블록을 나누지 않습니다 |
| 파라미터 검증 · scope 바인딩 · 필드명 번역 | 정보 부족이 아니라 **설계 판단**입니다 |

**"더 짜낼 수 있는데 안 한 것"이 아니라 "원본에 없는 것"입니다.** 전체 이관
착수 여부는 여전히 별개 판단이고, 이번 세 차례 작업은 그때의 비용을 낮췄을
뿐입니다.
