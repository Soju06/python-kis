# 2026-08-29 - #55 real/virtual → live/paper 명칭 통일 여부 결정

## 사용자 요청

> #55 착수

## 분석

이슈 [#55](https://github.com/visualmoney/vm-stock-kis/issues/55) 는 `needs-decision`
입니다. **산출물은 코드가 아니라 결정 한 줄**이고, 코드 변경은 별도 이슈로 엽니다.
코멘트는 0건이라 인계받을 함정이 없어서, 본문의 수치를 다시 재는 것부터 했습니다.

### 본문 수치 재검증 — 일치

```console
$ git grep -o Realtime -- src/
219
$ git grep -o Realtime -- src/ tests/ docs/ examples/
278
```

이슈 본문과 같습니다. (본문이 스스로 "이전 기록 236 은 낡았다"고 적어 둔 값이
현재도 유효합니다.)

### 본문에 없던 것 1 — `Realtime` 충돌은 정밀 검색에서 일어나지 않습니다

본문은 *"`real` 은 `Realtime*` 과 이름이 충돌"* 을 변경 근거로 들었습니다.
단어 경계로 재면 충돌이 없습니다.

```console
$ git grep -ohiE '\breal[a-z_]*' -- src/ | wc -l
46
$ git grep -ohiE '\breal[a-z_]*' -- src/ | grep -ci realtime
1
```

`KisRealtimePrice` 는 `Kis` 다음에 `Real` 이 붙어 있어 `\breal` 에 걸리지
않습니다. 충돌은 **대소문자 무시 부분일치**(`grep -i real`)에서만 발생하고,
그때 219건의 `KisRealtime*` 가 섞입니다. 근거가 없지는 않지만 본문이 시사하는
것보다 약합니다.

### 본문에 없던 것 2 — 위험 지점이 5곳이고, 그중 4곳은 라이브러리 밖입니다

본문은 *"옛 키를 만나면 명시적으로 실패시킨다"* 를 가장 중요한 한 줄로 꼽습니다.
그 위험이 실재하는지 확인했더니 **실재하고, 예상보다 넓습니다.**

```python
src/vmkis/helpers.py:114        virtual=cfg.get("virtual", False),
examples/01_basic/get_balance.py:43     virtual=cfg.get("virtual", False),
examples/01_basic/get_quote.py          (동일)
examples/01_basic/place_order.py        (동일)
examples/01_basic/realtime_price.py     (동일)
```

**기본값이 `False` = 실전입니다.** 키를 `paper` 로 바꾸면 옛 `virtual: true` 가
매칭되지 않아 `False` 로 떨어지고, **조용히 실전 계좌로 붙습니다.** 이슈가 경고한
시나리오 그대로입니다.

문제는 `load_config` 가 **5벌 복붙**돼 있다는 것입니다. 라이브러리(`helpers.py`)에
가드를 넣어도 **예제 4벌은 보호되지 않습니다.** 예제는 사용자가 그대로 복사해
가는 코드입니다.

### 본문에 없던 것 3 — `save_config_interactive` 가 키를 씁니다

```python
src/vmkis/helpers.py:146    data["virtual"] = v in ("y", "yes", "true", "1")
```

읽기만 바꾸면 이 함수가 새 키를 쓰고 옛 파일과 섞입니다. 쓰기 쪽도 범위입니다.

### 영향 범위 실측

`src/` 에서 `Realtime` 계열을 뺀 `real`/`virtual` 식별자는 약 **369 occurrences**
입니다. 그중 `tr_real`(61) + `tr_virtual`(57) = **118건이 KIS TR ID 개념**으로,
설정 키와는 다른 축입니다.

공개 API 노출: `__all__` 에 `create_client`, `save_config_interactive` 가 있고
`load_config` 는 없습니다. `VmKis.virtual` 프로퍼티(`kis.py:77`)와 `KisAuth(virtual=)`
는 사용자가 직접 쓰는 이름입니다.

### 판단에 영향을 준 것 — 대상 독자

`README.md` 20,248자 중 한글 8,194자, `docs/user/` 가 한글이고 영문은
`docs/user/en/` 3개 파일입니다. 주 독자가 KIS 한국어 문서(**실전/모의**)를 함께
보는 사용자라면, `paper` 는 그 문서와 대조가 안 되는 제3의 용어가 됩니다.

## 계획

1. ~~수치 재검증~~ 완료
2. ~~위험 지점 실측~~ 완료
3. ~~결정~~ 완료
4. ~~결정을 이슈 본문에 적고 제목에 결론 박아 닫기~~ 완료
5. ~~코드 이슈 개설~~ 완료

## 결과

**결정: 변경 (live/paper).** 사용자 선택입니다. 저는 유지를 권고했고, 근거는
벤더 표기(`virtual` ← VTS)와 한국어 주 독자였습니다. 사용자는 `real` 이 벤더
표기가 아니라는 점과 사용자 0명인 지금의 저렴함을 택했습니다.

작업 중 사용자가 **YAML 스키마 변경도 범위에 포함**하도록 지시해 #70 에 반영
했습니다. 스키마를 열어 보니 키 이름과 별개의 결함이 있었습니다 — 프로필 이름과
플래그가 같은 사실을 두 번 적고, 어긋났을 때의 정의가 없습니다. 불리언
`virtual: true/false` → `mode: live|paper` enum 으로 바꿉니다.

| 산출물 | |
|---|---|
| [#55](https://github.com/visualmoney/vm-stock-kis/issues/55) | 결정·근거를 본문에, 제목에 결론 박고 **CLOSED** |
| [#69](https://github.com/visualmoney/vm-stock-kis/issues/69) | 신설 — `load_config` 5벌 통합 + 미지의 키 예외. `next-up` |
| [#70](https://github.com/visualmoney/vm-stock-kis/issues/70) | 신설 — 개명 + 스키마 변경. `blocked` (선행 #69) |

순서를 뒤집은 것이 이 세션의 핵심입니다. 개명이 곧 "옛 키"를 만드는 행위라,
가드 없이 개명하면 개명 자체가 사고의 원인이 됩니다. 상세는
[개발 일지](../dev_logs/2026-08-29_05_issue55_live_paper_decision.md).
