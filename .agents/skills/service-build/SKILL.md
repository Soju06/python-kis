# /service-build

L1 Service 모듈 구축을 가이드하는 인터랙티브 스킬.

## Description

새로운 서비스 도메인(quote, chart, order, balance 등)을 L0 Raw 엔드포인트로부터 L1 Service 모듈로 구축합니다. Domain Analysis → Design → Implementation → Test → Record의 5-phase 워크플로우를 따릅니다.

## Arguments

- `<domain>` — 구축할 도메인 이름 (e.g., `chart`, `order`, `balance`)
- `--review-drift` — 현재 L0 drift 상태를 리뷰하고 영향받는 서비스 모듈 분석

## Workflow

### Phase 0: Domain Analysis

1. 대상 도메인의 L0 엔드포인트 스캔 (국내/해외)
   ```bash
   # Registry에서 관련 엔드포인트 검색
   PYTHONPATH=src .venv/bin/python -c "
   from pykis.api.raw import ensure_registry
   for eid, ep in ensure_registry().items():
       if '<keyword>' in ep.name.lower() or '<keyword>' in ep.path:
           print(f'{eid}: {ep.name} ({ep.path})')
   "
   ```

2. 필드 메타데이터 수집 (이름, 타입, 한글 설명, enum 코드)
   - L0 모델 파일 읽기: `src/pykis/api/raw/국내주식/`, `src/pykis/api/raw/해외주식/`
   - Request/Response 모델 필드 목록 추출

3. 국내↔해외 대응 엔드포인트 매칭
   - 동일 기능의 국내/해외 API 쌍 식별
   - 필드 대응 관계 분석

4. v2 참조 코드 분석
   - `python-kis-v2/pykis/api/stock/` — 해당 도메인 기존 구현
   - `python-kis-v2/pykis/adapter/product/` — 어댑터 패턴

5. **출력**: 도메인 분석 리포트 (사용자에게 제시)

### Phase 1: Design (HITL)

1. 통합 모델 제안
   - 필드 목록: 영문 이름, 타입 (Decimal/int/str/bool/enum), 출처 (국내 필드, 해외 필드)
   - `@dataclass(frozen=True, slots=True)` 패턴

2. 통합 enum 제안
   - L0 코드 ↔ 서비스 enum 매핑 테이블
   - `data/service/_enums.yaml` 확장

3. 서비스 함수 시그니처 제안
   - `async def get_<domain>(client, ...) -> <Model>`
   - 라우팅 전략 (exchange.is_domestic)

4. Multi-call / enrichment 요구사항 식별
   - 페이지네이션 필요 여부
   - 여러 엔드포인트 조합 필요 여부
   - request→response 전사 필요 여부

5. **HITL**: 사용자 리뷰 → 설계 확정

### Phase 2: Implementation

1. YAML 모델 스키마 작성
   ```
   data/service/<domain>.yaml
   ```

2. Enum 정의 + 매핑 테이블 확장
   - `src/pykis/service/enums.py` 확장 (필요 시)
   - `src/pykis/service/_enum_map.py` 확장

3. Service module Python 코드 작성
   ```
   src/pykis/service/<domain>/
       __init__.py
       models.py        # frozen dataclass
       service.py       # 오케스트레이션 (async + sync)
       _domestic.py     # 국내 매퍼 (Protocol 기반)
       _overseas.py     # 해외 매퍼 (Protocol 기반)
   ```

4. L0 manifest consumer 등록
   ```bash
   # data/service/_l0_manifest.yaml에서 해당 엔드포인트의 consumers에 도메인 추가
   ```

5. **HITL**: 코드 리뷰

### Phase 3: Test & Verify

1. 테스트 작성
   ```
   tests/unit/test_service_<domain>.py
   ```
   - Mock L0 output 데이터클래스 (Protocol 만족)
   - 국내/해외 매핑 각각 테스트
   - Enum 변환 테스트
   - Frozen/immutable 검증

2. 품질 게이트
   ```bash
   .venv/bin/ruff check src/pykis/service/ tests/unit/test_service_*.py
   .venv/bin/ty check src/pykis/service/
   .venv/bin/python -m pytest tests/unit/test_service_*.py -v
   .venv/bin/python -m pytest -q  # 전체 테스트 회귀 확인
   ```

3. Drift 검증
   ```bash
   PYTHONPATH=src .venv/bin/python scripts/check_l0_drift.py
   ```

4. **HITL**: 최종 승인

### Phase 4: Record

1. `context.md` 업데이트
   - Active Work 섹션에 완료 기록
   - test 카운트 업데이트

2. 도메인 완료 기록

## Drift Review Mode

`/service-build --review-drift` 실행 시:

1. drift 스크립트 실행
   ```bash
   PYTHONPATH=src .venv/bin/python scripts/check_l0_drift.py
   ```

2. 변경된 엔드포인트 분석
   - 필드 추가 → 서비스 모델에 반영 필요?
   - 필드 제거 → 매퍼 코드 컴파일 에러 감지
   - 타입 변경 → 변환 로직 수정 필요?
   - Enum 변경 → enum_map 업데이트 필요?

3. 수정 제안 → HITL 승인

4. manifest 갱신
   ```bash
   PYTHONPATH=src .venv/bin/python scripts/check_l0_drift.py --update
   ```

## Patterns Reference

- **Frozen dataclass**: `@dataclass(frozen=True, slots=True)` — see `src/pykis/streaming/normalize/models.py`
- **Protocol-based mapper**: see `src/pykis/streaming/normalize/mapper.py`
- **Service function**: see `src/pykis/service/quote/service.py`
- **L0 endpoint access**: `ensure_registry()[<uuid>]`
- **Enum mapping**: see `src/pykis/service/_enum_map.py`
- **Conversion helpers**: see `src/pykis/service/_convert.py`

## Output

```
Service Module: <domain>
- Models: src/pykis/service/<domain>/models.py
- Service: src/pykis/service/<domain>/service.py
- Tests: tests/unit/test_service_<domain>.py (N passed)
- Drift: ✅ manifest updated
- Quality: ruff ✅ ty ✅ pytest ✅
```
