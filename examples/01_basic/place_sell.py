"""기본 매도 예제 (안전 장치 포함).

전량이 아니라 1주만 냅니다. 보유가 없으면 API 가 거절합니다.
실계좌 주문 시 ALLOW_LIVE_TRADES=1 이 필요합니다.
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

    if not kis.paper and os.environ.get("ALLOW_LIVE_TRADES") != "1":
        raise SystemExit("실계좌 주문입니다. 의도한 것이 맞다면 ALLOW_LIVE_TRADES=1 을 설정하고 다시 실행하세요.")

    stock = kis.stock("005930")
    order = stock.sell(qty=1)
    print(order)


if __name__ == "__main__":
    main()
