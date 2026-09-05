# Basic Examples

이 폴더는 빠른 시작을 위한 최소 예제들을 제공합니다. 모두 `configs/account_profiles.yaml`
에서 인증 정보를 로드합니다.

## ⚠️ 준비 (중요)

1. 템플릿을 복사하세요. **제자리에서 고치지 마세요** — 템플릿은 추적 대상이라
   채우면 시크릿이 커밋될 수 있습니다.

   ```bash
   cp configs/template_account_profiles.yaml configs/account_profiles.yaml
   ```

2. 값을 채웁니다. **문자열은 전부 따옴표로 감싸세요** — 따옴표가 없으면 YAML 이
   `account_no: 00000000` 을 정수 `0` 으로 바꿉니다.

   ```yaml
   version: 1
   apps:
     app_paper1:
       mode: "paper"              # live | paper — 생략할 수 없습니다
       hts_id: "YOUR_HTS_ID"
       app_key: "YOUR_APP_KEY"    # 36자
       app_secret: "YOUR_SECRET"  # 180자
   accounts:
     acc_paper1:
       app: "app_paper1"
       account_no: "00000000"     # 8자리
       product_code: "01"         # 01 종합 / 22 개인연금 / 29 IRP
   default_account: "acc_paper1"
   ```

3. 계좌 선택 (계좌가 둘 이상일 때)
   - 스크립트 인자: `--account acc_live1`
   - 환경변수: `VMKIS_ACCOUNT=acc_live1`
   - 기본값: 설정의 `default_account`

4. **민감정보 보호**: `configs/` 는 이미 `.gitignore` 에 있습니다. 템플릿만
   추적되고 채운 파일과 토큰(`configs/token/`)은 무시됩니다.

전체 사양은 [docs/guidelines/CONFIG_SCHEMA.md](../../docs/guidelines/CONFIG_SCHEMA.md) 에 있습니다.

## 예제 목록

- `hello_world.py` — 기본 초기화
- `keep_token.py` — `keep_token=True` 로 토큰 저장
- `get_quote.py` — 시세 조회 예제 (삼성전자)
- `get_chart.py` — `stock.chart()` 일봉
- `get_orderbook.py` — `stock.orderbook()`
- `trading_hours.py` — `kis.trading_hours(market)`
- `get_balance.py` — 잔고 조회 예제
- `account_lookups.py` — `profits` · `daily_orders` · `orderable_amount` · `orderable` · `pending_orders`
- `place_order.py` — 시장가 매수 예제 (안전 장치 포함)
- `place_sell.py` — 매도 1주 (안전 장치 포함)
- `modify_cancel_order.py` — 지정가 매수 뒤 정정·취소
- `realtime_price.py` — 실시간 체결가 구독 예제
- `realtime_orderbook.py` — 실시간 호가
- `realtime_execution.py` — 실시간 체결내역

## 실행 방법

```bash
# 모의투자 계정에서 먼저 검증 (권장)
python examples/01_basic/get_quote.py
python examples/01_basic/get_chart.py
python examples/01_basic/get_balance.py
python examples/01_basic/account_lookups.py
python examples/01_basic/place_order.py

# 실시간 예제 (Enter를 눌러 종료)
python examples/01_basic/realtime_price.py
python examples/01_basic/realtime_orderbook.py
```

## 주의사항

- **실계좌 주문**: `ALLOW_LIVE_TRADES=1` 환경변수 필요
- **모의투자 권장**: `mode: "paper"` 로 모의투자에서 먼저 검증하세요
- **`configs/account_profiles.yaml` 보관**: 절대 커밋하지 마세요 (`.gitignore` 에 있습니다)
- **모의 잔고·계좌 조회 (`OPSQ2000`)**: `get_balance.py` · `account_lookups.py` 가
  `KisAPIError` `OPSQ2000` / `INVALID_CHECK_ACNO` 로 끝나면, 장 닫힘이 아니라
  **모의 앱이 그 CANO(계좌번호)를 거부**한 경우가 많습니다. YAML 의
  `account_no`·`product_code` 가 KIS 모의 계좌와 일치하는지 확인하세요.
  `#157` 필수 연기(시세·연결)에는 잔고·계좌가 들어 있지 않습니다 — leftover.
  실측 메모: `docs/dev_logs/2026-09-05_36`–`39_*.md`.
- **실시간 예제**: 종료 시 Enter를 눌러 구독을 해제하세요
