from typing import Generic, TypeVar

TProtocol = TypeVar("TProtocol", bound=object)


class Checkable(Generic[TProtocol]):
    def __init__(self, _: type[TProtocol]):
        pass
