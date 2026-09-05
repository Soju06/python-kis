# QUICKSTART

1. 설치

```bash
pip install vm-stock-kis
```

1. 인증 정보 준비 (권장: 외부 파일 사용, 리포지토리에 커밋 금지)

템플릿을 복사해 채웁니다. **제자리에서 고치지 마세요** — 템플릿은 추적 대상입니다.

```bash
cp configs/template_account_profiles.yaml configs/account_profiles.yaml
```

`configs/account_profiles.yaml` 예시:

```yaml
version: 1
apps:
  # 실전 앱은 모의투자만 할 때도 필요합니다 — 아래 설명 참고.
  app_live1:
    mode: "live"               # live | paper — 생략할 수 없습니다
    hts_id: "YOUR_HTS_ID"
    app_key: "YOUR_LIVE_KEY"
    app_secret: "YOUR_LIVE_SECRET"
  app_paper1:
    mode: "paper"
    hts_id: "YOUR_HTS_ID"
    app_key: "YOUR_PAPER_KEY"
    app_secret: "YOUR_PAPER_SECRET"
accounts:
  acc_live1:
    app: "app_live1"
    account_no: "00000000"
    product_code: "01"
  acc_paper1:
    app: "app_paper1"
    account_no: "00000000"
    product_code: "01"
default_account: "acc_paper1"   # 실수로 실전에 붙지 않도록 모의를 기본으로
```

> **실전 앱이 왜 필요한가**: 시세 TR 이 모의도메인에 없습니다. 모의 계좌로
> 시세를 조회해도 요청은 실전 도메인으로 나가고, 그때 실전 앱키를 씁니다.
> 모의 앱만 적으면 `create_client()` 가 무엇을 추가해야 하는지 알려주며
> 멈춥니다. ([#87](https://github.com/visualmoney/vm-stock-kis/issues/87))

**문자열은 전부 따옴표로 감싸세요.** 따옴표가 없으면 YAML 이 `account_no: 00000000`
을 정수 `0` 으로 바꿉니다.

1. 코드 예시

```python
from vmkis import create_client

kis = create_client()          # 기본 configs/account_profiles.yaml
print(kis.stock("005930").quote())
```

토큰은 설정 파일 옆(`configs/token/`)에 앱 이름으로 저장됩니다. 경로를 직접 적을
필요가 없습니다.

1. 테스트 팁

- 테스트에서는 `tmp_path`에 임시 설정 파일을 만들고 `create_client(path)` 로 넘기세요.

---

1. 다음 단계

- 예제 실행: `examples/01_basic/` 폴더의 스크립트를 그대로 실행해보세요.
- README 살펴보기: 루트 `README.md`에 설치/주문/실시간 예제가 더 있습니다.
- 설정 분리: 실계좌 주문 전 `mode: "paper"` 로 모의투자에서 먼저 검증하세요.

1. 트러블슈팅

- `FileNotFoundError`: `configs/account_profiles.yaml` 이 있는지 확인하세요. 템플릿에서 복사하지 않았을 수 있습니다.
- `version 이 없습니다`: 0.0.x 형식 파일입니다. 하위 호환을 지원하지 않으므로 템플릿을 보고 다시 작성하세요.
- 한글 깨짐: PowerShell/터미널 인코딩을 UTF-8로 설정 (`chcp 65001`).
- 실계좌 주문 차단: `ALLOW_LIVE_TRADES=1` 환경 변수를 설정하지 않으면 `place_order.py` 예제가 실계좌에서 중단됩니다.

1. FAQ

- Q: 환경변수로도 설정 가능한가요?
    A: 계좌 선택은 `VMKIS_ACCOUNT` 로 가능합니다. 자격증명은 설정 파일에 둡니다.
- Q: 예제 실행 순서는?
    A: `hello_world.py` → `get_quote.py` → `get_balance.py` → `place_order.py`(모의) → `realtime_price.py` 순으로 권장합니다.
