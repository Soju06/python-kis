from __future__ import annotations

from enum import StrEnum


class KisStrEnum(StrEnum):
    __slots__ = ("description",)

    description: str

    def __new__(cls, value: str, description: str = ""):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def docs(cls) -> dict[str, str]:
        return {member.value: member.description for member in cls}
