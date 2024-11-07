from abc import ABCMeta, abstractmethod
from typing import Any

__all__ = [
    "KisForm",
]


class KisForm(metaclass=ABCMeta):
    @abstractmethod
    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        """요청 폼을 생성합니다."""
        ...
