from pathlib import Path

_WORKSPACE_NAME = ".vmkis"


def get_workspace_path() -> Path:
    """VmKis의 기본 작업공간 폴더를 반환합니다."""
    return (Path.home() / _WORKSPACE_NAME).resolve()


def get_cache_path() -> Path:
    """VmKis의 캐시 폴더를 반환합니다."""
    return (get_workspace_path() / "cache").resolve()
