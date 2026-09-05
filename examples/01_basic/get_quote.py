"""기본 시세 조회 예제.

이 예제는 configs/account_profiles.yaml 에서 인증 정보를 로드한 뒤
삼성전자(005930) 시세를 조회해 출력합니다.
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
    quote = stock.quote()
    print(quote)


if __name__ == "__main__":
    main()
