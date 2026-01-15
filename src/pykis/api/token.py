from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Mapping
from zoneinfo import ZoneInfo

try:
    _KST = ZoneInfo("Asia/Seoul")
except Exception:
    _KST = timezone(timedelta(hours=9))


@dataclass(frozen=True, slots=True)
class KisAccessToken:
    token: str
    token_type: str
    expires_in: int
    issued_at: datetime

    @property
    def expired_at(self) -> datetime:
        return self.issued_at + timedelta(seconds=self.expires_in)

    @property
    def expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.expired_at

    def authorization(self) -> str:
        return f"{self.token_type} {self.token}"

    def to_cache(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "token": self.token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "issued_at": self.issued_at.astimezone(timezone.utc).isoformat(),
        }

    @classmethod
    def from_cache(cls, payload: Mapping[str, object]) -> "KisAccessToken":
        token = payload.get("token", "")
        token_type = payload.get("token_type", "Bearer")
        expires_in = int(payload.get("expires_in", 0))
        issued_at_raw = payload.get("issued_at") or payload.get("issued_at_utc")
        issued_at = _parse_datetime(issued_at_raw)
        if issued_at is None:
            expired_at_raw = payload.get("expired_at") or payload.get("access_token_token_expired")
            expired_at = _parse_datetime(expired_at_raw, default_tz=_KST)
            if expired_at and expires_in:
                issued_at = expired_at - timedelta(seconds=expires_in)
            else:
                issued_at = datetime.now(timezone.utc)
        return cls(
            token=token,
            token_type=token_type,
            expires_in=expires_in,
            issued_at=issued_at,
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, object]) -> "KisAccessToken":
        expires_in = int(payload.get("expires_in", 0))
        issued_at = datetime.now(timezone.utc)
        expired_at = _parse_token_expired_at(payload)
        if expired_at:
            if expires_in > 0:
                issued_at = expired_at - timedelta(seconds=expires_in)
            else:
                expires_in = max(int((expired_at - issued_at).total_seconds()), 0)
        return cls(
            token=payload.get("access_token", ""),
            token_type=payload.get("token_type", "Bearer"),
            expires_in=expires_in,
            issued_at=issued_at,
        )

    def revoke_payload(self, appkey: str, appsecret: str) -> dict[str, object]:
        return {
            "appkey": appkey,
            "appsecret": appsecret,
            "token": self.token,
        }


def _parse_datetime(value: object | None, *, default_tz: timezone | ZoneInfo = timezone.utc) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=default_tz)
        return parsed.astimezone(timezone.utc)
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=default_tz)
    return parsed.astimezone(timezone.utc)


def _parse_token_expired_at(payload: Mapping[str, object]) -> datetime | None:
    raw = payload.get("access_token_token_expired") or payload.get("access_token_expired")
    return _parse_datetime(raw, default_tz=_KST)
