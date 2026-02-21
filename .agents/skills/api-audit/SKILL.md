# /api-audit

KIS API 스펙-실응답 정합성 감사 스킬.

## Description

KIS API 문서 스펙과 실제 응답 데이터를 비교하여 불일치를 감지하고, 조치를 제안합니다.

## Arguments

- `[domain]` — 감사 대상 도메인 (optional). 예: `국내주식`, `해외주식`, `선물옵션`
- `[endpoint-id]` — 특정 endpoint UUID (optional)
- 인수 없으면 전체 감사

## Workflow

### Phase 0: Scope Selection

감사 대상 선택:
- 전체: 모든 endpoint
- 도메인별: `data/kis/{domain}/` 하위
- 단일: 특정 endpoint UUID

### Phase 1: Audit

스펙 파일 (`data/kis/`) vs 실응답 캐시 (`tmp/docs/augment/`) 비교.

불일치 패턴 분류:
- `model_type` — output kind 불일치 (문서 single, 실응답 array)
- `missing` — required 필드 조건부 누락
- `sentinel` — sentinel 값 패턴 (빈 문자열, 0, 00000000)
- `enum_drift` — 문서 미등록 enum 값 유입

### Phase 2: Report

감사 결과 요약:

```
API Audit Report
- Scope: [전체 / 도메인 / endpoint]
- Total endpoints audited: N
- Issues found: N
  - model_type: N
  - missing: N
  - sentinel: N
  - enum_drift: N

Recommendations:
- SRS update candidates: N
- Override candidates: N
- Code fix candidates: N
```
