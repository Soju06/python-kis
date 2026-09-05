"""기본 잔고 조회 예제.

configs/account_profiles.yaml 의 인증 정보를 사용해 계좌 잔고를 조회합니다.
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
    balance = account.balance()
    print(balance)


if __name__ == "__main__":
    main()
