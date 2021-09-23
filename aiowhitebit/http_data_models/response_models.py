__all__ = [
    "TradingBalanceItem",
    "TradingBalanceList",
    "CreateOrderResponse",
    "CancelOrderResponse",
    "ExecutedOrdersResponse",
    "ExecutedDealsResponse",
    "ExecutedOrdersByMarketResponse",
]

from decimal import Decimal
from typing import List, Optional

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
