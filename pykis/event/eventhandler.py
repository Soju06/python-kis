from typing import Callable, Generic, TypeVar

TSender = TypeVar("TSender")


class KisEventArgs:
    """이벤트 데이터"""

    pass


TEventArgs = TypeVar("TEventArgs", bound=KisEventArgs)


class KisEventHandler(Generic[TSender, TEventArgs]):
    """이벤트 핸들러"""

    handlers: set[Callable[[TSender, TEventArgs], None]]
    """이벤트 핸들러 목록"""

    def __init__(self, *handlers: Callable[[TSender, TEventArgs], None]):
        self.handlers = set(handlers)

    def add(self, handler: Callable[[TSender, TEventArgs], None]):
        """이벤트 핸들러를 추가합니다."""
        self.handlers.add(handler)

    def remove(self, handler: Callable[[TSender, TEventArgs], None]):
        """이벤트 핸들러를 제거합니다."""
        self.handlers.remove(handler)

    def clear(self):
        """이벤트 핸들러를 모두 제거합니다."""
        self.handlers.clear()

    def invoke(self, sender: TSender, e: TEventArgs):
        """이벤트를 발생시킵니다."""
        for handler in self.handlers:
            handler(sender, e)

    def __call__(self, sender: TSender, e: TEventArgs):
        """이벤트를 발생시킵니다."""
        self.invoke(sender, e)

    def __iadd__(self, handler: Callable[[TSender, TEventArgs], None]):
        self.add(handler)
        return self

    def __isub__(self, handler: Callable[[TSender, TEventArgs], None]):
        self.remove(handler)
        return self

    def __len__(self):
        return len(self.handlers)

    def __iter__(self):
        return iter(self.handlers)

    def __contains__(self, handler: Callable[[TSender, TEventArgs], None]):
        return handler in self.handlers

    def __bool__(self):
        return bool(self.handlers)

    def __repr__(self):
        return f"<EventHandler {len(self.handlers)} handlers>"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if isinstance(other, KisEventHandler):
            return self.handlers == other.handlers

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.handlers)
