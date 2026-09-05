"""1.0.0 호환 제거가 착수됐는지 기록합니다. (#33–#36)

예전에는 2026-11-27 시한폭탄으로 `#30` 을 깨웠습니다. `#30` 은 구조·예제
조건으로 닫혔고, 소유자가 2026-09-05 에 `#33`–`#36` 을 앞당겨 열었습니다.
시한은 더 이상 의미가 없습니다 — 폴백이 사라졌는지를 봅니다.
"""

from __future__ import annotations

import importlib
import warnings

import pytest


def test_pykis_alias_is_removed() -> None:
    vmkis = importlib.import_module("vmkis")

    with pytest.raises(AttributeError):
        _ = vmkis.PyKis


def test_root_types_delegation_is_removed() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        with pytest.raises(ImportError):
            from vmkis import KisObjectProtocol  # noqa: F401


def test_legacy_env_prefix_is_ignored(monkeypatch) -> None:
    from vmkis import helpers

    monkeypatch.delenv("VMKIS_PROFILE", raising=False)
    monkeypatch.setenv("PYKIS_PROFILE", "legacy")

    assert helpers._env("PROFILE") is None
