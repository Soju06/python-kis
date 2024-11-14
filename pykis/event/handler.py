import warnings
from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Generic,
    Iterable,
    Literal,
    Protocol,
    TypeVar,
    runtime_checkable,
)

from pykis.utils.reference import release_method

__all__ = [
    "EventCallback",
    "KisEventArgs",
    "KisEventFilter",
    "KisLambdaEventFilter",
    "KisMultiEventFilter",
    "KisEventCallback",
    "KisLambdaEventCallback",
    "KisEventTicket",
    "KisEventHandler",
]

TSender = TypeVar("TSender")
TCSender = TypeVar("TCSender", contravariant=True)


class KisEventArgs:
    """이벤트 데이터"""

    pass


TEventArgs = TypeVar("TEventArgs", bound=KisEventArgs)
TCEventArgs = TypeVar("TCEventArgs", bound=KisEventArgs, contravariant=True)


@runtime_checkable
class KisEventFilter(Protocol[TCSender, TCEventArgs]):
    """이벤트 필터"""

    @abstractmethod
    def __filter__(self, handler: "KisEventHandler", sender: TCSender, e: TCEventArgs) -> bool:
        """
        이벤트를 필터링합니다.

        Args:
            sender: 이벤트 발생 객체
            e: 이벤트 데이터

        Returns:
            `False`일 경우 이벤트를 전달합니다.
            `True`일 경우 이벤트를 무시합니다.
        """
        pass


class KisEventFilterBase(Generic[TSender, TEventArgs], metaclass=ABCMeta):
    """이벤트 필터"""

    @abstractmethod
    def __filter__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs) -> bool:
        """
        이벤트를 필터링합니다.

        Args:
            sender: 이벤트 발생 객체
            e: 이벤트 데이터

        Returns:
            `False`일 경우 이벤트를 전달합니다.
            `True`일 경우 이벤트를 무시합니다.
        """
        pass


class KisLambdaEventFilter(KisEventFilterBase[TSender, TEventArgs]):
    """람다 이벤트 필터"""

    def __init__(self, filter: Callable[[TSender, TEventArgs], bool]):
        self.filter = filter

    def __filter__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs) -> bool:
        return self.filter(sender, e)

    def __hash__(self) -> int:
        return hash(self.filter)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.filter!r})"

    def __str__(self) -> str:
        return repr(self)


class KisMultiEventFilter(KisEventFilterBase[TSender, TEventArgs]):
    """다중 이벤트 필터"""

    __slots__ = ("filters", "gate")

    def __init__(
        self,
        *filters: KisEventFilter[TSender, TEventArgs] | Callable[[TSender, TEventArgs], bool],
        gate: Literal["and", "or"] = "or",
    ):
        self.filters = filters
        self.gate = gate

    def __filter__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs) -> bool:
        results = (
            filter.__filter__(handler, sender, e) if isinstance(filter, KisEventFilter) else filter(sender, e)
            for filter in self.filters
        )

        if self.gate == "and":
            return all(results)
        elif self.gate == "or":
            return any(results)

        return False

    def __hash__(self) -> int:
        return hash((self.filters, self.gate))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(filter) for filter in self.filters)}, gate={self.gate!r})"

    def __str__(self) -> str:
        return repr(self)


class KisEventCallback(KisEventFilterBase[TSender, TEventArgs], metaclass=ABCMeta):
    """이벤트 콜백"""

    @abstractmethod
    def __callback__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs):
        """
        이벤트를 처리합니다.

        Args:
            sender: 이벤트 발생 객체
            e: 이벤트 데이터
        """
        pass


class KisLambdaEventCallback(KisEventCallback[TSender, TEventArgs]):
    """람다 이벤트 콜백"""

    callback: Callable[[TSender, TEventArgs], None]
    """이벤트 콜백"""
    where: KisEventFilter[TSender, TEventArgs] | Callable[[TSender, TEventArgs], bool] | None
    """이벤트 필터"""
    once: bool
    """실행 후 콜백 제거 여부"""

    def __init__(
        self,
        callback: Callable[[TSender, TEventArgs], None],
        where: KisEventFilter[TSender, TEventArgs] | Callable[[TSender, TEventArgs], bool] | None = None,
        once: bool = False,
    ):
        self.callback = callback
        self.where = where
        self.once = once

    def __filter__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs) -> bool:
        if self.where is None:
            return False

        return self.where.__filter__(handler, sender, e) if isinstance(self.where, KisEventFilter) else self.where(sender, e)

    def __callback__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs):
        if self.once:
            handler.remove(self)

        self.callback(sender, e)

    def __call__(self, handler: "KisEventHandler", sender: TSender, e: TEventArgs):
        if self.__filter__(handler, sender, e):
            self.__callback__(handler, sender, e)

    def __hash__(self) -> int:
        return hash((self.callback, self.where))

    def __del__(self):
        release_method(self.callback)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.callback!r}, where={self.where!r}, once={self.once!r})"

    def __str__(self) -> str:
        return repr(self)


EventCallback = Callable[[TSender, TEventArgs], None] | KisEventCallback[TSender, TEventArgs]


class KisEventTicket(Generic[TSender, TEventArgs]):
    """이벤트 티켓"""

    __slots__ = (
        "handler",
        "callback",
        "unsubscribed_callbacks",
        "_suppress_del",
    )

    handler: "KisEventHandler[TSender, TEventArgs]"
    """이벤트 핸들러"""
    callback: EventCallback[TSender, TEventArgs]
    """이벤트 콜백"""

    unsubscribed_callbacks: list[Callable[["KisEventTicket"], None]]
    """이벤트 콜백 제거 이벤트"""

    _suppress_del: bool
    """가비지 컬렉션에서 해지되지 않도록 합니다."""

    def __init__(
        self,
        handler: "KisEventHandler[TSender, TEventArgs]",
        callback: EventCallback[TSender, TEventArgs],
        unsubscribed_callbacks: list[Callable[["KisEventTicket"], None]] | None = None,
    ):
        self.handler = handler
        self.callback = callback
        self.unsubscribed_callbacks = unsubscribed_callbacks or []
        self._suppress_del = False

    @property
    def once(self) -> bool:
        """실행 후 콜백 제거 여부"""
        return isinstance(self.callback, KisLambdaEventCallback) and self.callback.once

    @property
    def registered(self) -> bool:
        """이벤트 핸들러에 등록되어 있는지 여부"""
        return self.callback in self.handler

    def unsubscribe(self):
        """이벤트 핸들러에서 제거합니다."""
        self.handler.remove(self.callback)

        if self.registered:
            for unsubscribed_callback in self.unsubscribed_callbacks:
                unsubscribed_callback(self)

    def suppress(self):
        """가비지 컬렉션에서 해지되지 않도록 합니다."""
        self._suppress_del = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.unsubscribe()

    def __del__(self):
        if not self._suppress_del:
            # 2.1.1 버전 이후부터는 티켓을 명시적으로 해지하지 않으면 경고 메시지를 출력합니다.
            if self.registered:
                warnings.warn(
                    f"Event ticket {self} was not explicitly unsubscribed, but was unsubscribed due to a resource release.",
                    UserWarning,
                )

            self.unsubscribe()

    def __repr__(self):
        return f"<{self.__class__.__name__} callback={self.callback}>"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if isinstance(other, KisEventTicket):
            return self.handler == other.handler and self.callback == other.callback

        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.handler, self.callback))


class KisEventHandler(Generic[TSender, TEventArgs]):
    """이벤트 핸들러"""

    handlers: set[EventCallback[TSender, TEventArgs]]
    """이벤트 핸들러 목록"""

    def __init__(self, *handlers: EventCallback[TSender, TEventArgs]):
        self.handlers = set(handlers)

    def add(self, handler: EventCallback[TSender, TEventArgs]) -> KisEventTicket[TSender, TEventArgs]:
        """이벤트 핸들러를 추가합니다."""
        self.handlers.add(handler)
        return KisEventTicket(self, handler)

    def on(
        self,
        handler: Callable[[TSender, TEventArgs], None],
        where: KisEventFilter[TSender, TEventArgs] | None = None,
        once: bool = False,
    ) -> KisEventTicket[TSender, TEventArgs]:
        """
        이벤트를 등록합니다.

        Args:
            handler: 이벤트 콜백
            where: 이벤트 필터
            once: 한 번만 실행할지 여부
        """
        return self.add(
            KisLambdaEventCallback(
                handler,
                where=where,
                once=once,
            )
        )

    def once(
        self,
        handler: Callable[[TSender, TEventArgs], None],
        where: KisEventFilter[TSender, TEventArgs] | None = None,
    ) -> KisEventTicket[TSender, TEventArgs]:
        """
        이벤트를 한 번만 실행합니다.

        Args:
            handler: 이벤트 콜백
            where: 이벤트 필터
        """
        return self.on(
            handler,
            where=where,
            once=True,
        )

    def remove(self, handler: EventCallback[TSender, TEventArgs]):
        """이벤트 핸들러를 제거합니다."""
        if isinstance(handler, KisEventCallback):
            del_method = getattr(handler, "__del__", None)

            if del_method is not None:
                del_method()
        else:
            release_method(handler)

        try:
            self.handlers.remove(handler)
        except KeyError:
            pass

    def clear(self):
        """이벤트 핸들러를 모두 제거합니다."""
        self.handlers.clear()

    def invoke(self, sender: TSender, e: TEventArgs):
        """이벤트를 발생시킵니다."""
        for handler in self.handlers.copy():
            if isinstance(handler, KisEventCallback):
                if not handler.__filter__(self, sender, e):
                    handler.__callback__(self, sender, e)
            else:
                handler(sender, e)

    def __call__(self, sender: TSender, e: TEventArgs):
        """이벤트를 발생시킵니다."""
        self.invoke(sender, e)

    def __iadd__(self, handler: EventCallback[TSender, TEventArgs]):
        self.add(handler).suppress()
        return self

    def __isub__(self, handler: EventCallback[TSender, TEventArgs]):
        self.remove(handler)
        return self

    def __len__(self):
        return len(self.handlers)

    def __iter__(self) -> Iterable[EventCallback[TSender, TEventArgs]]:
        return iter(self.handlers)

    def __contains__(self, handler: EventCallback[TSender, TEventArgs]):
        return handler in self.handlers

    def __bool__(self):
        return bool(self.handlers)

    def __repr__(self):
        return f"<{self.__class__.__name__} {len(self.handlers)} handlers>"

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
