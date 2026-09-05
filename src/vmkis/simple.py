from __future__ import annotations

from typing import Any

from vmkis.kis import VmKis


class SimpleKIS:
    """A very small facade for common user flows.

    This class intentionally implements a tiny, beginner-friendly API that
    delegates to a `VmKis` instance.
    """

    def __init__(self, kis: VmKis):
        self.kis = kis

    @classmethod
    def from_client(cls, kis: VmKis) -> SimpleKIS:
        return cls(kis)

    def get_price(self, symbol: str) -> Any:
        """Return the quote for `symbol`."""
        return self.kis.stock(symbol).quote()

    def get_balance(self) -> Any:
        """Return account balance object."""
        return self.kis.account().balance()

    def place_order(self, symbol: str, qty: int, price: Any = None) -> Any:
        """Place a basic order. If `price` is None, market order is used."""
        stock = self.kis.stock(symbol)
        if price is None:
            return stock.buy(qty=qty)
        return stock.buy(price=price, qty=qty)

    def cancel_order(self, order_obj: Any) -> Any:
        """Cancel an existing order object (delegates to order.cancel())."""
        return order_obj.cancel()
