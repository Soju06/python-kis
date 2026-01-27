from __future__ import annotations

import asyncio
import atexit
import threading
import time
from datetime import date, datetime
from datetime import time as time_value
from decimal import Decimal
from pathlib import Path
from typing import Literal, Mapping, TypeVar
from urllib.parse import urljoin

import httpx
from httpx_retries import Retry, RetryTransport
from pydantic import BaseModel

from pykis.api.auth import KisAuth
from pykis.api.constants import DEMO_DOMAIN, REAL_DOMAIN
from pykis.api.errors import (
    KisAuthError,
    KisErrorContext,
    KisHttpError,
    KisRateLimitError,
    KisResponseError,
    KisTransportError,
    KisUnsupportedEndpointError,
)
from pykis.api.rate_limit import (
    SyncRateLimiter,
    parse_retry_after,
    resolve_rate_limits,
    retry_backoff_hint,
)
from pykis.api.raw.types import Endpoint, KisResponse
from pykis.api.token import KisAccessToken
from pykis.api.token_cache import KisTokenCache, default_token_cache_dir
from pykis.logging import get_logger

RequestT = TypeVar("RequestT", bound=BaseModel)
ResponseT = TypeVar("ResponseT", bound=BaseModel)

DEFAULT_TIMEOUT = 8
TOKEN_RATE_LIMIT_WAIT = 300

logger = get_logger(__name__)


def _build_retry(backoff_hint: float) -> Retry:
    backoff_factor = backoff_hint if backoff_hint > 0 else 0.0
    max_backoff_wait = backoff_hint if backoff_hint > 0 else 120.0
    return Retry(
        total=2,
        allowed_methods=("GET",),
        status_forcelist=(429, 500, 502, 503, 504),
        backoff_factor=backoff_factor,
        max_backoff_wait=max_backoff_wait,
        backoff_jitter=0.0,
        respect_retry_after_header=True,
    )


def _error_context(
    *,
    endpoint_id: str | None = None,
    method: str | None = None,
    path: str | None = None,
    status_code: int | None = None,
    message: str | None = None,
) -> KisErrorContext:
    return KisErrorContext(
        endpoint_id=endpoint_id,
        method=method,
        path=path,
        status_code=status_code,
        message=message,
    )


def _encode_request_value(value: object) -> object:
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
        return {key: _encode_request_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_encode_request_value(val) for val in value]
    return value


def _apply_blank_allowed(model: BaseModel, payload: dict[str, object]) -> dict[str, object]:
    for name, field in model.__class__.model_fields.items():
        extra = field.json_schema_extra or {}
        if not extra.get("blank_allowed"):
            continue
        if getattr(model, name, None) is None:
            alias = field.serialization_alias or field.alias or name
            payload.setdefault(str(alias), "")
    return payload


def _coerce_query_params(payload: Mapping[str, object]) -> dict[str, str | int | float | None]:
    params: dict[str, str | int | float | None] = {}
    for key, value in payload.items():
        if value is None:
            params[str(key)] = None
        elif isinstance(value, (str, int, float)):
            params[str(key)] = value
        else:
            params[str(key)] = str(value)
    return params


def _extract_response_payload(response: KisResponse) -> dict[str, object] | None:
    try:
        data = response.json()
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return {str(key): value for key, value in data.items()}


def _is_invalid_token_payload(payload: Mapping[str, object]) -> bool:
    msg_cd = str(payload.get("msg_cd") or "").strip()
    error_code = str(payload.get("error_code") or "").strip()
    msg1 = str(payload.get("msg1") or "").strip()
    msg1_lower = msg1.lower()
    if msg_cd in {"EGW00121", "EGW00123"}:
        return True
    if error_code in {"EGW00121", "EGW00123"}:
        return True
    if "유효하지 않은 token" in msg1:
        return True
    return "invalid token" in msg1_lower


class SyncKisRawClient:
    auth: KisAuth
    domain: Literal["demo", "real"]
    rate_limit_per_second: float | None
    rate_limit_per_minute: float | None
    rate_limit_max_retries: int | None
    rate_limiter: SyncRateLimiter
    _client: httpx.Client
    _token_cache: dict[str, KisAccessToken]
    _token_cache_store: KisTokenCache | None
    _token_lock: threading.Lock | None
    _revoke_on_close: bool
    _closed: bool

    __slots__ = (
        "auth",
        "domain",
        "rate_limit_per_second",
        "rate_limit_per_minute",
        "rate_limit_max_retries",
        "rate_limiter",
        "_client",
        "_token_cache",
        "_token_cache_store",
        "_token_lock",
        "_revoke_on_close",
        "_closed",
    )

    def __init__(
        self,
        auth: KisAuth,
        domain: Literal["demo", "real"] | None = None,
        rate_limit: float | None = None,
        rate_limit_per_second: float | None = None,
        rate_limit_per_minute: float | None = None,
        rate_limit_max_retries: int | None = None,
        *,
        rate_limit_min_backoff: float = 0.5,
        keep_token: bool | str | Path | None = None,
        revoke_on_close: bool | None = None,
        client: httpx.Client | None = None,
        timeout: float | httpx.Timeout | None = None,
        atexit_close: bool = True,
    ) -> None:
        self.auth = auth
        self.domain = domain or "demo"
        limits = resolve_rate_limits(
            domain=self.domain,
            rate_limit=rate_limit,
            per_second=rate_limit_per_second,
            per_minute=rate_limit_per_minute,
        )
        self.rate_limit_per_second = limits.per_second
        self.rate_limit_per_minute = limits.per_minute
        self.rate_limit_max_retries = rate_limit_max_retries
        self.rate_limiter = SyncRateLimiter(
            per_second=self.rate_limit_per_second,
            per_minute=self.rate_limit_per_minute,
            min_backoff=rate_limit_min_backoff,
        )
        transport = None
        if client is None:
            retry = _build_retry(retry_backoff_hint(self.rate_limit_per_second))
            transport = RetryTransport(retry=retry)
        client_timeout = DEFAULT_TIMEOUT if timeout is None else timeout
        self._client = client or httpx.Client(timeout=client_timeout, transport=transport)
        self._token_cache = {}
        self._token_cache_store = None
        self._token_lock = None
        if keep_token:
            cache_dir = default_token_cache_dir() if keep_token is True else Path(keep_token).expanduser()
            self._token_cache_store = KisTokenCache(cache_dir, auth)
        if revoke_on_close is None:
            self._revoke_on_close = self._token_cache_store is None
        else:
            self._revoke_on_close = revoke_on_close
        self._closed = False
        if atexit_close:
            atexit.register(self._atexit_close)

    def _atexit_close(self) -> None:
        if self._closed:
            return
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            self.close()
        else:
            logger.warning("SyncKisRawClient still open; call close() explicitly.")

    def _acquire_rate_limit(self) -> None:
        self.rate_limiter.acquire()

    def _base_url(self, base_url: str | None = None) -> str:
        if base_url:
            return base_url
        return REAL_DOMAIN if self.domain == "real" else DEMO_DOMAIN

    def ensure_token(self, base_url: str | None = None) -> None:
        self._get_token(self._base_url(base_url))

    def _issue_token(self, base_url: str) -> KisAccessToken:
        while True:
            self._acquire_rate_limit()
            try:
                resp = self._client.post(
                    urljoin(base_url, "/oauth2/tokenP"),
                    headers={"content-type": "application/json; charset=UTF-8"},
                    json={
                        "grant_type": "client_credentials",
                        "appkey": self.auth.app_key,
                        "appsecret": self.auth.secret_key,
                    },
                )
            except httpx.HTTPError as exc:
                raise KisTransportError(
                    "token issuance transport error",
                    original=exc,
                    context=_error_context(method="POST", path="/oauth2/tokenP"),
                ) from exc

            if resp.status_code == 429:
                retry_after = parse_retry_after(resp.headers.get("Retry-After"))
                self.rate_limiter.on_rate_limited(retry_after)
                continue

            if resp.status_code != 403:
                if resp.status_code == 200 and "text/html" in (resp.headers.get("content-type") or ""):
                    snippet = resp.text[:200]
                    logger.warning(
                        "token response not JSON (status=%s body=%r); retrying after %ss",
                        resp.status_code,
                        snippet,
                        TOKEN_RATE_LIMIT_WAIT,
                    )
                    time.sleep(TOKEN_RATE_LIMIT_WAIT)
                    continue
                try:
                    resp.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    raise KisHttpError(
                        f"token issuance failed with status {resp.status_code}",
                        context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
                        payload=resp.text[:200],
                    ) from exc
                try:
                    payload = resp.json()
                except Exception as exc:
                    snippet = resp.text[:200]
                    raise KisAuthError(
                        "token response not JSON",
                        context=_error_context(
                            method="POST",
                            path="/oauth2/tokenP",
                            status_code=resp.status_code,
                            message=snippet,
                        ),
                    ) from exc
                token = KisAccessToken.from_payload(payload)
                if not token.token:
                    raise KisAuthError(
                        "token issuance returned empty access_token",
                        context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
                    )
                return token

            try:
                payload = resp.json()
            except Exception:
                payload = {}

            if payload.get("error_code") == "EGW00133":
                logger.warning("token rate-limited; waiting %ss before retry", TOKEN_RATE_LIMIT_WAIT)
                time.sleep(TOKEN_RATE_LIMIT_WAIT)
                continue
            error_code = payload.get("error_code")
            error_desc = payload.get("error_description")
            raise KisAuthError(
                f"token issuance failed: {error_code} {error_desc}".strip(),
                context=_error_context(method="POST", path="/oauth2/tokenP", status_code=resp.status_code),
            )

    def _get_token_lock(self) -> threading.Lock:
        if self._token_lock is None:
            self._token_lock = threading.Lock()
        return self._token_lock

    def _clear_token(self, base_url: str) -> None:
        self._token_cache.pop(base_url, None)
        if self._token_cache_store:
            self._token_cache_store.clear(base_url)

    def _get_token(self, base_url: str) -> KisAccessToken:
        lock = self._get_token_lock()
        with lock:
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

    def _refresh_token(self, base_url: str, used_token: str | None) -> None:
        lock = self._get_token_lock()
        with lock:
            current = self._token_cache.get(base_url)
            if current and used_token and current.token != used_token:
                return
            self._clear_token(base_url)
            token = self._issue_token(base_url)
            self._token_cache[base_url] = token
            if self._token_cache_store:
                self._token_cache_store.save(base_url, token)

    def _hashkey(self, base_url: str, body: Mapping[str, object]) -> str:
        attempts = 0
        while True:
            self._acquire_rate_limit()
            try:
                resp = self._client.post(
                    urljoin(base_url, "/uapi/hashkey"),
                    headers={
                        "content-type": "application/json",
                        "appkey": self.auth.app_key,
                        "appsecret": self.auth.secret_key,
                    },
                    json=body,
                )
            except httpx.HTTPError as exc:
                raise KisTransportError(
                    "hashkey transport error",
                    original=exc,
                    context=_error_context(method="POST", path="/uapi/hashkey"),
                ) from exc

            if resp.status_code == 429:
                retry_after = parse_retry_after(resp.headers.get("Retry-After"))
                self.rate_limiter.on_rate_limited(retry_after)
                attempts += 1
                if self.rate_limit_max_retries is not None and attempts > self.rate_limit_max_retries:
                    raise KisRateLimitError(
                        "rate limited for hashkey",
                        retry_after=retry_after,
                        context=_error_context(method="POST", path="/uapi/hashkey", status_code=resp.status_code),
                    )
                continue

            try:
                resp.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise KisHttpError(
                    f"hashkey failed with status {exc.response.status_code}",
                    context=_error_context(method="POST", path="/uapi/hashkey", status_code=exc.response.status_code),
                    payload=exc.response.text[:200],
                ) from exc

            payload = resp.json()
            return payload.get("HASH") or payload.get("hash") or ""

    def _revoke_token(self, base_url: str, token: KisAccessToken) -> None:
        self._acquire_rate_limit()
        try:
            resp = self._client.post(
                urljoin(base_url, "/oauth2/revokeP"),
                headers={"content-type": "application/json; charset=UTF-8"},
                json=token.revoke_payload(self.auth.app_key, self.auth.secret_key),
            )
            resp.raise_for_status()
        except Exception as exc:  # pragma: no cover - best effort on shutdown
            logger.warning("token revoke failed: %s", exc)

    def _request_with_token(
        self,
        *,
        method: str,
        base_url: str,
        path: str,
        headers: Mapping[str, str] | None,
        params: Mapping[str, str | int | float | None] | None,
        body: Mapping[str, object] | None,
        auth_required: bool,
        hashkey_required: bool,
    ) -> tuple[KisResponse, str | None]:
        headers = dict(headers or {})
        token_value: str | None = None
        if auth_required:
            token = self._get_token(base_url)
            headers["authorization"] = token.authorization()
            token_value = token.token

        if hashkey_required and body:
            headers["hashkey"] = self._hashkey(base_url, dict(body))

        self._acquire_rate_limit()
        try:
            response = self._client.request(
                method=method,
                url=urljoin(base_url, path),
                headers=headers,
                params=params,
                json=body if method == "POST" else None,
            )
        except httpx.HTTPError as exc:
            raise KisTransportError(
                "request transport error",
                original=exc,
                context=_error_context(method=method, path=path),
            ) from exc
        return response, token_value

    def request(
        self,
        *,
        method: str,
        base_url: str,
        path: str,
        headers: Mapping[str, str] | None,
        params: Mapping[str, str | int | float | None] | None,
        body: Mapping[str, object] | None,
        auth_required: bool,
        hashkey_required: bool,
    ) -> KisResponse:
        response, used_token = self._request_with_token(
            method=method,
            base_url=base_url,
            path=path,
            headers=headers,
            params=params,
            body=body,
            auth_required=auth_required,
            hashkey_required=hashkey_required,
        )
        if auth_required:
            payload = _extract_response_payload(response)
            if payload and _is_invalid_token_payload(payload):
                self._refresh_token(base_url, used_token)
                response, _ = self._request_with_token(
                    method=method,
                    base_url=base_url,
                    path=path,
                    headers=headers,
                    params=params,
                    body=body,
                    auth_required=auth_required,
                    hashkey_required=hashkey_required,
                )
        return response

    def call(
        self,
        endpoint: Endpoint[RequestT, ResponseT],
        request: RequestT | Mapping[str, object],
        headers: Mapping[str, str] | None = None,
    ) -> tuple[ResponseT, KisResponse]:
        if isinstance(request, BaseModel):
            model = request
        else:
            model = endpoint.request_model.model_validate(dict(request))
        request_fields: Mapping[str, object] = model.model_dump(by_alias=True, exclude_none=True)
        request_payload = {key: _encode_request_value(value) for key, value in request_fields.items()}
        request_payload = _apply_blank_allowed(model, request_payload)
        if endpoint.method == "GET":
            query = _coerce_query_params(request_payload)
            body = {}
        else:
            query = {}
            body = request_payload

        built_headers: dict[str, str] = dict(headers or {})
        built_headers.setdefault("content-type", "application/json; charset=utf-8")
        built_headers.setdefault("appkey", self.auth.app_key)
        built_headers.setdefault("appsecret", self.auth.secret_key)
        built_headers.setdefault("custtype", "P")
        tr_id = endpoint.real_tr_id if self.domain == "real" else endpoint.demo_tr_id
        has_tr_id = endpoint.real_tr_id is not None or endpoint.demo_tr_id is not None
        if has_tr_id:
            if tr_id is None:
                raise KisUnsupportedEndpointError(
                    f"endpoint not supported in {self.domain} domain: {endpoint.id}",
                    context=_error_context(endpoint_id=endpoint.id, method=endpoint.method, path=endpoint.path),
                )
            built_headers.setdefault("tr_id", tr_id)

        base_url = self._base_url()
        refresh_attempted = False
        while True:
            response, used_token = self._request_with_token(
                method=endpoint.method,
                base_url=base_url,
                path=endpoint.path,
                headers=built_headers,
                params=query if query else None,
                body=body if body else None,
                auth_required=endpoint.auth_required,
                hashkey_required=endpoint.hashkey_required,
            )
            attempts = 0
            while response.status_code == 429:
                retry_after = parse_retry_after(response.headers.get("Retry-After"))
                self.rate_limiter.on_rate_limited(retry_after)
                attempts += 1
                if self.rate_limit_max_retries is not None and attempts > self.rate_limit_max_retries:
                    raise KisRateLimitError(
                        f"rate limited for {endpoint.id}",
                        retry_after=retry_after,
                        context=_error_context(
                            endpoint_id=endpoint.id,
                            method=endpoint.method,
                            path=endpoint.path,
                            status_code=response.status_code,
                        ),
                    )
                response, used_token = self._request_with_token(
                    method=endpoint.method,
                    base_url=base_url,
                    path=endpoint.path,
                    headers=built_headers,
                    params=query if query else None,
                    body=body if body else None,
                    auth_required=endpoint.auth_required,
                    hashkey_required=endpoint.hashkey_required,
                )

            response_payload = _extract_response_payload(response)
            if (
                endpoint.auth_required
                and not refresh_attempted
                and response_payload
                and _is_invalid_token_payload(response_payload)
            ):
                self._refresh_token(base_url, used_token)
                refresh_attempted = True
                continue

            if response.is_success:
                if response_payload is None:
                    try:
                        data = response.json()
                    except Exception as exc:
                        snippet = response.text[:200]
                        raise KisResponseError(
                            f"invalid JSON for {endpoint.id}",
                            context=_error_context(
                                endpoint_id=endpoint.id,
                                method=endpoint.method,
                                path=endpoint.path,
                                status_code=response.status_code,
                                message=snippet,
                            ),
                        ) from exc
                else:
                    data = response_payload
                if isinstance(data, dict):
                    data_map = {str(key): value for key, value in data.items()}
                    if str(data_map.get("rt_cd")) not in ("0", "OK"):
                        raise KisResponseError(
                            f"API error for {endpoint.id}: {data_map.get('msg_cd')} {data_map.get('msg1')}".strip(),
                            context=_error_context(
                                endpoint_id=endpoint.id,
                                method=endpoint.method,
                                path=endpoint.path,
                                status_code=response.status_code,
                                message=str(data_map.get("msg1") or ""),
                            ),
                            payload=data_map,
                        )
                    return endpoint.response_model.model_validate(data_map), response
                return endpoint.response_model.model_validate(data), response
            raise KisHttpError(
                f"HTTP {response.status_code} for {endpoint.id}",
                context=_error_context(
                    endpoint_id=endpoint.id,
                    method=endpoint.method,
                    path=endpoint.path,
                    status_code=response.status_code,
                ),
                payload=response.text[:200],
            )

    def close(self) -> None:
        if self._closed:
            return
        if self._revoke_on_close:
            for base_url, token in list(self._token_cache.items()):
                if token.token:
                    self._revoke_token(base_url, token)
                    if self._token_cache_store:
                        self._token_cache_store.clear(base_url)
        self._client.close()
        self._closed = True

    def __enter__(self) -> "SyncKisRawClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
