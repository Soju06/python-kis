# 2026-08-28 - Issue #59 rate limiter 플레이키 테스트 개발 일지

**대상 이슈**: [#59](https://github.com/visualmoney/vm-stock-kis/issues/59)
**변경**: 한 줄

---

## 요약

```text
994 passed, 22 skipped / TOTAL 91.39%
커버리지 ON 반복 실행   이전 10회 중 1회 실패 -> 20회 연속 통과
```

---

## 1. 원인 — 여섯 곳을 고치면서 한 곳을 빠뜨렸습니다

커밋 `614b68e` 가 "타이밍 단언의 상한 여유 확대"를 하면서 상한 6곳을
`SCHEDULING_SLACK`(2.0)으로 바꿨습니다.

```text
-        assert 0.9 <= total_time <= 1.3
+        assert 0.9 <= total_time <= 1.0 + SCHEDULING_SLACK
-        assert 0.9 <= elapsed <= 1.3
+        assert 0.9 <= elapsed <= 1.0 + SCHEDULING_SLACK
-        assert 1.8 <= elapsed <= 2.5
+        assert 1.8 <= elapsed <= 2.0 + SCHEDULING_SLACK
-        assert 1.9 <= elapsed <= 2.5
+        assert 1.9 <= elapsed <= 2.0 + SCHEDULING_SLACK
-        assert 0.4 <= elapsed <= 0.8
+        assert 0.4 <= elapsed <= 0.5 + SCHEDULING_SLACK
```

`test_rate_limiter_thread_safety` 의 `assert 0.9 <= elapsed <= 1.3` 만
남았습니다. **하필 스레드 4개를 동시에 돌려 스케줄링에 가장 민감한
테스트인데 여유가 가장 좁습니다**(기대 1.0 에 +0.3).

그 커밋이 상수 주석에 남긴 진단이 이 건에 그대로 적용됩니다.

> 전체 스위트는 CPU를 포화시키는 벤치마크와 함께 돌기 때문에, 기대값에
> 0.3~0.4초만 얹은 상한은 부하가 걸릴 때 터진다.

---

## 2. 수정 — 한 줄

```python
assert 0.9 <= elapsed <= 1.0 + SCHEDULING_SLACK
```

**하한 `0.9` 는 건드리지 않았습니다.** 하한은 *"유량 제한이 실제로
걸렸는가"* 를 검증하므로 엄격해야 합니다.

왜 빠뜨렸었는지를 주석으로 남겼습니다. 다음 사람이 상한을 다시 좁히지
않게 하는 것이 목적입니다.

---

## 3. 되돌려 확인 — 상한을 늘리고도 회귀를 잡는가

이슈에 적은 착수 전 확인입니다. **상한만 늘리고 통과만 보면, 유량 제한이
사라진 회귀를 못 잡는 상태가 될 수 있습니다.** 프로덕션 코드를 변이시켜
두 경계를 각각 확인했습니다.

| 변이 (`utils/rate_limit.py`) | 무엇을 흉내내나 | 결과 |
|---|---|---|
| 대기 `sleep` 제거 | **유량 제한이 사라짐** | `assert 0.9 <= 0.0009…` → **하한이 잡음** |
| 대기에 `period * 3` 추가 | **대기가 주기만큼 더 늘어남** | `assert 4.05… <= (1.0 + 2.0)` → **상한이 잡음** |

`SCHEDULING_SLACK` 주석의 주장 — *"대기가 한 주기 더 늘어나는 회귀는 이
여유(2초)보다 크므로 상한이 여전히 잡는다"* — 이 실제로 성립함을
확인했습니다.

---

## 4. 플레이키 소멸 확인

```console
# 수정 전
$ for i in $(seq 1 10); do pytest <이 테스트> --cov=vmkis; done
10회 중 1회 실패

# 수정 후
$ for i in $(seq 1 20); do pytest <이 테스트> --cov=vmkis; done
20회 연속 통과
```

전체 스위트도 커버리지 켜고 3회 연속 통과했습니다.

---

## 변경 파일

- `tests/unit/utils/test_rate_limit_accuracy.py` — 173행 상한 + 주석

## 테스트 결과

```text
994 passed, 22 skipped
TOTAL 91.39%  (게이트 90)
ruff check  통과
```

## 다음 할 일

- [ ] 이 파일의 남은 두 단언(62행 `elapsed >= 0.9`, 193행 `elapsed < 1.0`)은
      **하한/무대기 단언**이라 성격이 다릅니다. 손대지 않는 것이 맞습니다
