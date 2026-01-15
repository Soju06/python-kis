from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True, slots=True)
class KisAuth:
    id: str | None
    appkey: str
    appsecret: str
    account: str | None
    demo: bool
    custtype: Literal["P", "B"] = "P"

    @property
    def account_number(self) -> tuple[str | None, str | None]:
        if not self.account:
            return None, None
        account = self.account.strip()
        if "-" in account:
            head, tail = account.split("-", 1)
            if len(head) == 8 and len(tail) == 2:
                return head, tail
        if account.isdigit() and len(account) == 10:
            return account[:8], account[8:]
        return None, None

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "KisAuth":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            id=data.get("id"),
            appkey=data["appkey"],
            appsecret=data["appsecret"],
            account=data.get("account"),
            demo=bool(data.get("demo", False)),
            custtype=data.get("custtype", "P"),
        )
