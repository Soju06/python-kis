from .kospi import KisKospi, KisKospiItem
from .kosdaq import KisKosdaq, KisKosdaqItem
from .sector import KisSector, KisSectorItem
from .kstock import KisKStockMarket, KisKStockItem

MARKETS = {
    "kospi": KisKospi,
    "kosdaq": KisKosdaq,
    "sector": KisSector,
}

MARKET_TYPE = KisKospi | KisKosdaq | KisSector
MARKET_ITEM_TYPE = KisKospiItem | KisKosdaqItem | KisSectorItem
