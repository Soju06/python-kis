from collections.abc import Iterable
from types import NoneType
from typing import Any, Protocol, TypeVar, get_args, runtime_checkable

from vmkis import logging
from vmkis.responses.dynamic import KisNoneValueError, KisType, empty
from vmkis.responses.types import KisAny

__all__ = [
    "TWebsocketResponse",
    "KisWebsocketResponse",
]


@runtime_checkable
class KisWebsocketResponseProtocol(Protocol):
    """한국투자증권 실시간 응답 클래스"""

    @property
    def __data__(self) -> list[str]:
        """원본 데이터"""
        ...

    def raw(self) -> list[str]:
        """원본 응답 데이터를 반환합니다."""
        ...


class KisWebsocketResponse:
    """한국투자증권 실시간 응답 클래스"""

    __fields__: list[KisType | type[KisType] | Any | None] = []
    """파싱할 필드 목록"""

    __data__: list[str]
    """원본 데이터"""

    def __pre_init__(self, data: list[str]) -> None:
        pass

    def __post_init__(self) -> None:
        pass

    def raw(self) -> list[str]:
        """원본 응답 데이터를 반환합니다."""
        return self.__data__

    @classmethod
    def parse(
        cls,
        data: str,
        /,
        count: int | None = None,
        split: str = "^",
        *,
        response_type: "type[TWebsocketResponse]",
    ) -> "Iterable[TWebsocketResponse]":
        """
        데이터를 파싱합니다.

        Args:
            data (str): 데이터
            count (int | None): 데이터 갯수
            split (str): 데이터 구분자
            response_type (Callable[..., TWebsocketResponse]): 응답 클래스
        """
        items = data.split(split)
        fields = getattr(response_type, "__fields__", None)

        if not fields:
            response = response_type()

            if (pre_init := getattr(response, "__pre_init__", None)) is not None:
                pre_init(items)

            response.__data__ = items

            if (post_init := getattr(response, "__post_init__", None)) is not None:
                post_init()

            yield response
            return

        if len(items) % len(fields) != 0:
            raise ValueError(f"Invalid data length: {len(items)}")

        # 필드 갯수 검증
        if count is not None:
            if len(items) // len(fields) != count:
                raise ValueError(f"Invalid data count: {len(items) / len(fields)}")
        else:
            count = len(items) // len(fields)

        # 각 아이템의 필드를 묶음 [A, A, B, B] -> [(A, A), (B, B)]
        try:
            for values in zip(*[iter(items)] * len(fields), strict=False):
                values: list[str]
                response = response_type()

                if (pre_init := getattr(response, "__pre_init__", None)) is not None:
                    pre_init(values)

                response.__data__ = values

                annotation = response_type.__annotations__

                for i, (field, value) in enumerate(zip(fields, values, strict=False)):
                    if field is None:
                        continue

                    if isinstance(field, type):
                        field = field.default_type()

                    if field.field is None:
                        logging.logger.warning(f"{response_type.__name__}[{i}] 필드의 이름이 지정되지 않았습니다.")
                        continue

                    try:
                        if isinstance(field, KisAny) and field.absolute:
                            value = field.transform(values)
                        else:
                            value = field.transform(value)

                        setattr(response, field.field, value)
                    except KisNoneValueError:
                        nullable = NoneType in get_args(anno) if (anno := annotation.get(field.field)) else False

                        default_value = None if field.default is empty else field.default

                        if callable(default_value):
                            default_value = default_value()

                        if default_value is None and not nullable:
                            # KisNoneValueError는 "값이 비어 있다"는 신호일 뿐 오류 원인이
                            # 아니므로 체인을 끊는다.
                            raise ValueError(
                                f"{response_type.__name__}.{field.field} 필드가 None일 수 없습니다."
                            ) from None

                        setattr(response, field.field, default_value)

                    except Exception as e:
                        raise ValueError(
                            f"{response_type.__name__}.{field.field} 필드를 변환하는 중 오류가 발생했습니다.\n→ {type(e).__name__}: {e}"
                        ) from e

                if (post_init := getattr(response, "__post_init__", None)) is not None:
                    post_init()

                yield response
        except Exception as e:
            raise ValueError(f"데이터 파싱 중 오류가 발생했습니다.\n→ {type(e).__name__}: {e}") from e


TWebsocketResponse = TypeVar("TWebsocketResponse", bound=KisWebsocketResponseProtocol)

#: TR ID -> 실시간 응답 클래스. **client 가 소유하고 api 가 자기등록합니다.**
#:
#: 예전에는 `api/websocket/__init__.py` 가 이 dict 를 소유하고
#: `client/websocket.py` 가 그것을 import 했습니다. 통신 계층이 상위 계층에
#: 의존하는 역방향 간선이었고(이슈 #17), TR 하나를 추가할 때마다 client 까지
#: 함께 바뀌었습니다.
#:
#: 여기(responses)에 두면 client 와 api 양쪽에서 **정방향** 참조가 됩니다.
WEBSOCKET_RESPONSES_MAP: dict[str, type["KisWebsocketResponse"]] = {}

#: 수신 본문이 AES 로 암호화되는 TR ID.
#:
#: 예전에는 `client/websocket.py` 에 튜플로 하드코딩돼 있어, 암호화 TR 을
#: 추가할 때 그 파일도 함께 고쳐야 했습니다.
ENCRYPTED_TR_IDS: set[str] = set()


def register_websocket_response(*tr_ids: str, encrypted: bool = False):
    """실시간 응답 클래스를 TR ID 에 등록하는 데코레이터.

    **등록하지 않으면 구독 메시지는 전송되지만 수신 이벤트가 조용히
    버려집니다.** 클래스 정의 바로 위에 붙여 두면 빠뜨리기 어렵습니다.

        @register_websocket_response("H0STCNT0")
        class KisDomesticRealtimePrice(KisWebsocketResponse, ...):
            ...

    Args:
        *tr_ids: 이 클래스가 처리할 TR ID. 실전/모의처럼 여러 개일 수 있습니다.
        encrypted: 수신 본문이 암호화되는 TR 인지 여부.
    """

    def decorator(cls):
        for tr_id in tr_ids:
            WEBSOCKET_RESPONSES_MAP[tr_id] = cls

            if encrypted:
                ENCRYPTED_TR_IDS.add(tr_id)

        return cls

    return decorator
