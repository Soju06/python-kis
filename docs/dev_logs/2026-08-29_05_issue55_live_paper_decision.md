# 2026-08-29 - #55 real/virtual → live/paper 결정 개발 일지

## 작업 내용

`needs-decision` 이슈 [#55](https://github.com/visualmoney/vm-stock-kis/issues/55) 를
**변경 (live/paper)** 으로 닫았습니다. 코드는 한 줄도 바꾸지 않았습니다 — 이 이슈의
산출물은 결정이고, 실행은 [#69](https://github.com/visualmoney/vm-stock-kis/issues/69)
→ [#70](https://github.com/visualmoney/vm-stock-kis/issues/70) 으로 넘겼습니다.

## 걸린 것

### 1. 이슈가 든 근거 하나가 실측에서 무너졌습니다

본문은 *"`real` 은 `Realtime*` 과 이름이 충돌"* 을 변경 근거로 들었습니다.
`Realtime` 개수(219 / 278)는 재 보니 **정확**했는데, 충돌 여부는 달랐습니다.

```console
$ git grep -ohiE '\breal[a-z_]*' -- src/ | wc -l
46
$ git grep -ohiE '\breal[a-z_]*' -- src/ | grep -ci realtime
1
```

`KisRealtimePrice` 는 `Kis` 뒤에 `Real` 이 붙어 **단어 경계에 걸리지 않습니다.**
충돌은 `grep -i real` 같은 부분일치에서만 생깁니다.

**개수가 맞다고 주장이 맞는 것은 아닙니다.** 219 라는 수는 검증됐지만, 그 수가
뒷받침한다고 적힌 문장은 검증된 적이 없었습니다. 결정은 그대로 "변경"이지만
근거 목록에서 이 항목을 빼고 이슈 본문에 그렇게 적었습니다.

### 2. "가장 중요한 한 줄"이 이미 깨져 있었습니다

이슈는 *"옛 키를 만나면 기본값으로 떨어지지 말고 명시적으로 실패시킨다"* 를
가장 중요한 항목으로 꼽았습니다. 그것이 **개명 이후의 요구사항**으로 적혀
있었는데, 실제로는 지금 이미 열려 있는 구멍이었습니다.

```python
src/vmkis/helpers.py:114    virtual=cfg.get("virtual", False),
```

**기본값이 `False` = 실전입니다.** 개명을 하든 안 하든, 사용자가 `virtaul: true`
로 오타를 내면 조용히 실전 계좌로 붙습니다.

이 발견이 **작업 순서를 뒤집었습니다.** 개명은 곧 "옛 키"를 만드는 행위이므로,
가드 없이 개명하면 **개명 자체가 사고의 원인**이 됩니다. 그래서 #69(가드)를
선행으로 두고 #70(개명)에 `blocked` 를 붙였습니다.

### 3. 위험 지점이 1곳이 아니라 5곳이고, 4곳이 라이브러리 밖입니다

이슈는 영향을 `config.yaml` 파일 3개로 적었습니다. 정작 문제는 **읽는 코드**였습니다.

```text
src/vmkis/helpers.py:114                virtual=cfg.get("virtual", False)
examples/01_basic/get_balance.py:43     (동일)
examples/01_basic/get_quote.py          (동일)
examples/01_basic/place_order.py        (동일)
examples/01_basic/realtime_price.py     (동일)
```

`load_config` 가 **5벌 복붙**돼 있습니다. `helpers.py` 한 곳에 가드를 넣으면
다 됐다고 착각하기 쉬운데, **예제 4벌은 보호되지 않습니다.** 예제는 사용자가
그대로 복사해 가는 코드라 오히려 노출이 더 큽니다.

쓰기 쪽도 같은 축입니다 — `save_config_interactive`(`helpers.py:146`)가
`data["virtual"]` 을 씁니다. 읽기만 고치면 쓰기와 어긋납니다.

### 4. 스키마가 같은 사실을 두 번 적고 있었습니다

작업 중 사용자가 "YAML 스키마 변경도 포함"을 지시해 스키마를 열어 봤더니,
키 이름과 무관한 결함이 있었습니다.

```yaml
configs:
  virtual:            # 프로필 이름
    virtual: true     # 같은 사실을 또
```

**둘이 어긋났을 때 어느 쪽이 이기는지 정의가 없습니다.** `load_config` 는 프로필
딕셔너리를 그대로 돌려주고 일치를 검사하지 않습니다. 프로필 이름은 사용자가
자유롭게 짓는 것(`VMKIS_PROFILE`)이라 이름에서 추론할 수도 없습니다.

```yaml
configs:
  virtual:
    virtual: false    # 모의 프로필인데 실전으로 붙습니다
```

그래서 #70 범위에 **불리언 → `mode: live|paper` enum** 을 넣었습니다. 불리언은
"없음"이 곧 `False`(실전)지만 enum 은 "없음"이 그냥 없음이라, 2번의 구멍이
구조적으로 사라집니다. 값 오타(`mode: papr`)도 enum 위반으로 잡힙니다.

### 5. 문서가 이미 `live` 를 쓰고 있었습니다

```text
config.example.real.yaml:1    # Real-only config example (live trading)
```

개명을 결정하고 나서야 눈에 들어왔습니다. 파일 이름은 `real` 인데 첫 줄 설명은
`live trading` 입니다.

## 변경 파일

코드 변경 없음. 문서 2건과 이슈 3건입니다.

- `docs/prompts/2026-08-29_05_issue55_live_paper_naming.md` - 판단 재료
- `docs/dev_logs/2026-08-29_05_issue55_live_paper_decision.md` - 이 문서
- 이슈 #55 - 본문에 결정·근거 추가, 제목에 결론, CLOSED
- 이슈 #69 - 신설 (선행, `next-up`)
- 이슈 #70 - 신설 (`blocked`, 선행 #69)

## 테스트 결과

**실행하지 않았습니다.** 코드 변경이 없습니다. 이 세션의 산출물은 결정과 문서입니다.

회귀 테스트는 #69 에서 씁니다 — 오타 키(`virtaul: true`)를 넣고 **실패하는지**
확인하고, 결함을 되살려 되돌려 확인한 결과를 그때 일지에 적습니다.

## 다음 할 일

- [ ] #69 착수 (`next-up`) — `load_config` 통합 + 미지의 키 예외
- [ ] #69 가 닫히면 #70 에서 `blocked` 제거
- [ ] #70 착수 시 `tr_real`/`tr_virtual` 118건을 개명 범위에 넣을지 정하고 근거를 본문에 기록
