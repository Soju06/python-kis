from pathlib import Path

from vmkis.utils.workspace import get_cache_path, get_workspace_path


def test_get_workspace_and_cache_paths_resolve(monkeypatch, tmp_path):
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    ws = get_workspace_path()
    assert isinstance(ws, Path)
    expected_ws = (fake_home / ".vmkis").resolve()
    assert ws == expected_ws
    cache = get_cache_path()
    assert isinstance(cache, Path)
    assert cache == (expected_ws / "cache").resolve()


def test_get_workspace_path_is_idempotent_and_absolute(monkeypatch, tmp_path):
    fake_home = tmp_path / "another_home"
    fake_home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    p1 = get_workspace_path()
    p2 = get_workspace_path()
    assert p1 == p2
    assert p1.is_absolute()
    assert p1.name == ".vmkis"


def test_legacy_pykis_path_is_ignored(monkeypatch, tmp_path):
    """#33. ~/.pykis 만 있어도 ~/.vmkis 를 씁니다."""
    fake_home = tmp_path / "home"
    fake_home.mkdir()
    (fake_home / ".pykis").mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    assert get_workspace_path() == (fake_home / ".vmkis").resolve()
    assert get_cache_path() == (fake_home / ".vmkis" / "cache").resolve()
