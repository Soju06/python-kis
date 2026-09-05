# 2026-08-27 - open-trading-api 대비 아키텍처 비교 분석 개발 일지

## 작업 내용

한국투자증권 공식 샘플 저장소(`../open-trading-api`)와 VM-Stock-KIS를
layered architecture 관점에서 코드 검증 기반으로 비교 분석하고 보고서 작성.

- software-architect 서브에이전트 7인 병렬 분석 (model: fable 5)
- load-bearing 주장 10건은 메인 세션에서 직접 재검증
- 추가 요청 반영: 소스 구조 설명(§3), 단방향 의존 판정(§5),
  클래스 vs 함수 사용 편의성(§8), 하부 레이어 흡수 타당성(§13), fetch 예제 부록(A)
- §12 P1-3에 입문자용 해설 박스 추가 (선언적 스펙 + 범용 실행기 개념 설명)

## 변경 파일

- `docs/prompts/2026-08-27_architecture_comparison_open_trading_api.md` - 프롬프트 원본
- `docs/reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md` - 비교 보고서 (1,978줄, 14장 + 부록 3)
- `docs/dev_logs/2026-08-27_architecture_comparison_devlog.md` - 본 문서

## 주요 발견

1. 커버리지 격차: 공식 377 TR ID vs vmkis 74 TR ID (약 9배). vmkis는 주식 현물만 지원
2. `ARCHITECTURE.md`의 단방향 계층 주장은 반증됨 - 역방향 의존 7건 실재
   (`client/websocket.py:19` → api, `responses/response.py:5-7` → client 등)
3. `VmKis.fetch(api=..., response_type=...)`가 미지원 TR 호출용 1급 escape hatch로
   이미 존재하나 사용자 문서에 미노출
4. `WEBSOCKET_RESPONSES_MAP` 미등록 TR은 구독은 되나 이벤트가 조용히 drop됨
5. 문서-코드 드리프트 7건 발견 (보고서 §11)
6. 역방향 의존 7건 중 필수 수정은 2건뿐 — 나머지는 rich domain object 설계의 필연.
   진짜 문제는 순환 우회 지연 import 30곳에 사유 주석이 0곳이라는 점 (§5)
7. `import vmkis.responses.response` 하나로 모듈 87개 전부 로드됨 (부분 로드 불가, 실측)
8. 공식 저장소에 LICENSE 파일 부재 (upstream 라이선스 필드도 null)
   → 코드 벤더링 불가. 사실 추출 기반 codegen만이 유일한 경로 (§13)
9. `examples_llm/` AST 파싱률 98.9% (REST 274개 중 271개) 실측 증명 (§13)
10. `KisPage`는 `ctx_area_fk100/200`만 지원 — 평문 `CTX_AREA_FK` API(`CTCA0903R`)는
    수동 커서 루프 필요 (부록 A.5에서 실증)
11. 환경 분기 실측: REST TR ID 9곳 / 웹소켓 TR ID 2곳 / 파라미터 값 2곳 /
    `domain="real"` 10곳 (초안의 "28곳" 추정치를 실측값으로 교정)

## 테스트 결과

- 코드 변경 없음 (문서 작업). 테스트 미실행

## 다음 할 일

- [ ] P0: Level 0/1 escape hatch 사용자 문서화 (`docs/user/`)
- [ ] P0: 문서-코드 드리프트 7건 수정 (ARCHITECTURE.md, CLAUDE.md, ARCHITECTURE_QUALITY_KR.md)
- [ ] P1: `client → api` 역참조 해소 (WebSocket 자기등록 데코레이터)
- [ ] P1: 페이지네이션 제네릭 헬퍼 추출
- [ ] P1: `KisPage.__pre_init__`에 `ctx_area_fk`/`fk50` 분기 추가 (4줄)
- [ ] P2: `examples_llm` 기반 codegen 파일럿 8개 엔드포인트 (§13.3 단계 1)
- [ ] 문서: 순환 우회 지연 import 30곳에 사유 주석 + import-linter CI 계약
- [ ] 버그: `kis.py:560-599` 무한 재시도 루프 상한 추가
- [ ] 버그: `KisNotFoundError` 이름 충돌 해소
