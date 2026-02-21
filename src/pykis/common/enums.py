from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, ClassVar, Protocol

if TYPE_CHECKING:

    class KisStrEnum(Protocol):
        value: str
        description: str
        __members__: ClassVar[dict[str, "KisStrEnum"]]

        def __getattribute__(self, name: str): ...

        @classmethod
        def docs(cls) -> dict[str, str]: ...

else:

    class KisStrEnum(StrEnum):
        __slots__ = ("description",)

        description: str
        __members__: ClassVar[dict[str, "KisStrEnum"]]

        def __new__(cls, value: str, description: str = "") -> "KisStrEnum":
            obj = str.__new__(cls, value)
            obj._value_ = value
            obj.description = description
            return obj

        def __getattribute__(self, name: str):
            if name == "__doc__":
                return object.__getattribute__(self, "description") or None
            return super().__getattribute__(name)

        @classmethod
        def docs(cls) -> dict[str, str]:
            return {member.value: member.description for member in cls.__members__.values()}
