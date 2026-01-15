from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from pykis.api.auth import KisAuth
from pykis.api.constants import DEMO_DOMAIN, REAL_DOMAIN
from pykis.api.token import KisAccessToken

_SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def default_token_cache_dir() -> Path:
    return Path.home() / ".pykis"


@dataclass(frozen=True, slots=True)
class KisTokenCache:
    root: Path
    auth: KisAuth

    def token_path(self, base_url: str) -> Path:
        domain = _domain_label(base_url)
        safe_id = _SAFE_ID_RE.sub("_", self.auth.id or "anon")
        key = sha256(
            f"pykis{self.auth.id or ''}{self.auth.appkey}{self.auth.appsecret}{base_url}token".encode()
        ).hexdigest()
        return self.root / f"token_{domain}_{safe_id}_{key}.json"

    def load(self, base_url: str) -> KisAccessToken | None:
        path = self.token_path(base_url)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            return KisAccessToken.from_cache(payload)
        except Exception:
            return None

    def save(self, base_url: str, token: KisAccessToken) -> None:
        path = self.token_path(base_url)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(path.suffix + ".tmp")
        tmp_path.write_text(json.dumps(token.to_cache(), ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            os.chmod(tmp_path, 0o600)
        except Exception:
            pass
        tmp_path.replace(path)

    def clear(self, base_url: str) -> None:
        path = self.token_path(base_url)
        try:
            path.unlink()
        except FileNotFoundError:
            return
        except Exception:
            return

def _domain_label(base_url: str) -> str:
    if base_url == DEMO_DOMAIN:
        return "demo"
    if base_url == REAL_DOMAIN:
        return "real"
    return "custom"
