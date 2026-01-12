from __future__ import annotations

import atexit
import time
from datetime import date, datetime, time as time_value
from decimal import Decimal
from pathlib import Path
from typing import Literal, Mapping, TypeVar
from urllib.parse import urljoin

import requests

from .auth import KisAuth
from .constants import DEMO_DOMAIN, REAL_DOMAIN
from .token import KisAccessToken
from .token_cache import KisTokenCache, default_token_cache_dir
from pydantic import BaseModel
from pykis.api.raw.types import Endpoint

RequestT = TypeVar("RequestT", bound=BaseModel)
ResponseT = TypeVar("ResponseT", bound=BaseModel)


DEFAULT_TIMEOUT = 8
TOKEN_RATE_LIMIT_WAIT = 300


class KisRawClient:
    __slots__ = (
        "auth",
        "domain",
        "rate_limit",
        "session",
        "_token_cache",
        "_token_cache_store",
        "_revoke_on_close",
    )

    def __init__(
        self,
        auth: KisAuth,
        domain: Literal["demo", "real"] | None = None,
        rate_limit: float = 0.4,
        *,
        keep_token: bool | str | Path | None = None,
        revoke_on_close: bool | None = None,
    ):
        self.auth = auth
        self.domain: Literal["demo", "real"] = domain or "demo"
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self._token_cache: dict[str, KisAccessToken] = {}
        self._token_cache_store: KisTokenCache | None = None
        if keep_token:
            cache_dir = default_token_cache_dir() if keep_token is True else Path(keep_token).expanduser()
            self._token_cache_store = KisTokenCache(cache_dir, auth)
        if revoke_on_close is None:
            self._revoke_on_close = self._token_cache_store is None
        else:
            self._revoke_on_close = revoke_on_close
        atexit.register(self.close)

    def _sleep(self) -> None:
        if self.rate_limit > 0:
            time.sleep(self.rate_limit)

    def _base_url(self, base_url: str | None = None) -> str:
        if base_url:
            return base_url
        return REAL_DOMAIN if self.domain == "real" else DEMO_DOMAIN

    def ensure_token(self, base_url: str | None = None) -> None:
        self._get_token(self._base_url(base_url))

    def _issue_token(self, base_url: str) -> KisAccessToken:
        while True:
            self._sleep()
            resp = self.session.post(
                urljoin(base_url, "/oauth2/tokenP"),
                headers={"content-type": "application/json; charset=UTF-8"},
                json={
                    "grant_type": "client_credentials",
                    "appkey": self.auth.appkey,
                    "appsecret": self.auth.appsecret,
                },
            )
            if resp.status_code != 403:
                if resp.status_code == 200 and "text/html" in (resp.headers.get("content-type") or ""):
                    snippet = resp.text[:200]
                    print(f"[kis.raw] token response not JSON (status={resp.status_code} body={snippet!r})")
                    print(f"[kis.raw] token rate-limited, waiting {TOKEN_RATE_LIMIT_WAIT}s before retry")
                    time.sleep(TOKEN_RATE_LIMIT_WAIT)
                    continue
                resp.raise_for_status()
                try:
                    payload = resp.json()
                except Exception:
                    snippet = resp.text[:200]
                    raise RuntimeError(
                        f"[kis.raw] token response not JSON (status={resp.status_code} body={snippet!r})"
                    )
                token = KisAccessToken.from_payload(payload)
                if not token.token:
                    raise RuntimeError("[kis.raw] token issuance returned empty access_token")
                return token

            try:
                payload = resp.json()
            except Exception:
                payload = {}

            if payload.get("error_code") == "EGW00133":
                print(f"[kis.raw] token rate-limited, waiting {TOKEN_RATE_LIMIT_WAIT}s before retry")
                time.sleep(TOKEN_RATE_LIMIT_WAIT)
                continue
            error_code = payload.get("error_code")
            error_desc = payload.get("error_description")
            raise RuntimeError(f"[kis.raw] token issuance failed: {error_code} {error_desc}".strip())

    def _get_token(self, base_url: str) -> KisAccessToken:
        token = self._token_cache.get(base_url)
        if token and not token.expired:
            return token
        if token and token.expired:
            self._token_cache.pop(base_url, None)
        if self._token_cache_store:
            cached = self._token_cache_store.load(base_url)
            if cached and not cached.expired:
                self._token_cache[base_url] = cached
                return cached
            if cached and cached.expired:
                self._token_cache_store.clear(base_url)
        token = self._issue_token(base_url)
        self._token_cache[base_url] = token
        if self._token_cache_store:
            self._token_cache_store.save(base_url, token)
        return token

    def _hashkey(self, base_url: str, body: Mapping[str, object]) -> str:
        self._sleep()
        resp = self.session.post(
            urljoin(base_url, "/uapi/hashkey"),
            headers={
                "content-type": "application/json",
                "appkey": self.auth.appkey,
                "appsecret": self.auth.appsecret,
            },
            json=body,
        )
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("HASH") or payload.get("hash") or ""

    def _revoke_token(self, base_url: str, token: KisAccessToken) -> None:
        self._sleep()
        try:
            resp = self.session.post(
                urljoin(base_url, "/oauth2/revokeP"),
                headers={"content-type": "application/json; charset=UTF-8"},
                json=token.revoke_payload(self.auth.appkey, self.auth.appsecret),
            )
            resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - best effort on shutdown
            print(f"[kis.raw] token revoke failed: {exc}")

    def request(
        self,
        *,
        method: Literal["GET", "POST"],
        base_url: str,
        path: str,
        headers: Mapping[str, str] | None,
        params: Mapping[str, object] | None,
        body: Mapping[str, object] | None,
        auth_required: bool,
        hashkey_required: bool,
        max_attempts: int = 3,
    ) -> requests.Response:
        headers = dict(headers or {})
        if auth_required:
            token = self._get_token(base_url)
            headers["authorization"] = token.authorization()

        if hashkey_required and body:
                headers["hashkey"] = self._hashkey(base_url, dict(body))

        for attempt in range(max_attempts):
            self._sleep()
            try:
                response = self.session.request(
                    method=method,
                    url=urljoin(base_url, path),
                    headers=headers,
                    params=params,
                    json=body if method == "POST" else None,
                    timeout=DEFAULT_TIMEOUT,
                )
            except requests.RequestException as exc:
                if attempt < max_attempts - 1:
                    wait = float(attempt + 1)
                    print(f"[kis.raw] request error {exc}, retrying in {wait:.0f}s")
                    time.sleep(wait)
                    continue
                raise
            if response.status_code in {429, 500, 502, 503, 504} and attempt < max_attempts - 1:
                retry_after = response.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.isdigit() else float(attempt + 1)
                print(f"[kis.raw] HTTP {response.status_code}, retrying in {wait:.0f}s")
                time.sleep(wait)
                continue
            return response
        return response

    def call(
        self,
        endpoint: Endpoint[RequestT, ResponseT],
        request: RequestT | Mapping[str, object],
        headers: Mapping[str, str] | None = None,
    ) -> tuple[ResponseT, requests.Response]:
        if isinstance(request, BaseModel):
            model = request
        else:
            model = endpoint.request_model.model_validate(dict(request))
        payload: Mapping[str, object] = model.model_dump(by_alias=True, exclude_none=True)
        request_payload = {key: self._encode_request_value(value) for key, value in payload.items()}
        if endpoint.method == "GET":
            query = request_payload
            body = {}
        else:
            query = {}
            body = request_payload

        built_headers: dict[str, str] = dict(headers or {})
        built_headers.setdefault("content-type", "application/json; charset=utf-8")
        built_headers.setdefault("appkey", self.auth.appkey)
        built_headers.setdefault("appsecret", self.auth.appsecret)
        built_headers.setdefault("custtype", self.auth.custtype)
        tr_id = endpoint.real_tr_id if self.domain == "real" else endpoint.demo_tr_id
        has_tr_id = endpoint.real_tr_id is not None or endpoint.demo_tr_id is not None
        if has_tr_id:
            if tr_id is None:
                raise RuntimeError(f"[kis.raw] endpoint not supported in {self.domain} domain: {endpoint.id}")
            built_headers.setdefault("tr_id", tr_id)

        for attempt in range(2):
            response = self.request(
                method=endpoint.method,
                base_url=self._base_url(),
                path=endpoint.path,
                headers=built_headers,
                params=query if query else None,
                body=body if body else None,
                auth_required=endpoint.auth_required,
                hashkey_required=endpoint.hashkey_required,
            )
            if response.ok:
                try:
                    data = response.json()
                except Exception:
                    snippet = response.text[:200]
                    raise RuntimeError(
                        f"[kis.raw] invalid JSON for {endpoint.id}: status={response.status_code} body={snippet!r}"
                    )
                return endpoint.response_model.model_validate(data), response
            if response.status_code >= 500 and attempt == 0:
                print(f"[kis.raw] HTTP {response.status_code} for {endpoint.id}, retrying once")
                time.sleep(1.0)
                continue
            raise RuntimeError(f"[kis.raw] HTTP {response.status_code} for {endpoint.id}: {response.text[:200]}")
        raise RuntimeError(f"[kis.raw] HTTP error for {endpoint.id}")

    def _encode_request_value(self, value: object) -> object:
        if isinstance(value, datetime):
            return value.strftime("%Y%m%d%H%M%S")
        if isinstance(value, date) and not isinstance(value, datetime):
            return value.strftime("%Y%m%d")
        if isinstance(value, time_value):
            return value.strftime("%H%M%S")
        if isinstance(value, bool):
            return "Y" if value else "N"
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, dict):
            return {key: self._encode_request_value(val) for key, val in value.items()}
        if isinstance(value, list):
            return [self._encode_request_value(val) for val in value]
        return value

    def close(self) -> None:
        if self._revoke_on_close:
            for base_url, token in list(self._token_cache.items()):
                if token.token:
                    self._revoke_token(base_url, token)
                    if self._token_cache_store:
                        self._token_cache_store.clear(base_url)
        self.session.close()
