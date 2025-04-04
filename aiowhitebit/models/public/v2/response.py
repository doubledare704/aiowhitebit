"""Response models for the WhiteBit Public API v2."""

from datetime import datetime
from typing import List

from pydantic import BaseModel

from aiowhitebit.models.base import BasePublicV2Response
from aiowhitebit.models.public.v1.response import OrderDepth


class Market(BaseModel):
    """Market information model for v2 API

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
        minTotal: Minimal total amount
        tradesEnabled: Whether trades are enabled for this market
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
    minTotal: float
    tradesEnabled: bool

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class MarketInfo(BasePublicV2Response):
    """Market information response model for v2 API

    Attributes:
        result: List of market information items
    """

    result: List[Market]

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class Ticker(BaseModel):
    """Ticker information model for v2 API

    Attributes:
        lastUpdateTimestamp: Last update timestamp
        tradingPairs: Trading pairs (e.g. BTC_USDT)
        lastPrice: Last price
        lowestAsk: Lowest ask price
        highestBid: Highest bid price
        baseVolume24h: Base volume in 24 hours
        quoteVolume24h: Quote volume in 24 hours
        tradesEnabled: Whether trades are enabled for this market
    """

    lastUpdateTimestamp: datetime
    tradingPairs: str
    lastPrice: float
    lowestAsk: float
    highestBid: float
    baseVolume24h: float
    quoteVolume24h: float
    tradesEnabled: bool

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class Tickers(BasePublicV2Response):
    """Tickers response model for v2 API

    Attributes:
        result: List of ticker items
    """

    result: List[Ticker]

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class RecentTrade(BaseModel):
    """Recent trade model for v2 API

    Attributes:
        tradeId: Trade ID
        price: Trade price
        volume: Trade volume
        time: Trade time
        isBuyerMaker: Whether the buyer is the maker
    """

    tradeId: int
    price: float
    volume: float
    time: datetime
    isBuyerMaker: bool

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class RecentTrades(BasePublicV2Response):
    """Recent trades response model for v2 API

    Attributes:
        result: List of recent trade items
    """

    result: List[RecentTrade]

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class Fee(BaseModel):
    """Fee model for v2 API

    Attributes:
        makerFee: Maker fee
        takerFee: Taker fee
    """

    makerFee: float
    takerFee: float

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class FeeResponse(BasePublicV2Response):
    """Fee response model for v2 API

    Attributes:
        result: Fee information
    """

    result: Fee

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class Asset(BaseModel):
    """Asset model for v2 API

    Attributes:
        asset_name: Asset name
        id: Asset ID
        lastUpdateTimestamp: Last update timestamp
        name: Asset display name
        canWithdraw: Whether withdrawals are enabled
        canDeposit: Whether deposits are enabled
        minWithdrawal: Minimum withdrawal amount
        maxWithdrawal: Maximum withdrawal amount
        makerFee: Maker fee
        takerFee: Taker fee
    """

    asset_name: str
    id: str
    lastUpdateTimestamp: datetime
    name: str
    canWithdraw: bool
    canDeposit: bool
    minWithdrawal: float
    maxWithdrawal: float
    makerFee: float
    takerFee: float

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class AssetStatus(BasePublicV2Response):
    """Asset status response model for v2 API

    Attributes:
        result: List of asset items
    """

    result: List[Asset]

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data


class OrderDepthV2(OrderDepth):
    """Order depth model for v2 API

    Attributes:
        asks: List of ask orders (price, amount pairs)
        bids: List of bid orders (price, amount pairs)
        lastUpdateTimestamp: Last update timestamp
    """

    lastUpdateTimestamp: datetime

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
        extra = "ignore"  # Ignores extra fields in the input data
