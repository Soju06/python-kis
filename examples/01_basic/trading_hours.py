"""장운영 시간 조회 예제.

`kis.trading_hours(market)` 입니다. `stock.trading_hours()` 는 없습니다.
"""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)
    hours = kis.trading_hours("KR")
    print(hours.market, hours.open, hours.close)


if __name__ == "__main__":
    main()
