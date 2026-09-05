# 2026-08-27 - Issue #3 테스트 스위트 부채 정리

## 사용자 요청

> Issue #3 작업 시작하기
> (이후) 작업 시작 승인, #3 이후 커밋 하고 #2 작업 진행

대상 이슈: [visualmoney/vm-stock-kis#3](https://github.com/visualmoney/vm-stock-kis/issues/3)
`test: 8개월간 미실행이던 테스트 스위트 복구 후 드러난 실패 3건 + 커버리지 게이트 복원(70→90)`

## 배경

`tests/unit/test_logging.py`가 커밋 `d9f104a`에서 잘린 채 커밋되어 `SyntaxError`
상태였고, pytest는 수집 단계 오류 시 전체 실행을 중단한다. CI는 `--maxfail=1`로
돌고 있었으므로 약 8개월간 스위트가 완주한 적이 없었다.

구문 오류는 uv 전환 PR(`16bf568`)에서 복구되었고, 그 결과 드러난 부채를 정리한다.

## 베이스라인 실측 (2026-08-27, 작업 착수 시점)

```text
3 failed, 870 passed, 8 skipped, 17 errors in 59.25s
TOTAL coverage 89.01%
```

* 실패 3건은 이슈 본문과 정확히 일치.
* `17 errors`는 실 API 자격증명을 요구하는 테스트(`tests/unit/test_account_balance.py`,
  `tests/unit/test_product_quote.py`)로, CI는 `-m 'not requires_api'`로 제외한다.
  이슈 본문의 `17 deselected`와 같은 대상이다.

## 작업 범위

| # | 항목 | 분류 |
|---|------|------|
| 1 | 로깅 통합 테스트 2건 `capsys` → `capfd` | 테스트 수정 |
| 2 | Rate limit 동시성 테스트 실패 원인 규명 및 수정 | 원인 분석 |
| 3 | 커버리지 89.01% → 90% 복원, `fail_under` 70 → 90 | 커버리지 |
| 4 | 재발 방지 (pre-commit `check-ast`, CI 수집 스텝 분리) | 인프라 |

## 원인 분석

### 1. 로깅 테스트 — `capsys`가 로거 출력을 보지 못함

`pykis/logging.py`의 `_create_logger()`가 모듈 import 시점에 실행되며
`logging.StreamHandler(stream=sys.stdout)`이 **그 시점의 `sys.stdout` 객체를
캡처**한다. pytest의 `capsys`는 나중에 `sys.stdout`을 교체하므로 이미 붙잡힌
핸들러의 출력은 관측되지 않는다.

`logging.StreamHandler`의 정상 동작이며 라이브러리 버그가 아니다.
파일 디스크립터 수준에서 캡처하는 `capfd`가 올바른 도구다.

`test_json_logger_output_format`은 `enable_json_logging()`이 핸들러를 **재생성**
하여 그 시점의 `sys.stdout`(= capsys가 교체한 객체)을 잡기 때문에 통과하고 있었다.
동일 클래스의 세 테스트 중 둘만 실패한 이유가 이것이다.

### 2. Rate limit — 만료된 토큰 픽스처로 인한 매 요청 재발급

`mock_token_response` 픽스처가 만료 시각을 **`"2025-12-31 23:59:59"`로 하드코딩**
하고 있다. 오늘(2026-08-27) 기준 이미 만료된 값이다.

`PyKis.primary_token`은 `remaining < timedelta(minutes=10)`이면 재발급하므로,
만료된 토큰은 **매 요청마다 재발급**된다. 그리고 `token_issue()`는
`self.fetch()` → `self.request()` 경로를 타므로 **동일 rate limiter 쿼터를 소비**한다.

따라서 실제 유량 획득 횟수는 10회가 아니라 20회(요청 10 + 토큰 발급 10)다.

`RateLimiter`(rate=2, period=1) 동작을 따라가면 대기는 3번째 획득부터 2회마다
발생하고 1회 대기는 `period + 0.05 = 1.05`초다:

* 20회 획득 → 대기 9회 → **9.45초** (실측 9.47초, 이슈 본문의 "대기 경고 9회"와 일치)
* 11회 획득(토큰 1회 + 요청 10회) → 대기 5회 → **5.25초** (기대 구간 4.5~6.0 내)

**결론**: 라이브러리 버그가 아니라 **테스트 픽스처의 시한폭탄**이다.
토큰 발급이 쿼터를 소비하는 것은 실제 API 호출이 맞으므로 보수적으로 옳은 동작이며
구현을 바꾸지 않는다. 픽스처의 만료 시각을 상대 시각으로 바꾸고, 타이밍 단언을
머신 속도에 덜 민감하도록 재작성한다.

### 3. `helpers.py` 27% — 함수 본문에 통째로 중첩된 죽은 코드

`save_config_interactive()`의 본문(81~162행)이 **모듈 전체의 복사본**이다.
`import`, `__all__`, `load_config`/`create_client`/`save_config_interactive`의
중복 정의가 함수 안에 중첩되어 있고, 바깥 함수는 이들을 **호출하지도 반환하지도
않는다**. 즉 `save_config_interactive()`는 아무 일도 하지 않고 `None`을 반환한다.

문서화된 반환 타입은 `dict[str, Any]`이고 `pykis/__init__.py`가 이 함수를
공개 API로 export하므로 **실사용 시 오동작하는 버그**다.
커버리지 27%는 증상이고, 원인은 잘못된 붙여넣기다.

## 계획

1. 프롬프트 문서 작성 (이 문서)
2. 로깅 테스트 2건 `capsys` → `capfd`
3. rate limit 픽스처 상대 시각화 + 단언 재작성
4. `helpers.py` 죽은 코드 제거 및 함수 복구, 테스트 보강
5. `fail_under` 70 → 90 복원
6. pre-commit `check-ast` 추가, CI 수집 스텝 분리
7. 개발 일지 작성 후 커밋

## 결과

완료. 상세는 [개발 일지](../dev_logs/2026-08-27_issue3_test_suite_recovery.md) 참조.

```text
943 passed, 8 skipped, 17 deselected
Required test coverage of 90.0% reached. Total coverage: 90.63%
```

작업 중 이슈 본문의 진단 두 가지가 사실과 다름을 확인했다.

1. **로깅**: 제안된 `capsys` → `capfd` 교체로는 해결되지 않는다. 핸들러가 붙잡은
   스트림은 fd 1이 아니라 pytest가 세션 시작 시 설치한 전역 캡처 객체라,
   `capfd`가 새로 거는 캡처와도 다르다. 핸들러 스트림을 직접 교체하는 방식으로 해결.
2. **CI**: "`--maxfail=1`로 돌고 있어 눈치채지 못했다"가 아니라 **CI가 단 한 번도
   실행된 적이 없다**. `ci.yml`이 74행에서 YAML 파싱 실패 상태이고, 7번의 실행이
   전부 0초 만에 failure다. `--maxfail=1`은 아무것도 가리지 않았다.
