# 2026-08-28 - Issue #25 배포 전 마이그레이션 재검토 및 버전 체계 재정의

## 사용자 요청

> 정식 배포 전 migration 작업 재검토를 이슈로 등록하여 재검토 착수 하고,
> 이슈 #2 종료(close) 조건 재검토

재검토 결과를 [#25](https://github.com/visualmoney/vm-stock-kis/issues/25)로
등록한 뒤 이어진 지시:

> 마이그레이션 가이드에서 모듈명이 변경되었으며, 정식 버전 명을 v3.0.0 태그에서
> v0.0.1 태그로 변경하고 #25 작업에 포함 시킴. (…) v0.0.1은 오리지널 버전
> v2.1.6에서 파생한 버전이나 버전 숫자가 2.1.6보다 클 이유는 없음.

> pip install vm-stock-kis / 유지, 정식 1차버전 v0.0.1 → 완전삭제 버전 v1.0.0 결정

## 확정 사항

| 항목 | 이전 | 확정 |
|---|---|---|
| PyPI 배포명 | `vm-stock-kis` | **유지** |
| 1차 정식 버전 | `v3.0.0` | **`v0.0.1`** |
| 호환 shim 완전 삭제 | `v4.0.0` | **`v1.0.0`** |
| `Development Status` | `5 - Production/Stable` | **`4 - Beta`** |

## 분석

- **작업 범위**: 문서 + 배포되는 코드의 경고 문구 + 테스트 단언 + classifier
- **영향 받는 모듈**: `src/vmkis/{__init__,helpers,types}.py`,
  `src/vmkis/utils/workspace.py` (동작 변경 없음, 문자열만)
- **예상 시간**: 3시간

## 계획

1. `pip install vmkis` 11곳 → `vm-stock-kis`
2. 버전 재번호 (`v3.0.0`→`0.0.1`, `v4.0.0`→`1.0.0`) — 코드·테스트·문서
3. `MIGRATION_GUIDE.md` 재작성 (부분 수정으로는 해결 불가)
4. `API_STABILITY_POLICY.md`의 가공된 릴리스 이력 정리
5. classifier 조정 및 근거 주석
6. 검증 → 개발 일지 → PR

## 결과

완료. 상세는 [개발 일지](../dev_logs/2026-08-28_issue25_migration_review.md) 참조.

계획에 없었으나 작업 중 추가로 발견해 고친 것:

- `SimpleKIS(config_path=...)` — 실제 생성자는 `VmKis` 인스턴스를 받는다
- `MarketInfo`의 실제 타입은 `KisMarketInfo`가 아니라 `KisMarketType`
- 공개 API 개수 "20개" → 실제 `__all__`은 12개
- `Python KIS`(하이픈 없는 표기) 5곳 — 문서 4개의 H1 제목 포함
