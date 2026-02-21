"""Quote service — orchestration layer for stock quote retrieval."""

from __future__ import annotations

from pykis.api.raw import ensure_registry
from pykis.api.raw.types import EndpointAsyncClient, EndpointClient
from pykis.service.enums import Exchange
from pykis.service.quote._domestic import map_domestic_quote
from pykis.service.quote._overseas import map_overseas_quote
from pykis.service.quote.models import Quote

# L0 endpoint UUIDs
_DOMESTIC_QUOTE_ENDPOINT_ID = "995f745a-aa8a-491b-85ef-0d4697094b58"
_OVERSEAS_QUOTE_ENDPOINT_ID = "3eeac674-072d-4674-a5a7-f0ed01194a81"


def get_quote_sync(
    client: EndpointClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    """Retrieve a stock quote (synchronous).

    Routes to the appropriate domestic or overseas L0 endpoint based on exchange.
    """
    if exchange.is_domestic:
        return _get_domestic_quote_sync(client, symbol, exchange)
    return _get_overseas_quote_sync(client, symbol, exchange)


async def get_quote(
    client: EndpointAsyncClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    """Retrieve a stock quote (async).

    Routes to the appropriate domestic or overseas L0 endpoint based on exchange.
    """
    if exchange.is_domestic:
        return await _get_domestic_quote(client, symbol, exchange)
    return await _get_overseas_quote(client, symbol, exchange)


def _get_domestic_quote_sync(
    client: EndpointClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    from pykis.service._enum_map import EXCHANGE_TO_DOMESTIC_MARKET_CODE

    registry = ensure_registry()
    endpoint = registry[_DOMESTIC_QUOTE_ENDPOINT_ID]
    market_code = EXCHANGE_TO_DOMESTIC_MARKET_CODE[exchange]

    response, _ = endpoint.call(client, {
        "FID_COND_MRKT_DIV_CODE": market_code,
        "FID_INPUT_ISCD": symbol,
    })
    return map_domestic_quote(response.output, symbol, exchange)


async def _get_domestic_quote(
    client: EndpointAsyncClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    from pykis.service._enum_map import EXCHANGE_TO_DOMESTIC_MARKET_CODE

    registry = ensure_registry()
    endpoint = registry[_DOMESTIC_QUOTE_ENDPOINT_ID]
    market_code = EXCHANGE_TO_DOMESTIC_MARKET_CODE[exchange]

    response, _ = await endpoint.acall(client, {
        "FID_COND_MRKT_DIV_CODE": market_code,
        "FID_INPUT_ISCD": symbol,
    })
    return map_domestic_quote(response.output, symbol, exchange)


def _get_overseas_quote_sync(
    client: EndpointClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    from pykis.service._enum_map import EXCHANGE_TO_OVERSEAS_EXCD

    registry = ensure_registry()
    endpoint = registry[_OVERSEAS_QUOTE_ENDPOINT_ID]
    excd = EXCHANGE_TO_OVERSEAS_EXCD[exchange]

    response, _ = endpoint.call(client, {
        "EXCD": excd,
        "SYMB": symbol,
    })
    return map_overseas_quote(response.output, symbol, exchange)


async def _get_overseas_quote(
    client: EndpointAsyncClient,
    symbol: str,
    exchange: Exchange,
) -> Quote:
    from pykis.service._enum_map import EXCHANGE_TO_OVERSEAS_EXCD

    registry = ensure_registry()
    endpoint = registry[_OVERSEAS_QUOTE_ENDPOINT_ID]
    excd = EXCHANGE_TO_OVERSEAS_EXCD[exchange]

    response, _ = await endpoint.acall(client, {
        "EXCD": excd,
        "SYMB": symbol,
    })
    return map_overseas_quote(response.output, symbol, exchange)
