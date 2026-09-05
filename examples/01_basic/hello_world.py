"""첫 연결 예제.

`create_client` 로 설정을 읽어 `VmKis` 를 만듭니다. 시세는 `get_quote.py`
를 보세요.
"""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account)
    print("connected", type(kis).__name__)


if __name__ == "__main__":
    main()
