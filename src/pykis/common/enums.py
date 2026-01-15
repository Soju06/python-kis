from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:

    class KisStrEnum(Protocol):
        value: str
        description: str

        @classmethod
        def docs(cls) -> dict[str, str]: ...

else:

    class KisStrEnum(StrEnum):
        __slots__ = ("description",)

        description: str

        def __new__(cls, value: str, description: str = "") -> "KisStrEnum":
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.description = description
            return obj

        @classmethod
        def docs(cls) -> dict[str, str]:
            return {member.value: member.description for member in cls}
