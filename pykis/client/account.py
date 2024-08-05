from typing import Any

from pykis.client.form import KisForm

__all__ = [
    "KisAccountNumber",
]


class KisAccountNumber(KisForm):
    """한국투자증권 계좌 정보"""

    __slots__ = [
        "number",
        "code",
    ]

    number: str
    """종합계좌번호"""
    code: str
    """계좌상품코드"""

    def __init__(self, account: str):
        """한국투자증권 계좌 정보를 생성합니다.

        Args:
            account: 계좌번호 XXXXXXXX, XXXXXXXX-XX, XXXXXXXXXX 중 하나의 숫자 형식
        """
        account_len = len(account)

        if account_len == 8:
            self.number = account
            self.code = "01"
        elif account_len == 10:
            self.number = account[:8]
            self.code = account[8:]
        elif account_len == 11 and account[8] == "-":
            self.number = account[:8]
            self.code = account[9:]
        else:
            raise ValueError(f"계좌번호 형식이 잘못되었습니다. ({account})")

        if not self.number.isdigit() or not self.code.isdigit():
            raise ValueError(f"계좌번호에 잘못된 문자가 포함되어 있습니다. ({account})")

    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        """계좌 정보를 추가합니다."""
        if dict is None:
            dict = {}

        dict.update({"CANO": self.number, "ACNT_PRDT_CD": self.code})
        return dict

    def __eq__(self, o: object) -> bool:
        if isinstance(o, KisAccountNumber):
            return self.number == o.number and self.code == o.code

        return False

    def __hash__(self) -> int:
        return hash((self.number, self.code))

    def __str__(self) -> str:
        return f"{self.number}-{self.code}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.number}-{self.code}')"
