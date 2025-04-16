"""Response models for the WhiteBit Private API."""

from decimal import Decimal
from typing import Any, Dict, List

from pydantic import BaseModel


class TradingBalanceItem(BaseModel):
    """Trading balance item model.

    Attributes:
        ticker: Ticker of the currency
        available: Available balance
        freeze: Frozen balance
    """

    ticker: str
    available: Decimal
    freeze: Decimal


class TradingBalanceList(BaseModel):
    """Trading balance list model.

    Attributes:
        result: List of trading balance items
    """

    result: List[TradingBalanceItem]


class CreateOrderResponse(BaseModel):
    """Create order response model.

    Attributes:
        amount: Order amount
        dealFee: Deal fee
        dealMoney: Deal money
        dealStock: Deal stock
        left: Amount left
        makerFee: Maker fee
        market: Market
        orderId: Order ID
        clientOrderId: Client order ID
        price: Price
        side: Side (buy or sell)
        takerFee: Taker fee
        timestamp: Timestamp
        type: Order type
    """

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
    """Cancel order response model.

    Attributes:
        activation_price: Activation price for stop orders
    """

    activation_price: str


class ExecutedOrdersResponse(BaseModel):
    """Executed orders response model.

    Attributes:
        result: Dictionary with executed orders information
    """

    result: Dict[str, Any]


class ExecutedDealsResponse(ExecutedOrdersResponse):
    """Executed deals response model."""

    pass


class ExecutedOrdersByMarketResponse(ExecutedOrdersResponse):
    """Executed orders by market response model."""

    pass
