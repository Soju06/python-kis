import importlib.metadata as real_metadata

from vmkis.utils import diagnosis


class DummyDist:
    def __init__(self, requires):
        self.requires = requires


def _set_vmkis_attrs(monkeypatch, version="1.2.3", package_name="vm-stock-kis"):
    # Ensure the runtime strings printed by diagnosis.check are stable
    monkeypatch.setattr(diagnosis.__env__, "__version__", version, raising=False)
    monkeypatch.setattr(diagnosis.__env__, "__package_name__", package_name, raising=False)


def test_check_no_dependencies(monkeypatch, capsys):
    _set_vmkis_attrs(monkeypatch, version="1.2.3", package_name="vm-stock-kis")

    # distribution() returns an object whose .requires is None
    monkeypatch.setattr(diagnosis.metadata, "distribution", lambda name: DummyDist(None))

    diagnosis.check()
    out = capsys.readouterr().out

    assert "Version: VmKis/1.2.3" in out
    assert "Installed Packages:" in out
    assert "No Dependencies" in out


def test_check_with_installed_dependency(monkeypatch, capsys):
    _set_vmkis_attrs(monkeypatch, version="2.0.0", package_name="vm-stock-kis")

    # distribution() returns a list with one dependency string
    monkeypatch.setattr(diagnosis.metadata, "distribution", lambda name: DummyDist(["foo>=1.0"]))

    # metadata.version should be called with package name 'foo'
    def fake_version(name):
        if name == "foo":
            return "2.5.1"
        raise real_metadata.PackageNotFoundError

    monkeypatch.setattr(diagnosis.metadata, "version", fake_version)

    diagnosis.check()
    out = capsys.readouterr().out

    assert "Version: VmKis/2.0.0" in out
    assert "Required: 1.0>=" in out  # parsing in module produces this pattern
    assert "Installed: 2.5.1" in out


def test_check_dependency_not_found(monkeypatch, capsys):
    _set_vmkis_attrs(monkeypatch, version="0.1.0", package_name="vm-stock-kis")

    monkeypatch.setattr(diagnosis.metadata, "distribution", lambda name: DummyDist(["bar==0.1.0"]))

    # metadata.version raises PackageNotFoundError for 'bar'
    def raise_not_found(name):
        raise real_metadata.PackageNotFoundError

    monkeypatch.setattr(diagnosis.metadata, "version", raise_not_found)

    diagnosis.check()
    out = capsys.readouterr().out

    assert "Version: VmKis/0.1.0" in out
    assert "Installed: Not Found" in out


def test_distribution_not_found(monkeypatch, capsys):
    _set_vmkis_attrs(monkeypatch, version="0.0.1", package_name="vm-stock-kis")

    # distribution() raises PackageNotFoundError
    def raise_dist_not_found(name):
        raise real_metadata.PackageNotFoundError

    monkeypatch.setattr(diagnosis.metadata, "distribution", raise_dist_not_found)

    diagnosis.check()
    out = capsys.readouterr().out

    assert "Package Not Found" in out
    # ensure the function returned early and did not print trailing separator
    assert "================================" not in out
