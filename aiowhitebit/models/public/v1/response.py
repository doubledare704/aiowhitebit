"""Response models for the WhiteBit Public API v1."""

from pydantic import BaseModel

from aiowhitebit.models.base import BasePublicV1Response


class Market(BaseModel):
    """Market information model for v1 API.

    Attributes:
        name: Name of market pair (e.g. BTC_USDT)
        stock: Ticker of stock currency (e.g. BTC)
        money: Ticker of money currency (e.g. USDT)
        stockPrec: Precision of stock currency
        moneyPrec: Precision of money currency
        feePrec: Precision of fee
        makerFee: Default maker fee ratio
        takerFee: Default taker fee ratio
        minAmount: Minimal amount of stock to trade
    """

    name: str
    stock: str
    money: str
    stockPrec: int
    moneyPrec: int
    feePrec: int
    makerFee: float
    takerFee: float
    minAmount: float


class MarketInfo(BasePublicV1Response):
    """Market information response model for v1 API.

    Attributes:
        result: List of market information items
    """

    result: list[Market]


class Ticker(BaseModel):
    """Ticker information model for v1 API.

    Attributes:
        name: Name of market pair (e.g. BTC_USDT)
        bid: Highest bid
        ask: Lowest ask
        low: Lowest price for 24h
        high: Highest price for 24h
        last: Last deal price
        vol: Volume in stock currency
        deal: Volume in money currency
        change: Change in percent between open and last prices
        at: Timestamp in seconds
    """

    name: str
    bid: float
    ask: float
    low: float
    high: float
    last: float
    vol: float
    deal: float
    change: float
    at: int


class Tickers(BasePublicV1Response):
    """Tickers response model for v1 API.

    Attributes:
        result: List of ticker items
    """

    result: list[Ticker]


class MarketSingle(BaseModel):
    """Single market activity information model for v1 API.

    Attributes:
        open: Open price for day
        bid: The highest bid currently available
        ask: The lowest ask currently available
        low: Lowest price for day
        high: Highest price for day
        last: Latest deal price
        volume: Volume in stock
        deal: Volume in money
        change: Change between open and close price in percentage
    """

    open: float
    bid: float
    ask: float
    low: float
    high: float
    last: float
    volume: float
    deal: float
    change: float


class MarketSingleResponse(BasePublicV1Response):
    """Single market response model for v1 API.

    Attributes:
        result: Market information for a single market
    """

    result: MarketSingle


class KlineItem(BaseModel):
    """Kline (candlestick) information model for v1 API.

    Attributes:
        time_seconds: Time in seconds
        open: Open price
        close: Close price
        high: High price
        low: Low price
        volume_stock: Volume in stock currency
        volume_mmoney: Volume in money currency
    """

    time_seconds: int
    open: float
    close: float
    high: float
    low: float
    volume_stock: float
    volume_mmoney: float


class Kline(BasePublicV1Response):
    """Kline response model for v1 API.

    Attributes:
        result: List of kline (candlestick) items
    """

    result: list[KlineItem]


class Symbols(BasePublicV1Response):
    """Symbols response model for v1 API.

    Attributes:
        result: List of available market symbols (e.g. BTC_USDT)
    """

    result: list[str]


class OrderDepthItem(BaseModel):
    """Order depth item model for v1 API.

    Attributes:
        price: Price level
        amount: Amount at this price level
    """

    price: float
    amount: float


class OrderDepth(BaseModel):
    """Order depth model for v1 API.

    Attributes:
        asks: List of ask orders (price, amount pairs)
        bids: List of bid orders (price, amount pairs)
    """

    asks: list[OrderDepthItem]
    bids: list[OrderDepthItem]


class TradeHistoryItem(BaseModel):
    """Trade history item model for v1 API.

    Attributes:
        id: Deal id
        time: Deal time in seconds
        price: Deal price
        amount: Deal amount
        type: Deal type (buy or sell)
    """

    id: int
    time: float
    price: float
    amount: float
    type: str


class TradeHistory(BasePublicV1Response):
    """Trade history response model for v1 API.

    Attributes:
        result: List of trade history items
    """

    result: list[TradeHistoryItem]
