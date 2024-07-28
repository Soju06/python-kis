from pathlib import Path


def get_workspace_path() -> Path:
    """Pykis의 기본 작업공간 폴더를 반환합니다."""
    return (Path.home() / ".pykis").resolve()


def get_cache_path() -> Path:
    """Pykis의 캐시 폴더를 반환합니다."""
    return (get_workspace_path() / "cache").resolve()
