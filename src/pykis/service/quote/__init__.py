"""Quote service — unified stock quote retrieval."""

from pykis.service.quote.models import Quote
from pykis.service.quote.service import get_quote

__all__ = [
    "Quote",
    "get_quote",
]
