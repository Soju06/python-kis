"""토큰 자동 저장 예제.

`create_client` 는 설정의 앱 이름 경로에 토큰을 둡니다 (`configs/token/`).
`keep_token=False` 면 저장하지 않습니다.
"""

from vmkis import create_client


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/account_profiles.yaml", help="설정 파일 경로")
    parser.add_argument("--account", help="쓸 계좌 이름. 생략하면 default_account")
    args = parser.parse_args()

    kis = create_client(args.config, account=args.account, keep_token=True)
    print(kis.stock("005930").quote())


if __name__ == "__main__":
    main()
