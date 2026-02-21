---
status: accepted
date: 2026-02-20
---

# ADR-012: L1+L2 통합 → Service Layer (2-Layer Architecture)

## Context

v2 분석 결과, 국내/해외 API 간의 갭은 단순 필드 매핑(L1 Normalize)으로 해소되지 않음. 절차적 서비스 로직이 필요:

- **Multi-call 조합**: 해외 분봉 차트 최대 12회 호출 + 중복 제거
- **Request→Response 전사**: 잔고 조회 시 request 데이터를 response에 주입
- **조건부 라우팅**: exchange.is_domestic에 따라 완전히 다른 엔드포인트/로직
- **Computed properties**: 수익률, 변동률 등 파생 필드

기존 3-layer (L0 Raw → L1 Normalize → L2 System) 구조에서 L1과 L2의 경계가 모호하고, 선언적 YAML 매핑만으로는 위 요구사항을 충족할 수 없었음.

## Decision

L1(Normalize) + L2(System)을 **L1 Service**로 통합한다.

```
L0 Raw (generated) → L1 Service (hand-written) → Public API
```

### Service Layer 구성

**A. Type System (YAML)** — 모델 스키마, enum 정의, 필드 메타데이터
- Location: `data/service/`
- 역할: "what" — 모델이 무엇인지 선언

**B. Service Modules (Python)** — 매핑, 오케스트레이션, enrichment
- Location: `src/pykis/service/`
- 역할: "how" — 어떻게 변환하는지 구현
- 패턴: Protocol-based mapper (L0 모델과 디커플링)

### Drift Detection

L0 변동 시 L1 정합성 유지를 위한 시그니처 기반 감지:
- `scripts/check_l0_drift.py` — 구조적 해시 비교
- `data/service/_l0_manifest.yaml` — 기준 매니페스트
- Pre-commit hook으로 커밋 게이트

## Consequences

- 단일 레이어로 변환 복잡도 집중 → 코드 탐색 용이
- 선언적 매핑과 절차적 로직의 명확한 분리 (YAML vs Python)
- Protocol 기반 매퍼로 L0 생성 코드와의 디커플링 유지
- Drift detection으로 L0 변경 시 영향 범위 자동 감지
- `/service-build` agent skill로 도메인 추가 워크플로우 표준화
