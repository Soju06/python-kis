# 2026-08-27 - open-trading-api 대비 레이어드 아키텍처 비교 분석

## 사용자 요청
>
> read CLAUDE.md, docs/architecture/ARCHITECTURE.md, ../open-api-trading과 layered architecture
> 관점에서 비교를 하고, 장단점을 비교해줘, 이 저장소에서 지원하지 않는 API를 지원하거나
> 추가 하려면 어떻게 해야 하는지, 한국투자증권 공식 API sample과 비교시 장단점을 비교해서
> 보고서로 작성해줘 (docs/reports) 필요하면 아키텍처 관련 다른 문서를 읽어도 되고,
> 코드를 통해서 실제 모습도 확인한다. Plan - software-architect subagent를 사용하고
> model은 fable 5를 사용한다.

## 분석

- 비교 대상: `../open-trading-api` (한국투자증권 공식 GitHub 샘플 저장소)
  - 사용자가 언급한 `../open-api-trading` 은 실제 디렉토리명 `open-trading-api` 로 확인
- 비교 관점: Layered Architecture (계층 분리, 의존 방향, 확장 지점, 결합도)
- 산출물: `docs/reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md`

## 계획

1. vm-stock-kis 실제 코드로 계층 구조 검증 (문서 vs 코드)
2. open-trading-api 구조/코드 스타일/API 커버리지 분석
3. 미지원 API 추가 절차 도출 (기존 API end-to-end 추적)
4. 장단점 비교 및 권장안 보고서 작성

## 추가 요청 (동일 세션)

1. 사용자 관점 클래스 방식 vs 함수 방식 사용 편의성 비교 → §8
2. 주식 현물 `fetch()` 활용 기능 추가 예제를 부록으로 → 부록 A
3. 본문에 소스 구조 설명 추가 → §3
4. 단방향 의존이 아니어도 문제 없는지 판정 → §5
5. 공식 샘플 함수를 하부 레이어로 흡수 가능한지 검토 → §13

## 결과

- 보고서: `docs/reports/2026-08-27_ARCHITECTURE_COMPARISON_OPEN_TRADING_API_KR.md` (1,836줄, 14장 + 부록 3)
- 개발 일지: `docs/dev_logs/2026-08-27_architecture_comparison_devlog.md`
- 핵심: 커버리지는 공식이 9배 우위, 타입/안전성/동시성은 vmkis 우위,
  단방향 계층 주장은 코드로 반증(역방향 의존 7건), 문서 드리프트 7건 발견
