from abc import abstractmethod
from typing import Any


class KisForm:
    @abstractmethod
    def build(self, dict: dict[str, Any] | None = None) -> dict[str, Any]:
        """요청 폼을 생성합니다."""
        raise NotImplementedError
