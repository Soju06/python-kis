"""기본 주문 예제 (안전 장치 포함).

- 실계좌 주문 시 ALLOW_LIVE_TRADES=1 환경 변수를 설정해야 합니다.
- 모의투자 계정으로 먼저 검증하고, configs/account_profiles.yaml 설정 후 주문을 수행합니다.
"""

import os

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)

    allow_live = os.environ.get("ALLOW_LIVE_TRADES") == "1"

    # 이 파일의 docstring이 약속하는 안전장치. 이전에는 allow_live를 계산만 하고
    # 사용하지 않아, 실계좌 설정으로 실행하면 아무 확인 없이 실주문이 나갔다.
    if not kis.paper and not allow_live:
        raise SystemExit("실계좌 주문입니다. 의도한 것이 맞다면 ALLOW_LIVE_TRADES=1 을 설정하고 다시 실행하세요.")

    stock = kis.stock("005930")  # 삼성전자

    # 예시: 시장가 매수 1주 (실계좌/모의투자 설정에 따라 실행)
    order = stock.buy(qty=1)
    print(order)


if __name__ == "__main__":
    main()
