__all__ = [
    "CreateLimitOrderRequest",
    "OrderType",
    "CreateStockMarketOrderRequest",
    "CreateStopLimitOrderRequest",
    "CreateStopMarketOrderRequest",
    "CancelOrderRequest",
    "ActiveOrdersRequest",
    "ExecutedOrderHistoryRequest",
    "ExecutedOrderDealsRequest",
    "ExecutedOrdersByMarket",
]

from enum import Enum
from typing import Optional

from pydantic.main import BaseModel


class OrderType(str, Enum):
    buy = "buy"
    sell = "sell"


class CreateLimitOrderRequest(BaseModel):
    market: str
    side: OrderType
    amount: str
    price: str
    clientOrderId: Optional[str]


class CreateStockMarketOrderRequest(BaseModel):
    market: str
    side: OrderType
    amount: str
    clientOrderId: Optional[str]


class CreateStopLimitOrderRequest(BaseModel):
    market: str
    side: OrderType
    amount: str
    price: str
    activation_price: str
    clientOrderId: Optional[str]


class CreateStopMarketOrderRequest(BaseModel):
    market: str
    side: OrderType
    amount: str
    activation_price: str
    clientOrderId: Optional[str]


class CancelOrderRequest(BaseModel):
    market: str
    orderId: int


class ActiveOrdersRequest(BaseModel):
    market: str
    limit: Optional[int]  # Default in api: 50, Min: 1, Max: 100
    offset: Optional[int]  # Default in api: 0, Min: 0, Max: 10000


class ExecutedOrderHistoryRequest(ActiveOrdersRequest):
    market: Optional[str]


class ExecutedOrderDealsRequest(BaseModel):
    orderId: int
    limit: Optional[int]  # Default in api: 50, Min: 1, Max: 100
    offset: Optional[int]  # Default in api: 0, Min: 0, Max: 10000


class ExecutedOrdersByMarket(ExecutedOrderHistoryRequest):
    pass
