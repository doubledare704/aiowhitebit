__all__ = [
    "TradingBalanceItem",
    "TradingBalanceList",
    "CreateOrderResponse",
    "CancelOrderResponse",
    "ExecutedOrdersResponse",
    "ExecutedDealsResponse",
    "ExecutedOrdersByMarketResponse",
    "TickersV1",
    "MarketInfoV1",
    "TickerItem",
    "MarketSingleResponse",
    "MarketSingle",
    "KlineV1",
    "KlineItem",
    "SymbolsV1",
    "OrderDepthItem",
    "OrderDepthV1",
    "TradeHistoryItem",
    "TradeHistoryV1",
    "MarketInfoV2",
    "TickerItemV2",
    "TickersV2",
    "RecentTradesV2",
    "FeeV2",
    "AssetStatusV2",
    "AssetItemV2",
    "OrderDepthV2",
]

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any

from pydantic import BaseModel


class TradingBalanceItem(BaseModel):
    ticker: Optional[str]
    available: Decimal
    freeze: Decimal


class TradingBalanceList(BaseModel):
    result: List[TradingBalanceItem]


class CreateOrderResponse(BaseModel):
    amount: Decimal
    dealFee: Decimal
    dealMoney: Decimal
    dealStock: Decimal
    left: Decimal
    makerFee: Decimal
    market: str
    orderId: int
    clientOrderId: str
    price: str
    side: str
    takerFee: Decimal
    timestamp: float
    type: str


class CancelOrderResponse(CreateOrderResponse):
    activation_price: str


class ExecutedOrdersResponse(BaseModel):
    result: dict


class ExecutedDealsResponse(ExecutedOrdersResponse):
    pass


class ExecutedOrdersByMarketResponse(ExecutedOrdersResponse):
    pass


class BasePublicV1(BaseModel):
    success: bool
    message: Any


class MarketItem(BaseModel):
    name: str
    stock: str
    money: str
    stockPrec: int
    moneyPrec: int
    feePrec: int
    makerFee: float
    takerFee: float
    minAmount: float


class MarketInfoV1(BasePublicV1):
    result: List[MarketItem]


class TickerItem(BaseModel):
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


class TickersV1(BasePublicV1):
    result: List[TickerItem]


class MarketSingle(BaseModel):
    open: float
    bid: float
    ask: float
    low: float
    high: float
    last: float
    volume: float
    deal: float
    change: float


class MarketSingleResponse(BasePublicV1):
    result: MarketSingle


class KlineItem(BaseModel):
    time_seconds: int
    open: float
    close: float
    high: float
    low: float
    volume_stock: float
    volume_mmoney: float


class KlineV1(BasePublicV1):
    result: List[KlineItem]


class SymbolsV1(BasePublicV1):
    result: List[str]


class OrderDepthItem(BaseModel):
    price: float
    amount: float


class OrderDepthV1(BaseModel):
    asks: List[OrderDepthItem]
    bids: List[OrderDepthItem]


class TradeHistoryItem(BaseModel):
    id: int
    time: float
    price: float
    amount: float
    type: str


class TradeHistoryV1(BasePublicV1):
    result: List[TradeHistoryItem]


class MarketItemV2(BaseModel):
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


class MarketInfoV2(BasePublicV1):
    result: List[MarketItemV2]


class TickerItemV2(BaseModel):
    lastUpdateTimestamp: datetime
    tradingPairs: str
    lastPrice: float
    lowestAsk: float
    highestBid: float
    baseVolume24h: float
    quoteVolume24h: float
    tradesEnabled: bool


class TickersV2(BasePublicV1):
    result: List[TickerItemV2]


class RecentTradeItem(BaseModel):
    tradeId: int
    price: float
    volume: float
    time: datetime
    isBuyerMaker: bool


class RecentTradesV2(BasePublicV1):
    result: List[RecentTradeItem]


class FeeItem(BaseModel):
    makerFee: float
    takerFee: float


class FeeV2(BasePublicV1):
    result: FeeItem


class AssetItemV2(BaseModel):
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


class AssetStatusV2(BasePublicV1):
    result: List[AssetItemV2]


class OrderDepthV2(OrderDepthV1):
    lastUpdateTimestamp: datetime
