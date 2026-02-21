from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

_APP_KEY_LENGTH = 36
_SECRET_KEY_LENGTH = 180
_ALLOWED_KEYS = frozenset({"id", "app_key", "secret_key", "account", "demo"})


def _normalize_required_str(value: object, key: str) -> str:
    if value is None:
        raise ValueError(f"Missing required auth key: {key}")
    if not isinstance(value, str):
        raise ValueError(f"Auth key must be a string: {key}")
    value = value.strip()
    if not value:
        raise ValueError(f"Auth key must not be blank: {key}")
    return value


def _normalize_optional_str(value: object, key: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Auth key must be a string: {key}")
    value = value.strip()
    if not value:
        raise ValueError(f"Auth key must not be blank: {key}")
    return value


def _normalize_optional_bool(data: dict[str, object], key: str, default: bool) -> bool:
    if key not in data:
        return default
    value = data[key]
    if not isinstance(value, bool):
        raise ValueError(f"Auth key must be a boolean: {key}")
    return value


def _validate_length(value: str, key: str, expected: int) -> str:
    if len(value) != expected:
        raise ValueError(f"{key} length must be {expected} characters")
    return value


def _parse_required_key(data: dict[str, object], key: str, expected_length: int) -> str:
    value = _normalize_required_str(data.get(key), key)
    return _validate_length(value, key, expected_length)


def _validate_required_key(value: str, key: str, expected_length: int) -> str:
    normalized = _normalize_required_str(value, key)
    return _validate_length(normalized, key, expected_length)


def _validate_account(value: str | None) -> str | None:
    if value is None:
        return None
    account = value.strip()
    if not account:
        raise ValueError("Account must not be blank")
    if account.isdigit() and len(account) in (8, 10):
        return account
    if "-" in account:
        head, tail = account.split("-", 1)
        if head.isdigit() and tail.isdigit() and len(head) == 8 and len(tail) == 2:
            return account
    raise ValueError(f"Invalid account format: {value}")


@dataclass(frozen=True, slots=True)
class KisAuth:
    id: str | None
    app_key: str
    secret_key: str
    account: str | None
    demo: bool

    def __post_init__(self) -> None:
        app_key = _validate_required_key(self.app_key, "app_key", _APP_KEY_LENGTH)
        secret_key = _validate_required_key(self.secret_key, "secret_key", _SECRET_KEY_LENGTH)
        id_value = _normalize_optional_str(self.id, "id")
        account_value = _validate_account(_normalize_optional_str(self.account, "account"))
        if not isinstance(self.demo, bool):
            raise ValueError("Auth key must be a boolean: demo")

        if app_key != self.app_key:
            object.__setattr__(self, "app_key", app_key)
        if secret_key != self.secret_key:
            object.__setattr__(self, "secret_key", secret_key)
        if id_value != self.id:
            object.__setattr__(self, "id", id_value)
        if account_value != self.account:
            object.__setattr__(self, "account", account_value)

    @property
    def account_number(self) -> tuple[str | None, str | None]:
        if not self.account:
            return None, None
        account = self.account.strip()
        if account.isdigit():
            if len(account) == 8:
                return account, "01"
            if len(account) == 10:
                return account[:8], account[8:]
        if "-" in account:
            head, tail = account.split("-", 1)
            if head.isdigit() and tail.isdigit() and len(head) == 8 and len(tail) == 2:
                return head, tail
        return None, None

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "KisAuth":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"Auth payload must be a JSON object: {path}")
        data: dict[str, object] = raw
        extra_keys = sorted(set(data) - _ALLOWED_KEYS)
        if extra_keys:
            raise ValueError(f"Unknown auth keys: {', '.join(extra_keys)}")

        return cls(
            id=_normalize_optional_str(data.get("id"), "id"),
            app_key=_parse_required_key(data, "app_key", _APP_KEY_LENGTH),
            secret_key=_parse_required_key(data, "secret_key", _SECRET_KEY_LENGTH),
            account=_validate_account(_normalize_optional_str(data.get("account"), "account")),
            demo=_normalize_optional_bool(data, "demo", False),
        )
