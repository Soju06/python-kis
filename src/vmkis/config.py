"""설정 파일 스키마.

`docs/guidelines/CONFIG_SCHEMA.md` 가 이 모듈의 사양입니다. 규칙 번호(R1~R9)는
그 문서와 1:1 로 대응합니다.

이 모듈이 하는 일은 **거부**입니다. 모르는 키, 빠진 키, 잘못된 타입을 조용히
넘기지 않습니다. 이전 스키마에서는 `virtaul: true` 오타가 기본값 `False`(실전)로
떨어져 모의투자 의도가 실전 주문이 됐습니다 (#69).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

__all__ = [
    "AccountConfig",
    "KisConfig",
    "load_kis_config",
]

#: 지원하는 스키마 판. 이 밖의 값은 거부합니다 (R1).
SUPPORTED_VERSIONS = frozenset({1})

MODES: tuple[str, ...] = ("live", "paper")

_TOP_KEYS = frozenset({"version", "apps", "accounts", "default_account", "token_dir", "user_agent", "endpoints"})
_APP_KEYS = frozenset({"mode", "hts_id", "app_key", "app_secret"})
_ACCOUNT_KEYS = frozenset({"app", "account_no", "product_code"})
_ENDPOINT_KEYS = frozenset({"base_url", "ws_url"})

#: 따옴표를 빼면 YAML 이 정수로 바꿔 버리는 필드 (R9).
#: `account_no: 00000000` 은 `0` 이 되고, 아무도 알려주지 않습니다.
_MUST_BE_STR = ("hts_id", "app_key", "app_secret", "account_no", "product_code", "app", "mode")


@dataclass(frozen=True)
class Endpoint:
    """한 모드의 서버 주소. 지정하지 않은 쪽은 `None` 이고 라이브러리 기본값을 씁니다."""

    base_url: str | None = None
    ws_url: str | None = None


@dataclass(frozen=True)
class AccountConfig:
    """계좌 하나를 쓰는 데 필요한 것 전부.

    `apps` 와 `accounts` 를 합쳐 놓은 결과입니다. 호출부는 두 블록의 관계를
    다시 풀 필요가 없습니다.
    """

    name: str
    """`accounts` 에서의 이름"""
    app: str
    """`apps` 에서의 이름. 토큰이 이 단위로 발급됩니다"""
    mode: Literal["live", "paper"]
    hts_id: str
    app_key: str
    app_secret: str
    account_no: str
    product_code: str
    token_path: Path
    """토큰 파일. 앱 이름에서 파생되므로 앱이 다르면 반드시 다릅니다"""

    @property
    def account(self) -> str:
        """`KisAuth.account` 형식 — `00000000-01`"""
        return f"{self.account_no}-{self.product_code}"

    @property
    def is_paper(self) -> bool:
        return self.mode == "paper"


@dataclass(frozen=True)
class KisConfig:
    """설정 파일 하나를 읽은 결과."""

    path: Path
    accounts: dict[str, AccountConfig]
    default_account: str
    user_agent: str | None = None
    endpoints: dict[str, Endpoint] | None = None

    def account(self, name: str | None = None) -> AccountConfig:
        """계좌 하나를 고릅니다. 이름을 생략하면 `default_account`.

        Raises:
            ValueError: 없는 계좌 이름인 경우
        """
        key = name or self.default_account

        if key not in self.accounts:
            known = ", ".join(sorted(self.accounts))
            raise ValueError(f"{self.path} 에 계좌 '{key}' 가 없습니다. 있는 계좌: {known}")

        return self.accounts[key]

    def endpoint(self, mode: str) -> Endpoint:
        """모드의 주소 재정의. 지정하지 않았으면 빈 `Endpoint`."""
        return (self.endpoints or {}).get(mode) or Endpoint()


def _reject_unknown(block: dict[str, Any], allowed: frozenset[str], where: str) -> None:
    """R2 — 모르는 키를 거부합니다.

    조용히 무시하면 오타가 사고가 됩니다. 무엇을 쓸 수 있는지도 같이 알려줍니다.
    """
    if unknown := sorted(set(block) - allowed):
        raise ValueError(
            f"{where} 에 모르는 키가 있습니다: {', '.join(unknown)}. 쓸 수 있는 키: {', '.join(sorted(allowed))}"
        )


def _require(block: dict[str, Any], keys: frozenset[str], where: str) -> None:
    """R3 — 필수 키가 없으면 거부합니다."""
    if missing := sorted(keys - set(block)):
        raise ValueError(f"{where} 에 필수 키가 없습니다: {', '.join(missing)}")


def _require_str(block: dict[str, Any], where: str) -> None:
    """R9 — 문자열 자리에 `int`/`bool` 이 오면 거부하고 따옴표를 안내합니다.

    사용자 오타가 아니라 **YAML 의 함정**입니다. `account_no: 00000000` 은 따옴표가
    없으면 정수 `0` 이 되고, 계좌번호가 통째로 사라집니다. 오류 메시지가 원인을
    바로 말해야 합니다.
    """
    for key in _MUST_BE_STR:
        if key not in block:
            continue

        value = block[key]

        if not isinstance(value, str):
            raise ValueError(
                f"{where}.{key} 가 {type(value).__name__} {value!r} 입니다. "
                f'문자열이어야 합니다 — 따옴표를 씌우세요: {key}: "{value}"'
            )


def _parse_endpoints(raw: Any, where: str) -> dict[str, Endpoint]:
    if not isinstance(raw, dict):
        raise ValueError(f"{where} 이(가) 매핑이 아닙니다: {type(raw).__name__}")

    _reject_unknown(raw, frozenset(MODES), where)

    parsed: dict[str, Endpoint] = {}

    for mode, block in raw.items():
        spot = f"{where}.{mode}"

        if not isinstance(block, dict):
            raise ValueError(f"{spot} 이(가) 매핑이 아닙니다: {type(block).__name__}")

        # 부분 지정을 허용합니다. 벤더가 웹소켓 포트만 바꾸는 일이 흔합니다.
        _reject_unknown(block, _ENDPOINT_KEYS, spot)
        parsed[mode] = Endpoint(base_url=block.get("base_url"), ws_url=block.get("ws_url"))

    return parsed


def _resolve_token_dir(raw: dict[str, Any], path: Path) -> Path:
    """토큰 폴더. 기본은 **설정 파일과 같은 폴더의 `token/`** 입니다.

    cwd 기준이면 다른 디렉터리에서 실행할 때마다 새 토큰 파일이 생겨 매번
    재발급하거나 엉뚱한 곳에 토큰이 쌓입니다.
    """
    token_dir = raw.get("token_dir")

    if token_dir is None:
        return path.parent / "token"

    if not isinstance(token_dir, str):
        raise ValueError(f'{path} 의 token_dir 이 문자열이 아닙니다 — 따옴표를 씌우세요: token_dir: "{token_dir}"')

    return path.parent / token_dir if not Path(token_dir).is_absolute() else Path(token_dir)


def load_kis_config(path: str | Path = "configs/account_profiles.yaml") -> KisConfig:
    """설정 파일을 읽고 검증합니다.

    사양은 `docs/guidelines/CONFIG_SCHEMA.md` 이며 규칙 번호가 대응합니다.

    Args:
        path: 설정 파일 경로

    Returns:
        검증을 통과한 설정

    Raises:
        ValueError: 규칙 R1~R9 중 하나를 어긴 경우
        FileNotFoundError: 파일이 없는 경우
    """
    path = Path(path)

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not isinstance(raw, dict):
        raise ValueError(f"{path} 이(가) 매핑이 아닙니다: {type(raw).__name__}")

    _check_version(raw, path)
    _reject_unknown(raw, _TOP_KEYS, str(path))
    _require(raw, frozenset({"apps", "accounts"}), str(path))

    token_dir = _resolve_token_dir(raw, path)
    apps = _parse_apps(raw["apps"], path, token_dir)
    accounts = _parse_accounts(raw["accounts"], path, apps)

    _check_orphan_apps(apps, accounts, path)

    return KisConfig(
        path=path,
        accounts=accounts,
        default_account=_resolve_default_account(raw, accounts, path),
        user_agent=raw.get("user_agent"),
        endpoints=_parse_endpoints(raw["endpoints"], f"{path} 의 endpoints") if "endpoints" in raw else None,
    )


def _check_version(raw: dict[str, Any], path: Path) -> None:
    """R1 — 판이 없거나 모르는 값이면 거부합니다.

    옛 형식(`default:` + `configs:`)에는 이 키가 없으므로 여기서 걸립니다.
    조용히 오독되지 않는 것이 이 규칙의 목적입니다.
    """
    if "version" not in raw:
        raise ValueError(
            f"{path} 에 `version` 이 없습니다. 이 파일은 0.0.x 형식으로 보입니다 — 지원하지 않습니다. "
            f"template_account_profiles.yaml 을 참고해 다시 작성하세요."
        )

    version = raw["version"]

    if version not in SUPPORTED_VERSIONS:
        known = ", ".join(str(v) for v in sorted(SUPPORTED_VERSIONS))
        raise ValueError(f"{path} 의 version 이 {version!r} 입니다. 아는 판: {known}")


def _parse_apps(raw: Any, path: Path, token_dir: Path) -> dict[str, dict[str, Any]]:
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{path} 의 apps 가 비어 있거나 매핑이 아닙니다")

    apps: dict[str, dict[str, Any]] = {}

    for name, block in raw.items():
        where = f"{path} 의 apps.{name}"

        if not isinstance(block, dict):
            raise ValueError(f"{where} 이(가) 매핑이 아닙니다: {type(block).__name__}")

        _reject_unknown(block, _APP_KEYS, where)
        _require(block, _APP_KEYS, where)
        _require_str(block, where)

        if block["mode"] not in MODES:
            raise ValueError(
                f"{where}.mode 가 {block['mode']!r} 입니다. {' | '.join(MODES)} 중 하나여야 합니다"  # R4
            )

        # 토큰 파일명을 앱 이름에서 **파생**시킵니다. 사용자가 앱마다 경로를 적게
        # 하면 두 앱이 같은 파일을 가리켜도 아무도 못 막고, 증상은 "가끔 인증이
        # 풀린다"로 나타납니다.
        apps[name] = {**block, "token_path": token_dir / f"{name}.json"}

    return apps


def _parse_accounts(raw: Any, path: Path, apps: dict[str, dict[str, Any]]) -> dict[str, AccountConfig]:
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{path} 의 accounts 가 비어 있거나 매핑이 아닙니다")

    accounts: dict[str, AccountConfig] = {}

    for name, block in raw.items():
        where = f"{path} 의 accounts.{name}"

        if not isinstance(block, dict):
            raise ValueError(f"{where} 이(가) 매핑이 아닙니다: {type(block).__name__}")

        _reject_unknown(block, _ACCOUNT_KEYS, where)
        _require(block, _ACCOUNT_KEYS, where)
        _require_str(block, where)

        app_name = block["app"]

        if app_name not in apps:  # R5
            known = ", ".join(sorted(apps))
            raise ValueError(f"{where}.app 이 '{app_name}' 인데 apps 에 없습니다. 있는 앱: {known}")

        app = apps[app_name]
        accounts[name] = AccountConfig(
            name=name,
            app=app_name,
            mode=app["mode"],
            hts_id=app["hts_id"],
            app_key=app["app_key"],
            app_secret=app["app_secret"],
            account_no=block["account_no"],
            product_code=block["product_code"],
            token_path=app["token_path"],
        )

    return accounts


def _check_orphan_apps(apps: dict[str, Any], accounts: dict[str, AccountConfig], path: Path) -> None:
    """R6 — 어떤 계좌도 쓰지 않는 앱을 거부합니다.

    R5 와 **양방향**인 이유: 한쪽만 검사하면 오타로 만든 블록이 고아로 조용히
    남습니다. 자격증명이 든 블록이 아무도 모르게 방치되는 것은 그 자체로 위험합니다.
    """
    used = {account.app for account in accounts.values()}

    if orphans := sorted(set(apps) - used):
        raise ValueError(f"{path} 의 apps 중 아무 계좌도 쓰지 않는 것이 있습니다: {', '.join(orphans)}")


def _resolve_default_account(raw: dict[str, Any], accounts: dict[str, AccountConfig], path: Path) -> str:
    """R7·R8 — 계좌가 둘 이상이면 기본 계좌를 반드시 적어야 하고, 그것이 존재해야 합니다."""
    default = raw.get("default_account")

    if default is None:
        if len(accounts) > 1:  # R7
            known = ", ".join(sorted(accounts))
            raise ValueError(f"{path} 에 계좌가 {len(accounts)}개인데 default_account 가 없습니다. 있는 계좌: {known}")

        return next(iter(accounts))

    if default not in accounts:  # R8
        known = ", ".join(sorted(accounts))
        raise ValueError(f"{path} 의 default_account 가 '{default}' 인데 accounts 에 없습니다. 있는 계좌: {known}")

    return default
