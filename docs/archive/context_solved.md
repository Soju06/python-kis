# Codegen 점검 컨텍스트 (2026-02-12)

## 1) 파이프라인 재실행 결과

- 기준 리포트: `tmp/docs/reports/api_report.json`
- `generated_at`: `2026-02-06T07:42:47.552493+00:00`
- `smoke`: `total=498`, `errors=0`, `warnings=6`
- `augment`: `total=268`, `processed=268`, `errors=18`
- `validation`: `total=268`, `errors=0`

## 2) Smoke warnings 6 조사 결과

### 2.1 현황

- 6건 모두 `reason=empty_response`
- 실질적으로는 3개 endpoint가 2회씩 중복 집계됨
  - `147e81db-e0d2-40cd-95f5-d8da90c2d998` `/uapi/elw/v1/quotations/newly-listed`
  - `3f2f6823-fcdf-4713-a594-a03c7154096e` `/uapi/domestic-stock/v1/quotations/psearch-result`
  - `24413e7f-cca6-4ab4-8598-b9d4e2d4305d` `/uapi/domestic-stock/v1/quotations/psearch-title`

### 2.2 파라미터/응답 확인

- `psearch-title`, `psearch-result`는 호출 시 `msg_cd=MCA05762`, `msg1=조회가 계속 됩니다. (다음을 누르십시오.)` 응답 확인
- 해당 메시지는 문서 주의사항과 일치
  - `docs/kis/국내주식/시세분석/psearch-title.yaml`
  - `docs/kis/국내주식/시세분석/psearch-result.yaml`
- `newly-listed`는 기본 파라미터(`tmp/docs/reports/smoke_requests.json`) 및 대체 조합(날짜/분류/기초자산 등) 테스트에서 빈 엔벨로프(`rt_cd`, `msg_cd`, `msg1` 공백) 반복 확인
- `newly-listed`에 의도적으로 잘못된 시장코드를 넣으면 명시적 에러(`OPSQ2001`)가 내려와, 엔드포인트 자체가 죽은 상태는 아님

### 2.3 해석

- smoke warning 6건은 단순 필수 파라미터 누락보다는 API/업무상태 의존(조건검색 저장 상태, 해당 조건일자 데이터 유무 등) 성격이 큼
- 특히 `newly-listed`는 잘못된 요청에 대한 에러와 정상 요청의 빈 응답이 공존하여, 파라미터만으로 0-warning 보장을 만들기 어려운 케이스로 판단

## 3) augment errors 18 상세 (model_type 9 + missing 9)

### 3.1 분류

- `model_type`: 9건
- `missing`: 9건

### 3.2 endpoint 목록

#### `model_type` (9)

- `ca2e71e1-5ef4-4489-b4c4-118e10588690` `ELW 비교대상종목조회 [국내주식-183]` `/uapi/elw/v1/quotations/compare-stocks`
- `636e216a-f3bb-4dc6-8bc3-e6d9babca5f1` `HTS조회상위20종목 [국내주식-214]` `/uapi/domestic-stock/v1/ranking/hts-top-view`
- `4a077f43-7053-47be-b811-8e35be4ea745` `국내기관_외국인 매매종목가집계[국내주식-037]` `/uapi/domestic-stock/v1/quotations/foreign-institution-total`
- `e5c6c050-e63f-4ab7-b339-d1a645d3239b` `시장별 투자자매매동향(시세)[v1_국내주식-074]` `/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market`
- `fee465d1-7fd5-4c66-b4a4-731b813d569d` `관심종목(멀티종목) 시세조회 [국내주식-205]` `/uapi/domestic-stock/v1/quotations/intstock-multprice`
- `5c488ab2-59fd-486e-bf74-b68e813e35c0` `국내휴장일조회[국내주식-040]` `/uapi/domestic-stock/v1/quotations/chk-holiday`
- `fbfe7300-7096-4938-840b-9f7c328cc5fd` `종합 시황/공시(제목) [국내주식-141]` `/uapi/domestic-stock/v1/quotations/news-title`
- `7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a` `장내채권현재가(일별) [국내주식-202]` `/uapi/domestic-bond/v1/quotations/inquire-daily-price`
- `3acd4025-6e95-46dc-a90d-b38215912d11` `해외선물옵션 장운영시간 [해외선물-030]` `/uapi/overseas-futureoption/v1/quotations/market-time`

#### `missing` (9)

- `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` `선물옵션기간별시세(일/주/월/년)[v1_국내선물-008]` `/uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice`
- `86194480-c8f0-4b0b-9d3d-001c2fc33422` `선물옵션 분봉조회[v1_국내선물-012]` `/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice`
- `e5f413ec-3e68-47d7-931f-d7eb263990d9` `ELW LP매매추이 [국내주식-182]` `/uapi/elw/v1/quotations/lp-trade-trend`
- `a08c3421-e50f-4f24-b1fe-64c12f723c77` `국내주식기간별시세(일/주/월/년)[v1_국내주식-016]` `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice`
- `6b0b388e-f815-4009-b46d-e08e47575ca7` `국내주식 시간외호가[국내주식-077]` `/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price`
- `1e375270-7d8d-4e4b-bcac-d11cb41542cb` `국내주식 시간외현재가[국내주식-076]` `/uapi/domestic-stock/v1/quotations/inquire-overtime-price`
- `e53eb2e6-b292-4e2b-b150-22d92b401453` `ETF/ETN 현재가[v1_국내주식-068]` `/uapi/etfetn/v1/quotations/inquire-price`
- `a274b685-7ea8-441d-a2fe-3087becb6bf2` `장내채권현재가(시세) [국내주식-200]` `/uapi/domestic-bond/v1/quotations/inquire-price`
- `81269474-9c66-404f-bdfe-4bb472975330` `해외지수분봉조회[v1_해외주식-031]` `/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice`

## 4) 원인 분석 및 override 판단

### 4.1 공통 관찰

- 18건 모두 `augment` 단계에서만 에러로 집계됨
- 동일 원본 payload를 **현재 생성된 최신 raw model**로 검증 시 `18/18` 전부 통과
  - 검증 방식: `src/pykis/api/raw/registry.py`의 `ENDPOINTS[eid].response_model.model_validate(payload)`

### 4.2 `model_type` 9건

- 현상: 문서/정규화 스펙에서는 `output`/`output1`이 단일 dict(`single`)로 잡혀 있는데 실제 payload는 list
- 판단: 한국투자증권 문서/스펙 불일치 성격이 큼
- 코드 측면: inference가 payload container를 기준으로 kind를 재판정하고, generate는 이 결과를 반영하므로 최종 생성 모델은 list로 정상화됨

### 4.3 `missing` 9건

- 현상: 응답은 성공(`rt_cd=0`, `msg_cd=MCA00000`)인데 일부 필드가 누락되어 required 검증 실패
- 판단: 잘못된 요청으로 빈 전체 응답이 내려온 케이스라기보다, “정상 응답 + 필드 조건부 생략” 케이스에 가까움
- 코드 측면: inference 단계에서 누락 필드를 optional로 완화하여 최종 모델에서는 수용 가능

### 4.4 override 필요성

- 현재 상태에서는 최종 생성 결과가 이미 payload와 합치되므로, 즉시 override는 필수 아님
- 다만 **augment 단계 리포트까지 0-error로 강제**하려면 override 후보를 만들 수 있음
- 정책상 `docs/overrides/type_overrides.yaml` 반영은 명시적 승인 후에만 진행

## 5) 품질 점검 결과

- `ruff check .` 통과
- `ty check` 통과
- `pytest -q`는 인터프리터 경로 문제로 실패 가능
- `.venv/bin/python -m pytest -q` 통과 (`76 passed`)

## 6) 누락 보강: 핵심 판단 정리

### 6.1 Smoke warnings 6 (파라미터 적합성/안정값 가능성)

- warning 기준:
  - `KisResponseError` 발생 + payload가 empty로 판정되면 `empty_response` warning으로 집계
  - 판정 함수: `src/codegen/api/runtime.py`의 `is_empty_payload`
- `user_id` 채움 규칙:
  - `user_id`/`userid`는 `KisAuth.id`를 사용
  - 구현 위치: `src/codegen/api/runtime.py` `ValueResolver.resolve_with_source(...)`

#### (A) 종목조건검색 2개 (4 warnings)

- 대상 endpoint:
  - `24413e7f-cca6-4ab4-8598-b9d4e2d4305d` `/uapi/domestic-stock/v1/quotations/psearch-title`
  - `3f2f6823-fcdf-4713-a594-a03c7154096e` `/uapi/domestic-stock/v1/quotations/psearch-result`
- smoke 파라미터 자체는 정상(필수 누락 없음)
- 실제 real 호출 응답:
  - `msg_cd=MCA05762`, `msg1=조회가 계속 됩니다. (다음을 누르십시오.)`
- 문서에도 동일 안내가 존재:
  - `docs/kis/국내주식/시세분석/psearch-title.yaml`
  - `docs/kis/국내주식/시세분석/psearch-result.yaml`
- 결론:
  - 파라미터 튜닝만으로 안정적으로 해결하기 어렵고, HTS(eFriend Plus)에서 조건 등록 + “사용자조건 서버저장” 선행이 사실상 필요
  - 정상화 후 안정 흐름은 `psearch-title.output2[].seq -> psearch-result.seq`

#### (B) ELW 신규상장종목 1개 (2 warnings)

- 대상 endpoint:
  - `147e81db-e0d2-40cd-95f5-d8da90c2d998` `/uapi/elw/v1/quotations/newly-listed`
- smoke 파라미터는 모델/문서 기준 정상 형태(필수 누락 없음)
  - 관련 request 모델: `src/pykis/api/raw/국내주식/ELW_시세/newly_listed.py`
- 실제 호출:
  - HTTP 200이지만 `rt_cd/msg_cd/msg1`가 비어 있는 empty envelope 반복
  - 반대로 의도적 잘못된 코드 입력 시 명시적 에러(`OPSQ2001`)는 정상 수신
- 결론:
  - 잘못된 요청이라기보다 KIS 측 빈 응답 정책/데이터 상태 의존 가능성이 높음
  - 현재 smoke에서 warning이 발생하는 것을 완전히 제거하기 어려운 타입

#### Smoke 운영 판단

- “항상 green”이 목표라면 아래 3개 endpoint는 smoke에서 제외(SKIP) 또는 warning 허용 정책을 적용하는 것이 현실적
  - `147e81db-e0d2-40cd-95f5-d8da90c2d998`
  - `24413e7f-cca6-4ab4-8598-b9d4e2d4305d`
  - `3f2f6823-fcdf-4713-a594-a03c7154096e`

### 6.2 `model_type` 9개 (문서 오류 vs 로직 문제)

- 핵심:
  - 문서/정규화 스펙은 `output` 또는 `output1`을 `single(dict)`로 보지만, 실제 payload는 `list`
  - 따라서 근본 원인은 문서/정규화 스펙 불일치
- 로직 상태:
  - infer가 런타임 샘플 기준으로 container kind를 교정하고, generate가 그 결과를 반영
  - 예시 생성물(list 반영): `src/pykis/api/raw/장내채권/기본시세/inquire_daily_price.py`
- override 판단:
  - SDK 최종 생성물 기준으로는 이미 정상이라 “즉시 override 필수”는 아님
  - 다만 augment 리포트 0-error/캐시 효율이 목표면 override를 검토할 가치 있음

### 6.3 `missing` 9개 (빈 응답/간헐성/필수값 판단)

- 핵심:
  - 9건은 “전체 빈 응답”이 아니라, 성공 응답(`rt_cd=0`, `msg_cd=MCA00000`)에서 일부 필드만 누락된 케이스
  - 즉 `required`가 문서 기준으로 과도하게 잡힌 경우가 주원인
- 로직 상태:
  - infer에서 누락 필드를 optional로 완화하는 경로가 이미 있음
  - 구현 위치: `src/codegen/api/steps/infer.py`
- 예시(`a274b685...`):
  - 정규화 스펙에는 `stnd_iscd` required로 잡힘
    - `tmp/docs/normalized/장내채권/기본시세/inquire_price__a274b685-7ea8-441d-a2fe-3087becb6bf2.json`
  - 실제 성공 payload에서는 해당 키가 빠질 수 있음
  - 최종 생성 raw 모델은 optional로 생성됨
    - `src/pykis/api/raw/장내채권/기본시세/inquire_price.py`

### 6.4 실행 옵션

- 옵션 A: smoke 안정성 우선
  - 위 3개 endpoint를 smoke SKIP/allow-warning 처리
- 옵션 B: 문서 정합성/리포트 0-error 우선
  - `model_type 9 + missing 9`에 대해 override 후보를 드래프트로 작성
  - 승인 메타데이터 확정 후 `docs/overrides/type_overrides.yaml` 반영

## 7) HTS 조건검색 추가 이후 재확인 (2026-02-12 17:54 KST 근접)

- 확인 대상:
  - `24413e7f-cca6-4ab4-8598-b9d4e2d4305d` (`psearch-title`)
  - `3f2f6823-fcdf-4713-a594-a03c7154096e` (`psearch-result`)
- 확인 방식:
  - real 계정(`user_id=soju06`)으로 endpoint 직접 호출
  - smoke와 동일하게 각 endpoint 2회 시도
- 결과:
  - `psearch-title` 2회 모두 `HTTP 200`, `rt_cd=0`, `msg_cd=MCA00000`, `msg1=정상처리 되었습니다.`, `output2_count=1`, `seq=0`
  - `psearch-result(seq=0)` 2회 모두 `HTTP 200`, `rt_cd=0`, `msg_cd=MCA00000`, `msg1=정상처리 되었습니다.`, `output2_count=100`
- 결론:
  - HTS에서 조건 추가/서버저장 반영이 현재 API 호출 결과에 정상적으로 나타남
  - 이전 `MCA05762` 상태는 해소된 것으로 판단

## 8) 수동 enum override 후보 시스템 추가 (2026-02-12)

- 자동 수용은 적용하지 않음 (`src/pykis/common/enums.py` 변경 미적용 상태 유지)
- enum 문서/실응답 드리프트는 inference trace에 후보 정보로만 기록
  - `documented_values`
  - `sample_values`
  - `unknown_sample_values`
- 후보 산출물:
  - `tmp/docs/reports/enum_drift_candidates.json`
  - 현 시점 집계: `total=17`, `endpoints=9`
- 수동 반영 초안 산출물(승인 전):
  - `tmp/docs/reports/type_override_candidates_enum.json`
  - `tmp/docs/reports/type_override_candidates_enum.md`
  - 현 시점 집계: `draft_overrides=9`, `total_candidates=17`
- 초안은 `docs/overrides/type_overrides.yaml`에 자동 반영되지 않음
  - 각 항목에 `approved_by`, `approved_at` placeholder를 두고 수동 승인 전용으로 유지

### 8.1 우선순위 분류 산출물

- 파일:
  - `tmp/docs/reports/type_override_candidates_enum_priority.json`
  - `tmp/docs/reports/type_override_candidates_enum_priority.md`
- 분류 요약:
  - `ready_overrides=4`
  - `hold_overrides=5`
- Ready(승인 우선) endpoint:
  - `011d4de2-a4a0-47c0-aa47-20c65a26a763`
  - `1394ba1d-e17d-42c8-8e53-6bed5dce7588`
  - `a08c3421-e50f-4f24-b1fe-64c12f723c77`
  - `af3d3794-92c0-4f3b-8041-4ca4ddcda5de`
- 분류 기준(자동):
  - `request.*` 위치 enum 변경은 보류
  - 고카디널리티(unknown 20+) 보류
  - 시간형 필드 enum 확장 보류
  - 소수점형 샘플(`0.00` 등) 기반 enum 확장 보류(파서/추론 보정 후보)

## 9) 최신 파이프라인 재실행 결과 (2026-02-13 14:30 KST)

- 기준 리포트:
  - `tmp/docs/reports/api_report.json` (`generated_at=2026-02-13T05:30:12.172540+00:00`)
  - `tmp/docs/reports/augment.json`
  - `tmp/docs/reports/smoke.json`
- 결과 요약:
  - `augment`: `total=268`, `processed=268`, `ok=18`, `cached=174`, `skipped=76`, `errors=0`
  - `smoke`: `total=287`, `errors=0`, `warnings=1`
  - `validation`: `errors=0`

## 10) 현재 잔여 이슈 (실패 아님, 추적 필요 항목)

### 10.1 smoke warning 1

- endpoint: `147e81db-e0d2-40cd-95f5-d8da90c2d998` (`/uapi/elw/v1/quotations/newly-listed`)
- reason: `empty_response`
- 해석:
  - 잘못된 파라미터로 보기는 어렵고, KIS 측 데이터 상태/빈 응답 정책 영향으로 판단
  - 현재 정책대로 warning 유지가 타당

### 10.2 augment `validation_error` note 18

- `errors=0`이지만, `ok + note=validation_error`로 18건 기록
- 분류:
  - `model_type`: 9건
  - `missing`: 8건
  - `model_validation_exception`(class-not-fully-defined): 1건 (`a08c3421-e50f-4f24-b1fe-64c12f723c77`)
- 의미:
  - augment 시점 문서/정규화 스펙과 실응답이 충돌한 케이스를 hard-fail 대신 note로 보존
  - 이후 inference/generate를 거친 최종 raw 모델 및 validation 단계는 정상 통과

### 10.3 운영 판단

- 현재 파이프라인 품질 관점:
  - hard error 기준으로는 green (`augment errors=0`, `smoke errors=0`)
  - 남은 이슈는 문서-실응답 드리프트 추적 항목
- 후속 선택지:
  - A) 현 상태 유지(권장): note/warning 추적으로 운영
  - B) 리포트 완전 무노이즈 지향: 수동 override 승인 프로세스로 문서 보정

## 11) augment `validation_error` 18건 상세표 (2026-02-13 14:30 KST)

### 11.1 endpoint 요약

| id | issue_type | field_count | name | path |
| --- | --- | ---: | --- | --- |
| `1e375270-7d8d-4e4b-bcac-d11cb41542cb` | `missing` | 4 | 국내주식 시간외현재가[국내주식-076] | `/uapi/domestic-stock/v1/quotations/inquire-overtime-price` |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | 14 | 국내주식 시간외호가[국내주식-077] | `/uapi/domestic-stock/v1/quotations/inquire-overtime-asking-price` |
| `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` | `missing` | 3 | 선물옵션기간별시세(일/주/월/년)[v1_국내선물-008] | `/uapi/domestic-futureoption/v1/quotations/inquire-daily-fuopchartprice` |
| `81269474-9c66-404f-bdfe-4bb472975330` | `missing` | 2 | 해외지수분봉조회[v1_해외주식-031] | `/uapi/overseas-price/v1/quotations/inquire-time-indexchartprice` |
| `86194480-c8f0-4b0b-9d3d-001c2fc33422` | `missing` | 3 | 선물옵션 분봉조회[v1_국내선물-012] | `/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice` |
| `a274b685-7ea8-441d-a2fe-3087becb6bf2` | `missing` | 3 | 장내채권현재가(시세) [국내주식-200] | `/uapi/domestic-bond/v1/quotations/inquire-price` |
| `e53eb2e6-b292-4e2b-b150-22d92b401453` | `missing` | 2 | ETF/ETN 현재가[v1_국내주식-068] | `/uapi/etfetn/v1/quotations/inquire-price` |
| `e5f413ec-3e68-47d7-931f-d7eb263990d9` | `missing` | 1 | ELW LP매매추이 [국내주식-182] | `/uapi/elw/v1/quotations/lp-trade-trend` |
| `3acd4025-6e95-46dc-a90d-b38215912d11` | `model_type` | 1 | 해외선물옵션 장운영시간 [해외선물-030] | `/uapi/overseas-futureoption/v1/quotations/market-time` |
| `4a077f43-7053-47be-b811-8e35be4ea745` | `model_type` | 1 | 국내기관_외국인 매매종목가집계[국내주식-037] | `/uapi/domestic-stock/v1/quotations/foreign-institution-total` |
| `5c488ab2-59fd-486e-bf74-b68e813e35c0` | `model_type` | 1 | 국내휴장일조회[국내주식-040] | `/uapi/domestic-stock/v1/quotations/chk-holiday` |
| `636e216a-f3bb-4dc6-8bc3-e6d9babca5f1` | `model_type` | 1 | HTS조회상위20종목 [국내주식-214] | `/uapi/domestic-stock/v1/ranking/hts-top-view` |
| `7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a` | `model_type` | 1 | 장내채권현재가(일별) [국내주식-202] | `/uapi/domestic-bond/v1/quotations/inquire-daily-price` |
| `ca2e71e1-5ef4-4489-b4c4-118e10588690` | `model_type` | 1 | ELW 비교대상종목조회 [국내주식-183] | `/uapi/elw/v1/quotations/compare-stocks` |
| `e5c6c050-e63f-4ab7-b339-d1a645d3239b` | `model_type` | 1 | 시장별 투자자매매동향(시세)[v1_국내주식-074] | `/uapi/domestic-stock/v1/quotations/inquire-investor-time-by-market` |
| `fbfe7300-7096-4938-840b-9f7c328cc5fd` | `model_type` | 1 | 종합 시황/공시(제목) [국내주식-141] | `/uapi/domestic-stock/v1/quotations/news-title` |
| `fee465d1-7fd5-4c66-b4a4-731b813d569d` | `model_type` | 1 | 관심종목(멀티종목) 시세조회 [국내주식-205] | `/uapi/domestic-stock/v1/quotations/intstock-multprice` |
| `a08c3421-e50f-4f24-b1fe-64c12f723c77` | `model_validation_exception` | 0 | 국내주식기간별시세(일/주/월/년)[v1_국내주식-016] | `/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice` |

### 11.2 필드 단위 상세

| id | issue_type | location | message |
| --- | --- | --- | --- |
| `1e375270-7d8d-4e4b-bcac-d11cb41542cb` | `missing` | `output.flng_cls_name` | Field required |
| `1e375270-7d8d-4e4b-bcac-d11cb41542cb` | `missing` | `output.mang_issu_cls_name` | Field required |
| `1e375270-7d8d-4e4b-bcac-d11cb41542cb` | `missing` | `output.mrkt_warn_cls_name` | Field required |
| `1e375270-7d8d-4e4b-bcac-d11cb41542cb` | `missing` | `output.revl_issu_reas_name` | Field required |
| `3acd4025-6e95-46dc-a90d-b38215912d11` | `model_type` | `output` | Input should be a valid dictionary or instance of `MarketTimeOutput` |
| `4a077f43-7053-47be-b811-8e35be4ea745` | `model_type` | `output` | Input should be a valid dictionary or instance of `ForeignInstitutionTotalOutput` |
| `5c488ab2-59fd-486e-bf74-b68e813e35c0` | `model_type` | `output` | Input should be a valid dictionary or instance of `ChkHolidayOutput` |
| `636e216a-f3bb-4dc6-8bc3-e6d9babca5f1` | `model_type` | `output1` | Input should be a valid dictionary or instance of `HtsTopViewOutput1` |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc10` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc4` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc5` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc6` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc7` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc8` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_askp_icdc9` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc10` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc4` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc5` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc6` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc7` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc8` | Field required |
| `6b0b388e-f815-4009-b46d-e08e47575ca7` | `missing` | `output1.ovtm_untp_bidp_icdc9` | Field required |
| `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` | `missing` | `output1.kospi200_prdy_ctrt` | Field required |
| `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` | `missing` | `output1.kospi200_prdy_vrss` | Field required |
| `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` | `missing` | `output1.kospi200_prdy_vrss_sign` | Field required |
| `7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a` | `model_type` | `output` | Input should be a valid dictionary or instance of `InquireDailyPriceOutput` |
| `81269474-9c66-404f-bdfe-4bb472975330` | `missing` | `output1.hts_kor_isnm` | Field required |
| `81269474-9c66-404f-bdfe-4bb472975330` | `missing` | `output1.stck_shrn_iscd` | Field required |
| `86194480-c8f0-4b0b-9d3d-001c2fc33422` | `missing` | `output1.kospi200_prdy_ctrt` | Field required |
| `86194480-c8f0-4b0b-9d3d-001c2fc33422` | `missing` | `output1.kospi200_prdy_vrss` | Field required |
| `86194480-c8f0-4b0b-9d3d-001c2fc33422` | `missing` | `output1.kospi200_prdy_vrss_sign` | Field required |
| `a08c3421-e50f-4f24-b1fe-64c12f723c77` | `model_validation_exception` | `-` | `FlngClsCodeEnum` 미정의로 `model_rebuild()` 전 class-not-fully-defined 발생 |
| `a274b685-7ea8-441d-a2fe-3087becb6bf2` | `missing` | `output.hts_kor_isnm` | Field required |
| `a274b685-7ea8-441d-a2fe-3087becb6bf2` | `missing` | `output.prdy_vrss_sign` | Field required |
| `a274b685-7ea8-441d-a2fe-3087becb6bf2` | `missing` | `output.stnd_iscd` | Field required |
| `ca2e71e1-5ef4-4489-b4c4-118e10588690` | `model_type` | `output` | Input should be a valid dictionary or instance of `CompareStocksOutput` |
| `e53eb2e6-b292-4e2b-b150-22d92b401453` | `missing` | `output.mbcr_name` | Field required |
| `e53eb2e6-b292-4e2b-b150-22d92b401453` | `missing` | `output.nmix_ctrt` | Field required |
| `e5c6c050-e63f-4ab7-b339-d1a645d3239b` | `model_type` | `output` | Input should be a valid dictionary or instance of `InquireInvestorTimeByMarketOutput` |
| `e5f413ec-3e68-47d7-931f-d7eb263990d9` | `missing` | `output1.prdy_vrss_sign` | Field required |
| `fbfe7300-7096-4938-840b-9f7c328cc5fd` | `model_type` | `output` | Input should be a valid dictionary or instance of `NewsTitleOutput` |
| `fee465d1-7fd5-4c66-b4a4-731b813d569d` | `model_type` | `output` | Input should be a valid dictionary or instance of `IntstockMultpriceOutput` |

## 12) 모델타입 override 반영 결과 (2026-02-13)

- 사용자 승인(1번 요청)에 따라 `model_type` 9건을 `docs/overrides/type_overrides.yaml`에 반영
  - 변경: `changes.output_kinds` (`output`/`output1` → `array`)
  - endpoint:
    - `3acd4025-6e95-46dc-a90d-b38215912d11`
    - `4a077f43-7053-47be-b811-8e35be4ea745`
    - `5c488ab2-59fd-486e-bf74-b68e813e35c0`
    - `636e216a-f3bb-4dc6-8bc3-e6d9babca5f1`
    - `7d6d8ba7-bcae-4d7c-8d5b-4b51cd42a94a`
    - `ca2e71e1-5ef4-4489-b4c4-118e10588690`
    - `e5c6c050-e63f-4ab7-b339-d1a645d3239b`
    - `fbfe7300-7096-4938-840b-9f7c328cc5fd`
    - `fee465d1-7fd5-4c66-b4a4-731b813d569d`
- 후속 조정:
  - `fbfe7300...`(`news_lrdv_code`) smoke enum 에러 재발 방지를 위해 enum 확장(`I11`, `E03`, `I13`, `I06`, `P10`) 반영

## 13) missing 8건 수동 검토 결과 (2026-02-13)

- 산출물: `tmp/docs/reports/missing_manual_review_2026-02-13.json`
- 검토 방식:
  - 각 endpoint를 baseline + 대체 파라미터로 실호출
  - `rt_cd/msg_cd`와 missing 필드 잔존 여부 비교

### 13.1 endpoint별 판정

- `1e375270-7d8d-4e4b-bcac-d11cb41542cb` (`inquire-overtime-price`)
  - 테스트: `005930`, `000660`, `035420`
  - 결과: 모두 `rt_cd=0`, missing 4개 고정
  - 판정: 문서 required 과도(조건부 필드) 가능성 높음

- `6b0b388e-f815-4009-b46d-e08e47575ca7` (`inquire-overtime-asking-price`)
  - 테스트: `005930`, `000660`, `035420`
  - 결과: 모두 `rt_cd=0`, missing 14개 고정
  - 판정: 문서 required 과도 가능성 높음(4~10 호가증감 필드 조건부/미제공)

- `77de2a74-b26c-40ca-a5b7-f87e2ef64f9f` (`inquire-daily-fuopchartprice`)
  - 테스트: baseline, 날짜 최신화
  - 결과: `rt_cd=0`, missing 3개 고정
  - 판정: 문서 required 과도 가능성 높음

- `86194480-c8f0-4b0b-9d3d-001c2fc33422` (`inquire-time-fuopchartprice`)
  - 테스트: baseline, 날짜 최신화
  - 결과: `rt_cd=0`, missing 3개 고정
  - 판정: 문서 required 과도 가능성 높음

- `81269474-9c66-404f-bdfe-4bb472975330` (`inquire-time-indexchartprice`)
  - 테스트: `005930`, `100`, `DJI`, `TSLA`
  - 결과: `TSLA`에서 missing 0, 나머지는 missing 2
  - 판정: 파라미터 영향 큼(기본값 `005930`는 부적합). 문서 설명/샘플 보강 필요

- `a274b685-7ea8-441d-a2fe-3087becb6bf2` (`domestic-bond inquire-price`)
  - 테스트:
    - missing 3 유지: `KR6095572D81`, `KR6449111CB8`, `KR2088012A16`, `KR101501D942`, `KR101501D967`
    - missing 0: `KR2033022D33`, `KR103502GA34`, `KR103502GD31`
  - 판정: 파라미터/종목 상태 의존 + 일부 필드 조건부 생략 공존(혼합형)

- `e53eb2e6-b292-4e2b-b150-22d92b401453` (`etfetn inquire-price`)
  - 테스트: `005930`, `069500`, `102110`
  - 결과:
    - `005930` missing 2 (`nmix_ctrt`, `mbcr_name`)
    - ETF 코드(`069500`, `102110`) missing 1 (`nmix_ctrt`)
  - 판정: 파라미터 영향 + 문서 required 과도(`nmix_ctrt`) 혼합형

- `e5f413ec-3e68-47d7-931f-d7eb263990d9` (`elw lp-trade-trend`)
  - 테스트: `57K281`, `58L002`, `58L003`
  - 결과:
    - baseline `57K281`: missing 1 (`prdy_vrss_sign`)
    - `58L002`: missing 0
    - `58L003`: HTTP 500 (재시도 필요)
  - 판정: 파라미터(종목코드 신선도/유효성) 영향

### 13.2 종합 결론

- **문서 required 과도 우세**: `1e375...`, `6b0b...`, `77de...`, `861944...`
- **파라미터 영향 우세**: `812694...`, `e5f413...`
- **혼합형(파라미터 + 문서)**: `a274...`, `e53...`

## 14) 3번(a08 class-not-fully-defined) 재확인

- 대상: `a08c3421-e50f-4f24-b1fe-64c12f723c77`
- 재검증:
  - 저장 payload 직접 검증: `InquireDailyItemchartpriceResponse.model_validate(...)` 통과
  - 실호출 검증: `HTTP 200`, `rt_cd=0`, 응답 모델 생성 정상
- 결론:
  - 현재 코드는 실사용 관점에서 문제 없음
  - 해당 이슈는 augment 시점 모델 재구성 타이밍에서만 관측되는 노이즈성 항목

## 15) smoke warnings 26 분류 (2026-02-13)

- 산출물:
  - `tmp/docs/reports/smoke_warning_triage_2026-02-13.json`
  - `tmp/docs/reports/smoke_warning_triage_2026-02-13.md`
- 입력 기준:
  - `tmp/docs/reports/api_report.json` 의 `smoke.warnings`
  - `tmp/docs/reports/smoke_requests.json` 의 `resolution + sentinel_probe`
- 요약:
  - `endpoint_total=22`
  - `warning_total=26`
  - `P0_param_fix=12 endpoints / 14 warnings`
  - `P1_param_tune=5 endpoints / 6 warnings`
  - `P2_keep_warning=5 endpoints / 6 warnings`

### 15.1 P0_param_fix (즉시 파라미터 보정 권장)

- 해외선물/옵션 `SRS_CD` 샘플 노후화/placeholder
  - `1a07c21c-5fca-4d8f-a780-d861a7f80eb8` (`SRS_CD=0`)
  - `3d3ad086-7c1b-41cb-9b76-ba05ccf6ba95` (`SRS_CD=CNHU24`)
  - `f9f83090-60d0-4dcf-99c9-a4b36852848e` (`SRS_CD=CNHU24`)
  - `621bdd34-a902-4117-98b8-57733197742a` (`SRS_CD=OESU24 C5500`)
  - `89c2f9ea-62be-4c4a-bd07-66f3fe3234a6` (`SRS_CD=OESU24 C5500`)
  - 조치: mst(`ffcode/focode/fostkcode`) 기반으로 “현재 유효 종목코드”를 자동 선별해 주입
- 해외주식 `EXCD-SYMB` 불일치
  - `3eeac674-072d-4674-a5a7-f0ed01194a81` (`EXCD=HKS`, `SYMB=AAPL`)
  - `abc66a03-8103-4f6d-8ba8-450c2b935e14` (`EXCD=HKS`, `SYMB=AAPL`)
  - `852d7e45-4f34-418b-b6a1-a4552bbcdf90` (`EXCD=NYS`, `SYMB=AAPL`)
  - `ed60877a-6183-433a-9a8c-ef56ed9bc679` (`EXCD=NYS`, `SYMB=TSLA`)
  - 조치: 심볼-거래소 매핑 테이블 기반으로 `EXCD` 교정(미국 예시: `NAS + AAPL/TSLA`)
- 의미 없는 enum default/placeholder
  - `da63a88a-e288-426f-9498-42db0b537bf3` (`FID_INPUT_ISCD=100`)
  - `e5c6c050-e63f-4ab7-b339-d1a645d3239b` (`fid_input_iscd_2=iscd`)
  - `ade0f812-3677-48c0-9cce-ddfb4a689add` (`fid_input_iscd=005930` on ETF/ETN NAV endpoint)
  - 조치:
    - `e5c6...`: 문서 조합 준수(`ETF -> T000` 등)
    - `ade0...`: ETF/ETN 코드 사용(예: `069500`)
    - `da63...`: 해외지수 마스터 코드로 치환

### 15.2 P1_param_tune (튜닝 후 재검증)

- ELW 종목코드 신선도 영향
  - `07313e08-45f2-4423-abb2-2a49752910ae` (`FID_INPUT_ISCD=57K281`)
  - `4af6e358-255c-4e4e-b691-388610068216` (`FID_INPUT_ISCD=57K281`)
  - `31081a30-ba59-4b42-a9f2-c1fe850fadb1` (`FID_INPUT_ISCD=57JS61`)
  - 조치: 활성 ELW 코드(최근 체결/마스터 기준)로 교체
- 데이터 커버리지/윈도우 튜닝
  - `99ac7df4-132a-4458-8b07-4dab240d9896` (당일 단일 날짜 범위)
  - `fbb4bb45-57bb-4037-905d-dff0ff635cf6` (추정실적 커버리지 종목 편향)
  - 조치:
    - 배당일정: 기간 확대(`F_DT`~`T_DT`)
    - 추정실적: 커버리지 높은 대형주로 샘플 교체

### 15.3 P2_keep_warning (현행 warning 유지)

- `4ea57616-0e63-4f8c-a607-f096f1304183` (시간외 일자별주가)
- `6b0b388e-f815-4009-b46d-e08e47575ca7` (시간외 호가)
- `147e81db-e0d2-40cd-95f5-d8da90c2d998` (ELW 신규상장종목: empty_response)
- `b73a4cdf-402b-4e11-a161-609ea9451835` (해외속보 제목)
- `fbfe7300-7096-4938-840b-9f7c328cc5fd` (국내 뉴스 제목)
- 판단:
  - 시간대/데이터 유무 의존성이 크고, KIS의 성공-빈데이터 관대한 응답 특성이 강함
  - smoke 목적상 warning 유지가 합리적

## 16) P1 파라미터 튜닝 반영 및 재검증 (2026-02-13)

### 16.1 반영한 override (augment_overrides)

- `07313e08-45f2-4423-abb2-2a49752910ae` (ELW 현재가)
  - `FID_INPUT_ISCD: 58L002`
- `4af6e358-255c-4e4e-b691-388610068216` (ELW 투자지표추이 분별)
  - `FID_INPUT_ISCD: 58L002`
- `31081a30-ba59-4b42-a9f2-c1fe850fadb1` (ELW 변동성추이 분별)
  - `FID_INPUT_ISCD: 58L002`
  - `FID_PW_DATA_INCU_YN: N`
- `99ac7df4-132a-4458-8b07-4dab240d9896` (배당일정)
  - `CTS: ''`
  - `GB1: '2'`
  - `F_DT: '20250101'`
  - `T_DT: '20260213'`
  - `SHT_CD: ''`
  - `HIGH_GB: ''`
- `fbb4bb45-57bb-4037-905d-dff0ff635cf6` (종목추정실적)
  - `SHT_CD: '005930'`

### 16.2 실호출 사전 검증(튜닝 후보 검증)

- `07313...`:
  - `58L002/58L003/58L006`은 demo/real 모두 sentinel 미검출
  - 기존 `57K281`은 demo/real 모두 sentinel 유지
- `4af6...`:
  - `FID_HOUR_CLS_CODE` 유효 enum은 `60/180/300/600/1800/3600/7200`
  - `58L002` + `60` + `FID_PW_DATA_INCU_YN=Y|N` 모두 sentinel 미검출
- `31081...`:
  - `FID_HOUR_CLS_CODE` 유효 enum은 `60/180/300/600/1800/3600`
  - `58L002` + `60` + `FID_PW_DATA_INCU_YN=Y|N` 모두 sentinel 미검출
- `99ac...`:
  - `GB1='2', F_DT='20250101', T_DT='20260213'` 조합에서 `rows=100`, sentinel 미검출
  - `T_DT='20261231'` 등 미래 포함 구간은 `divi_pay_dt` null로 모델 검증 오류 빈번
- `fbb4...`:
  - `005930`은 sentinel 미검출
  - 기존 `265520`은 sentinel 유지

### 16.3 파이프라인 재실행 결과 요약

- full API pipeline 재실행 시 augment fingerprint 특성상 전체 endpoint 재검증이 발생함
  - (`overrides` 전체가 fingerprint 입력이어서, 일부 endpoint override 수정도 전 endpoint cache 무효화)
- smoke 경고는 **12 → 5**로 감소
  - 잔여 warning: `147e81db...`(empty_response), `4ea57616...`(demo/real), `6b0b388e...`, `b73a4cdf...`
- 다만 동시점 실데이터 드리프트로 smoke error/validation error가 재노출됨
  - smoke error 3:
    - `fbfe7300...` (`news_lrdv_code` 신규 enum 값 유입)
    - `2549b1c6...`, `40409c43...` (`MINX` 파라미터 서버 요구)
  - validation error 7:
    - `147e81db...`, `4769336b...`, `6bd62480...`, `3871dd9b...`, `ae084fcd...`, `40409c43...`, `fbfe7300...`

### 16.4 품질 게이트

- `ruff check .` 통과
- `.venv/bin/ty check` 통과
- `.venv/bin/python -m pytest -q` 통과 (`89 passed`)

## 17) P0 후속 정리 (2026-02-13, 재실행)

### 17.1 이번 반영 사항

- `docs/overrides/augment_overrides.yaml`
  - `3f2f6823-fcdf-4713-a594-a03c7154096e`: `seq='1'` 고정 (조건검색 결과 조회 안정화)
  - 해외선물옵션 체결추이 4개 endpoint(`8702...`, `8c47...`, `c7be...`, `cd2e...`)는 기존 8자리 날짜값 유지
- `docs/overrides/type_overrides.yaml`
  - `fbfe7300-7096-4938-840b-9f7c328cc5fd`: `news_lrdv_code` enum에 `P03` 추가
  - `cf3b44a4-1864-4cc3-8650-ba4e2dbcbf06`: `output` 모델 kind를 `array`로 고정
  - `ed60877a-6183-433a-9a8c-ef56ed9bc679`: `output2.pbid2~10`, `pask2~10`를 optional 처리
  - `0a0f2b43-8a3f-44a4-80b7-f8cf4d6e2f37`: `output1` 모델 kind를 `array`로 고정
- `src/codegen/api/runtime.py`
  - 해외선물옵션 체결추이 4개 endpoint의 `OPSQ2001/START_DATE_TIME[14]`를 endpoint 한정 `nonfatal_server_error`로 분류하는 헬퍼 추가
- `src/codegen/api/steps/smoke.py`
  - `KisResponseError` 처리 시 `nonfatal_server_error`를 warning(skip)로 처리
- `src/codegen/api/steps/infer.py`
  - `validate_samples()`에서 동일 `nonfatal_server_error`를 skipped 처리

### 17.2 최종 재실행 결과

- API pipeline: 정상 종료 (exit 0)
- `tmp/docs/reports/validation.json`
  - `total=268`, `errors=0`
- `tmp/docs/reports/smoke.json`
  - `total=287`, `errors=0`, `warnings=83`
  - status 분포: `ok=204`, `skipped=83`

### 17.3 품질 게이트

- `ruff check .` 통과
- `ty check` 통과
- `pytest -q` 통과 (`89 passed in 11.31s`)

## 18) smoke warnings 83 분류(2026-02-14)

### 18.1 집계 요약

- 기준 파일:
  - `tmp/docs/reports/smoke.json`
  - `tmp/docs/reports/smoke_requests.json`
- 전체 skipped(warnings): `83`
  - `not_read_only`: `76`
  - runtime warning triage 대상: `7` rows (`6` endpoints)

### 18.2 triage 결과

- 결과 파일:
  - `tmp/docs/reports/smoke_warning_triage_2026-02-14.json`
  - `tmp/docs/reports/smoke_warning_triage_2026-02-14.md`
- 분류:
  - `keep_warning`: `4` endpoints
    - `3f2f6823-fcdf-4713-a594-a03c7154096e` (`empty_response`, 조건검색 계정상태 의존)
    - `4ea57616-0e63-4f8c-a607-f096f1304183` (`sentinel_success`, 시간외 일자별주가)
    - `6b0b388e-f815-4009-b46d-e08e47575ca7` (`sentinel_success`, 시간외호가)
    - `c7be7c01-6f43-4576-b1fd-84d0102ce4c3` (`nonfatal_server_error`, 서버 비결정성)
  - `reduce_candidate`: `2` endpoints
    - `b73a4cdf-402b-4e11-a161-609ea9451835`
    - `fbfe7300-7096-4938-840b-9f7c328cc5fd`
    - 공통 원인: 핵심 뉴스 필드는 정상인데 `iscd2~10` 등 연결종목 확장필드 공백 비율이 높아 sentinel false-positive 성격

### 18.3 추가 확인 사항

- `fbfe...`는 date/hour 조건 조회 시 `news_lrdv_code='T01'` enum drift가 추가 관측됨
  - 현재 smoke 기본 파라미터에서는 미노출
  - 후속 enum drift 모니터링/보정 필요

## 19) 후속 재실행 결과 (2026-02-14)

### 19.1 이번 반영/확인

- `docs/overrides/augment_overrides.yaml`
  - `01fd59f1-e7f6-4192-8b02-d52e5dd7c8f3` 파라미터를 넓은 기간(`F_DT=20250101`, `T_DT=20260214`)과 빈 `SHT_CD`로 조정하여 sentinel false-positive를 완화
- `tests/unit/test_api_smoke.py`
  - `_build_news_like_payload()` 반환 타입을 `JsonObject`로 명시 캐스팅하여 `ty` 타입 검사 오류 제거

### 19.2 파이프라인 재실행 결과

- 실행: `PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"`
- 결과:
  - `tmp/docs/reports/smoke.json`: `total=287`, `errors=0`, 상태 분포 `ok=205`, `skipped=82`
  - `tmp/docs/reports/validation.json`: `total=268`, `errors=0`, 상태 분포 `ok=191`, `skipped=77`
  - `01fd59f1-e7f6-4192-8b02-d52e5dd7c8f3`는 smoke에서 `ok`로 확인

### 19.3 smoke skipped(운영 이슈/정책성) 분류

- `not_read_only`: `76` (쓰기/비안전 endpoint 정책 skip)
- `sentinel_success`: `3`
  - `4ea57616-0e63-4f8c-a607-f096f1304183` (demo/real)
  - `6b0b388e-f815-4009-b46d-e08e47575ca7` (real)
- `nonfatal_server_error`: `2`
  - `3ed0247e-d717-43ed-85e9-51f952844687`
  - `8c473311-ecfd-428f-9ec2-0b574d8592b9`
- `empty_response`: `1`
  - `3f2f6823-fcdf-4713-a594-a03c7154096e`

### 19.4 품질 게이트

- `ruff check .` 통과
- `ty check` 통과
- `pytest -q tests/unit/test_api_smoke.py` 통과 (`5 passed`)

## 20) warning 축소 추가 작업 (2026-02-14)

### 20.1 원인 재확인

- 기존 runtime warning 6건 중:
  - `sentinel_success` 3건 (`4ea57616...` demo/real, `6b0b388e...` real)
  - `empty_response` 1건 (`3f2f6823...`)
  - `nonfatal_server_error` 2건 (`3ed0247e...`, `8c473311...`)

### 20.2 파라미터 탐색 결과

- `3f2f6823-fcdf-4713-a594-a03c7154096e`:
  - `24413e7f...`(조건검색 목록조회) 실호출 결과 `seq=0`이 유효
  - `seq=1`은 빈 응답 경향
- `4ea57616-0e63-4f8c-a607-f096f1304183`, `6b0b388e-f815-4009-b46d-e08e47575ca7`:
  - 종목코드 `005930` 등은 sentinel 검출
  - ETF 코드 `069500`에서 demo/real 모두 sentinel 미검출 확인
- `3ed0247e...`, `8c473311...`:
  - 동일 파라미터에서도 `OPSQ2001 WRONG VALUE SIZE ... [14]`가 간헐적으로 발생
  - 현재는 nonfatal 분류 유지가 안전

### 20.3 반영

- `docs/overrides/augment_overrides.yaml`
  - `3f2f6823...`: `seq: '0'`으로 변경
  - `4ea57616...`: `FID_INPUT_ISCD: '069500'` 추가
  - `6b0b388e...`: `FID_INPUT_ISCD: '069500'` 추가

### 20.4 재실행 결과

- 실행: `PYTHONPATH=src .venv/bin/python -c "from codegen.api.pipeline import run_pipeline; run_pipeline()"`
- `tmp/docs/reports/smoke.json`
  - `total=287`, `errors=0`
  - 상태 분포: `ok=210`, `skipped=77`
  - skipped 사유: `not_read_only=76`, `nonfatal_server_error=1`
  - 잔여 runtime warning endpoint: `3ed0247e-d717-43ed-85e9-51f952844687`
- `tmp/docs/reports/validation.json`
  - `total=268`, `errors=0`
  - 상태 분포: `ok=192`, `skipped=76(unsafe)`

### 20.5 품질 게이트

- `ruff check .` 통과
- `ty check` 통과

## 21) runtime warning 0 달성 (2026-02-14)

### 21.1 로직 보강

- `src/codegen/api/steps/smoke.py`
  - `nonfatal_server_error` 재시도 상한을 `2 -> 4`로 확장
  - 일반 케이스는 기존 `2회` 유지
- `tests/unit/test_api_smoke.py`
  - `nonfatal_server_error` 재시도/복구 시나리오 테스트 추가
  - `4회 소진 시 skipped` 시나리오 테스트 추가

### 21.2 파라미터 안정화 (해외선물 체결추이)

- `docs/overrides/augment_overrides.yaml`
  - `8702dab4-008d-4849-8f24-a91b57872a80`
  - `8c473311-ecfd-428f-9ec2-0b574d8592b9`
  - `c7be7c01-6f43-4576-b1fd-84d0102ce4c3`
  - `cd2e4d9a-7e3d-44ff-9b68-36d971655c24`
  - 공통 변경: `START_DATE_TIME: ''` (공백)
- 수동 실호출 확인:
  - 위 4개 endpoint 모두 `START_DATE_TIME=''`에서 `rt_cd=0` 재현
  - 기존 `START_DATE_TIME='20240324'`는 `OPSQ2001 WRONG VALUE SIZE [START_DATE_TIME]:[14]` 빈발

### 21.3 최종 재실행 결과

- 실행 시각(UTC): `2026-02-14T03:02:06.654003+00:00`
- `tmp/docs/reports/smoke.json`
  - `total=287`, `errors=0`
  - 상태 분포: `ok=211`, `skipped=76`
  - skipped 사유: `not_read_only=76` (runtime warning 0)
- `tmp/docs/reports/validation.json`
  - `total=268`, `errors=0`
  - 상태 분포: `ok=192`, `skipped=76(unsafe)`

### 21.4 품질 게이트

- `pytest -q tests/unit/test_api_smoke.py` 통과 (`7 passed`)
- `ruff check .` 통과
- `ty check` 통과

### 21.5 triage 문서 갱신

- `tmp/docs/reports/smoke_warning_triage_2026-02-14.md` 최신 수치 기준으로 갱신
- `tmp/docs/reports/smoke_warning_triage_2026-02-14.json` 신규 생성

## 22) augment transport error 잔여 1건 해소 (2026-02-14)

### 22.1 원인

- `augment`의 성공 시나리오는 본 요청 성공 후 `_probe_error()`를 추가 호출함.
- 이 probe 요청은 보조 수집(에러 형태 확인) 용도인데, 네트워크 전송 오류가 나면 전체 endpoint를 `error`로 처리하던 구조였음.
- 실제 잔여 에러(`3b0af8ef-13b4-4514-a07a-1bc718d07005`)는 `request transport error` 1건으로 관측.

### 22.2 코드 수정

- `src/codegen/api/steps/augment.py`
  - `_probe_error()` 호출을 `try/except`로 감싸서 전송오류를 warning으로만 기록하고 본 성공 결과는 유지하도록 변경.
- `tests/unit/test_api_augment.py`
  - probe 단계에서 `KisTransportError`가 발생해도 `augment_endpoint()`가 `ok`로 종료되는 단위 테스트 추가.

### 22.3 검증 결과

- 단위 테스트:
  - `pytest -q tests/unit/test_api_augment.py tests/unit/test_api_smoke.py` 통과 (`9 passed`)
- 품질 게이트:
  - `ruff check .` 통과
  - `ty check` 통과
- 전체 파이프라인 재실행:
  - `tmp/docs/reports/summary.json` (timestamp: `2026-02-14T03:29:04.674016+00:00`)
  - `augment`: `errors=0`
  - `validation`: `errors=0`
  - `smoke`: `errors=0`

## 23) enum override 후보 리포트 노이즈 제거 (2026-02-20)

### 23.1 배경

- `docs/overrides/type_overrides.yaml`에 이미 반영된 enum 확장(ready 3건)이 `type_override_candidates_enum_priority.json`에 계속 `ready`로 재노출됨.
- 원인은 enum 후보 산출 단계가 기존 `type_overrides`를 고려하지 않고 `enum_drift_candidates`만 기준으로 draft를 만들던 구조였음.

### 23.2 코드 변경

- `src/codegen/api/steps/override_candidates.py`
  - 기존 override에 이미 포함된 `unknown_values`를 후보에서 제외하는 필터 추가.
  - summary에 `covered_by_existing_overrides`, `pending_candidates` 집계 추가.
- `src/codegen/api/pipeline.py`
  - enum 후보 생성 시 `applied_overrides=type_overrides` 전달.
- `tests/unit/test_api_override_candidates.py`
  - 기존 override로 커버된 enum drift가 draft에서 제외되는 단위 테스트 추가.

### 23.3 검증 결과

- 단위/전체 테스트
  - `pytest -q tests/unit/test_api_override_candidates.py` 통과 (`3 passed`)
  - `pytest -q` 통과 (`95 passed`)
- 품질 게이트
  - `ruff check .` 통과
  - `ty check` 통과
- 전체 파이프라인 재실행
  - `tmp/docs/reports/summary.json` timestamp: `2026-02-20T04:38:31.738091+00:00`
  - `smoke errors=0`, `validation errors=0`, `augment errors=0`
  - `type_override_candidates_enum_priority.json`: `ready_overrides 3 -> 0`, `hold_overrides 5`
  - `type_override_candidates_enum.json` summary:
    - `covered_by_existing_overrides=3`
    - `pending_candidates=15`
    - `draft_overrides=5`

## 24) hold 5건 정리 및 enum 오탐 축소 (2026-02-20)

### 24.1 목표

- `type_override_candidates_enum_priority.json`의 `hold_overrides=5`를 항목별로 분해해,
  - 오탐(파서/추론 불일치) 후보 제거
  - 실제 override 검토 필요 후보만 남기도록 정리

### 24.2 코드 변경

- `src/codegen/api/steps/enum_candidates.py`
  - enum drift 후보 생성 시 `decision.kind == "enum"`인 필드만 대상으로 제한.
  - 효과: `decision.kind`가 `time`, `decimal`인 필드에서 enum 설명 파편으로 생기던 drift 제거.
- `src/codegen/core/enums.py`
  - `label:code` 형태(예: `KRX : J`) 파싱 보강.
  - 다만 `code:label`(예: `J: KRX`)은 역전 파싱하지 않도록 휴리스틱 추가.
  - 한글 라벨 + 장문 값(예: `공백: KOSPI200`)은 코드로 오인하지 않도록 보호.

### 24.3 테스트

- `tests/unit/test_api_enum_candidates.py`
  - enum candidate 생성이 `decision.kind=enum`일 때만 동작하는 회귀 테스트 추가.
- `tests/unit/test_core_enums.py`
  - `label:code` 파싱 케이스 추가 (`KRX:J`, `NXT:NX`, `통합:UN`).
  - `code:label` 비역전 케이스 추가 (`J:KRX`, `NX:NXT`, `UN:통합`).
  - 한글 라벨 + 장문 값 오인 방지 케이스 추가 (`공백:KOSPI200`).

### 24.4 검증 결과

- 단위 테스트
  - `pytest -q tests/unit/test_core_enums.py tests/unit/test_api_enum_candidates.py tests/unit/test_api_override_candidates.py` 통과 (`11 passed`)
- 품질 게이트
  - `ruff check` 통과
  - `ty check` 통과
- 파이프라인 재실행 결과
  - `tmp/docs/reports/type_override_candidates_enum_priority.json`
    - `total_overrides=0`, `ready_overrides=0`, `hold_overrides=0`
  - `tmp/docs/reports/type_override_candidates_enum.json`
    - `total_candidates=3`, `covered_by_existing_overrides=3`, `pending_candidates=0`, `draft_overrides=0`
  - `tmp/docs/reports/summary.json` (`2026-02-20T05:01:51.741249+00:00`)
    - `validation errors=0`
    - `smoke errors=1` (잔여: `fbfe7300-7096-4938-840b-9f7c328cc5fd`, `news_lrdv_code` 실응답 신규 enum 값 `T02`, `I02` 미포함)

## 25) enum 파서 오염 후보 13건 해소 (2026-02-20)

### 25.1 배경

- `manual_enum_review_candidates.json`에서 13개 필드가 `parser_fix`로 분류됨.
- 공통 원인은 설명 문구의 메타/참조 토큰(`Type`, `Length`, `Header`, URL 조각, 예시 문구 등)이 enum 코드로 오인되는 현상이었음.

### 25.2 코드 변경

- `src/codegen/core/enums.py`
  - 메타 토큰 차단(`header`, `type`, `length`, `default`, `id`, `code`, `odno`, `fghin` 등).
  - enum 코드 형태 검증 강화(대문자/숫자, 소문자+숫자 패턴, 1글자 소문자만 허용).
  - colonless 파싱에서 URL 분해 오탐이 나던 `/` 분리 제거 및 안내문(조회/입력/api 등) 라인 제외.
- `src/codegen/api/steps/infer.py`
  - 필드 길이(`length`)를 기준으로 설명 유래 enum 값 필터링 추가.
- `src/codegen/api/steps/manual_candidates.py`
  - `d11`, `a10` 같은 `소문자+숫자` 패턴은 오탐으로 보지 않도록 lowercase suspicious 규칙 보정.

### 25.3 테스트

- `tests/unit/test_core_enums.py`
  - 메타 토큰/안내문/collapsed token(`FGHIN`) 오탐 방지 회귀 테스트 추가.
- `tests/unit/test_api_enum_candidates.py`
  - 필드 길이 초과 토큰이 infer enum으로 승격되지 않는 테스트 추가.
- `tests/unit/test_api_manual_candidates.py`
  - 소문자 prefix enum(`d`, `a`, `d11`, `a10`)이 manual suspicious로 분류되지 않는 테스트 추가.

### 25.4 검증 결과

- 단위 테스트:
  - `pytest -q tests/unit/test_core_enums.py tests/unit/test_api_enum_candidates.py tests/unit/test_api_manual_candidates.py tests/unit/test_store_type_infer.py::test_infer_enum_ignores_example_list` 통과 (`18 passed`)
- 품질 게이트:
  - `ruff check .` 통과
  - `ty check` 통과
  - `pytest -q` 통과 (`106 passed`)
- 파이프라인 재실행:
  - `tmp/docs/reports/manual_enum_review_candidates.json`: `total_fields=0`, `endpoints=0`
  - `tmp/docs/reports/manual_enum_review_priority.json`: `parser_fix_fields=0`, `override_review_fields=0`
  - `tmp/docs/reports/summary.json`: `smoke.errors=0`, `validation.errors=0`, `augment.errors=0`

### 25.5 후속 안정화 (2026-02-20)

- `src/codegen/api/steps/infer.py`
  - `0/1` 문서 enum + 다자리 `0/1` 샘플(`111111111`) 패턴을 `binary_mask_code`로 분리해 `str`로 추론.
  - 효과: request 비트마스크 필드가 enum drift hold로 남지 않음.
- `docs/overrides/augment_overrides.yaml`
  - `fbfe7300-7096-4938-840b-9f7c328cc5fd`에 `FID_NEWS_OFER_ENTP_CODE='2'`를 지정해 `news-title` smoke 응답 변동성 완화.

- 최종 재검증:
  - `tmp/docs/reports/summary.json` timestamp: `2026-02-20T06:17:24.184528+00:00`
  - `smoke.errors=0`, `validation.errors=0`, `augment.errors=0`
  - `tmp/docs/reports/type_override_candidates_enum_priority.json`: `ready_overrides=0`, `hold_overrides=0`

## 26) scan/normalize 경고 노이즈 축소 (2026-02-20)

### 26.1 배경

- 기존 `scan`/`normalize` 경고의 대부분이 필드 단위 `description.missing`로 누적되어 리포트 가독성이 크게 떨어졌음.
- 기준 수치(이전): `scan.warnings=8277`, `normalize.warnings=8292`.

### 26.2 코드 변경

- `src/codegen/api/steps/validate.py`
  - `request.headers`, `request.params`, `request.body`, `response.body`의 description 누락 경고를 필드별 1건씩이 아니라 **영역별 집계 1건**으로 변경.
  - 메시지에 누락 필드 수와 코드 preview(최대 5개)를 포함하도록 변경.

### 26.3 테스트

- `tests/unit/test_api_validate.py` 신규 추가:
  - 영역별 집계 경고가 1건만 생성되는지 검증.
  - preview가 5개 초과 시 `… (+N)`로 축약되는지 검증.

### 26.4 검증 결과

- 단위 테스트:
  - `pytest -q tests/unit/test_api_validate.py tests/unit/test_core_enums.py tests/unit/test_api_enum_candidates.py tests/unit/test_api_manual_candidates.py` 통과 (`20 passed`)
- 파이프라인 재실행:
  - `tmp/docs/reports/summary.json` timestamp: `2026-02-20T06:27:24.466113+00:00`
  - `scan.warnings: 8277 -> 390`
  - `normalize.warnings: 8292 -> 405`
  - `smoke.errors=0`, `validation.errors=0`, `augment.errors=0` 유지
- 품질 게이트:
  - `ruff check .` 통과
  - `ty check` 통과
  - `pytest -q` 통과 (`108 passed`)
