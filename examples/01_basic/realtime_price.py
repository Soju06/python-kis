"""실시간 체결가 구독 예제.

- 삼성전자(005930) 실시간 체결가를 구독합니다.
- 종료하려면 Enter를 누르세요.
"""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)

    stock = kis.stock("005930")  # 삼성전자

    def on_price(sender, e):
        print(e.response)

    ticket = stock.on("price", on_price)
    try:
        input("Press Enter to stop streaming...\n")
    finally:
        ticket.unsubscribe()


if __name__ == "__main__":
    main()
