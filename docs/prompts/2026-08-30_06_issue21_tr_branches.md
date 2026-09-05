# 2026-08-30 - #21 codegen 3차: TR ID 분기 조건 추출

## 사용자 요청

> 머지하고 1번 진행

(1번 = `tr_id` 분기 조건 추출. 파일럿 인계 코멘트가 남긴 "사람 몫" 6개 중
**정보가 원본에 있는 마지막 항목**입니다.)

## 분석

### 조건이 AST 에 그대로 있습니다

```python
if env_dv == "real":
    if pd_dv == "before":   tr_id = "CTSC9215R"
    elif pd_dv == "inner":  tr_id = "TTTC0081R"
elif env_dv == "demo":
    if pd_dv == "before":   tr_id = "VTSC9215R"
    elif pd_dv == "inner":  tr_id = "VTTC0081R"
```

조건 변수를 전수로 세면 축이 갈립니다.

```text
env_dv 94   ← 실전/모의 축
ord_dv 29 · ovrs_excg_cd 8 · pd_dv 4 · nat_dv 4 · day_dv 3 ...  ← 업무 축
```

### 이미 정해진 방식이 있습니다

`client/endpoint.py` 의 docstring 이 그대로 답입니다.

> 그 표에서 **실전/모의 차원만 떼어내 `KisEndpoint` 로 옮기면** 나머지 차원은
> 그대로 `dict[key, KisEndpoint]` 로 남습니다.

즉 새 설계가 필요 없고 **#43 이 만든 패턴에 맞추면** 됩니다.

## 계획

1. 추출기: 조건 스택을 들고 하향식으로 걸어 `tr_branches` 수집
2. 생성기: 실전/모의 축은 `KisEndpoint` 로 흡수, 업무 축은 dict
3. `else` 가지는 **조건을 특정할 수 없으므로** 그대로 표시
4. 회귀 + **결함 되살려 확인**

## 결과

4-way 분기가 `dict[업무축, KisEndpoint]` 로 정확히 접혔습니다. 회귀 2건 추가.
상세는 [docs/dev_logs/2026-08-30_06_issue21_tr_branches.md](../dev_logs/2026-08-30_06_issue21_tr_branches.md).
