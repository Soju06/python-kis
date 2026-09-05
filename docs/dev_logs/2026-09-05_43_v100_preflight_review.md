# 2026-09-05 — v0.3.0→v1.0.0 전 리뷰 보고서

## 한 줄

SimpleKIS 예제 파일은 가이드·API 정합 전에는 추가하지 않는다. `v1.0.0`은
이미 0.3.0에 들어간 Breaking을 다시 지우는 일이 아니라 major 선언 +
문서 leftover 정리이다. 이슈는 보고서 승인 후.

## 산출

| 경로 | 내용 |
|---|---|
| [`docs/reports/2026-09-05_V030_TO_V100_REVIEW.md`](../reports/2026-09-05_V030_TO_V100_REVIEW.md) | SimpleKIS 판정 + P0–P2 + 이슈 초안 제목 |
| [`docs/INDEX.md`](../INDEX.md) | 읽을 만한 최신 보고서 한 줄 |
| [`docs/prompts/2026-09-05_43_v100_preflight_review.md`](../prompts/2026-09-05_43_v100_preflight_review.md) | 이 단위 |

## SimpleKIS 판정 (보고서 §1)

- `examples/`에 `SimpleKIS` **0건**.
- 가이드 `side=` / `order_id` / `change_rate` / `total_assets` ≠ `simple.py`
  (매수만, `cancel_order(order_obj)`, quote/balance 필드명 불일치).
- 권고: 가이드 축소 또는 API 확장 후, 선택적으로
  `01_basic/simplekis_get_price.py`만 검토. `02`/`03` 부활 없음.

## 1.0.0 갭 요지

| 우선 | 요지 |
|---|---|
| P0 | 문서가 0.3.0 Breaking을 “1.0.0 대기”로 말함 |
| P0 | Stable vs “0.x minor Breaking” · FAQ `<1.0.0` 핀 |
| P0 | `client.exceptions.KisNotFoundError` “1.0.0에서 제거” 별칭 |
| P1 | SIMPLEKIS_GUIDE · paper OPSQ leftover · `next-up` 재대기 |
| P2 | PYPI_RELEASE 예시 · `#104` · `#100` B 재고지 |

## 하지 않은 것

- `examples/` SimpleKIS 파일
- GitHub 이슈 개설 · `next-up` 재대기
- `#33`–`#36` 재작업 · `v1.0.0` 태그
- `configs/` · 주문/웹소켓 실측

## 트랩

- 가이드를 따르는 예제 = 깨진 데모. 코드에 맞춘 예제 = 가이드 모순.
  둘 다 파일 추가 전에 문서를 고친다.
- “1.0.0에서 제거한다”고 쓰여 있어도 코드 제거는 이미 0.3.0에 끝난
  경우가 많다. 남은 별칭과 **문서 시제**를 먼저 본다.
