from abc import ABCMeta, abstractmethod
from typing import Callable, Generic, TypeVar

from pykis.event.handler import KisEventFilter, KisEventTicket, TEventArgs, TSender

TEventType = TypeVar("TEventType", bound=str)

__all__ = [
    "KisWebsocketAdapter",
]


class KisWebsocketAdapter(Generic[TEventType, TSender, TEventArgs], metaclass=ABCMeta):
    """한국투자증권 웹소켓 어댑터"""

    @abstractmethod
    def on(
        self,
        event: TEventType,
        callback: Callable[[TSender, TEventArgs], None],
        where: KisEventFilter | None = None,
        once: bool = False,
    ) -> KisEventTicket[TSender, TEventArgs]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (TEventType): 이벤트 타입
            callback (Callable[[TSender, TEventArgs], None]): 콜백 함수
            where (KisEventFilter | None, optional): 이벤트 필터. Defaults to None.
            once (bool, optional): 한번만 실행할지 여부. Defaults to False.
        """
        raise NotImplementedError

    @abstractmethod
    def once(
        self,
        event: TEventType,
        callback: Callable[[TSender, TEventArgs], None],
        where: KisEventFilter | None = None,
    ) -> KisEventTicket[TSender, TEventArgs]:
        """
        웹소켓 이벤트 핸들러 등록

        Args:
            event (TEventType): 이벤트 타입
            callback (Callable[[TSender, TEventArgs], None]): 콜백 함수
            where (KisEventFilter | None, optional): 이벤트 필터. Defaults to None.
        """
        raise NotImplementedError
