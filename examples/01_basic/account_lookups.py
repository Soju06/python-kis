"""잔고 외 계좌 조회 예제.

기간 손익, 일별 체결, 매수 가능 금액, 매도 가능 수량, 미체결.
`profits()` 는 모의투자를 지원하지 않습니다.
"""

from datetime import date, timedelta

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)
    account = kis.account()
    stock = kis.stock("005930")
    start = date.today() - timedelta(days=30)

    print(repr(account.daily_orders(start=start)))
    print(repr(account.orderable_amount(market="KRX", symbol="005930")))
    print(repr(stock.orderable_amount()))
    print(stock.orderable)
    print(repr(account.pending_orders()))
    print(repr(account.profits(start=start)))


if __name__ == "__main__":
    main()
