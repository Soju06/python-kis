"""지정가 매수 뒤 정정·취소 예제 (안전 장치 포함).

체결되기 어려운 낮은 지정가로 넣은 뒤 수량을 정정하고 취소합니다.
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
    order = stock.buy(price=1000, qty=1)
    print(order)
    if order.pending:
        order = order.modify(qty=1)
        print(order)
    order.cancel()
    print(order)


if __name__ == "__main__":
    main()
