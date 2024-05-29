from typing import Generic, TypeVar

TProtocol = TypeVar("TProtocol", bound=object)


class Checkable(Generic[TProtocol]):

    __slots__ = []

    def __init__(self, _: type[TProtocol]):
        pass
