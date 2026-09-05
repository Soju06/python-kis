"""실시간 체결내역 구독 예제.

계좌 체결 알림입니다. 종료하려면 Enter를 누르세요.
"""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)
    account = kis.account()

    def on_execution(sender, e):
        print(e.response)

    ticket = account.on("execution", on_execution)
    try:
        input("Press Enter to stop streaming...\n")
    finally:
        ticket.unsubscribe()


if __name__ == "__main__":
    main()
