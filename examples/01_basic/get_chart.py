"""일봉 차트 조회 예제."""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)
    stock = kis.stock("005930")
    print(repr(stock.chart("7d")))


if __name__ == "__main__":
    main()
