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
]

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
