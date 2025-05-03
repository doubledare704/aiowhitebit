"""Request models for the WhiteBit Private API."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, field_validator


class OrderType(str, Enum):
    """Order type enum.

    Attributes:
        buy: Buy order
        sell: Sell order
    """

    buy = "buy"
    sell = "sell"


class CreateLimitOrderRequest(BaseModel):
    """Create limit order request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        side: Order side (buy or sell)
        amount: Order amount
        price: Order price
        clientOrderId: Client order ID (optional)
    """

    market: str
    side: OrderType
    amount: str
    price: str
    clientOrderId: Optional[str] = None

    @field_validator("market", "amount", "price")
    @classmethod
    def validate_required_fields(cls, v: Any) -> Any:
        """Validate that required fields are not empty.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is empty.
        """
        if not v:
            raise ValueError("This field is required and cannot be empty")
        return v


class CreateStockMarketOrderRequest(BaseModel):
    """Create stock market order request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        side: Order side (buy or sell)
        amount: Order amount
        clientOrderId: Client order ID (optional)
    """

    market: str
    side: OrderType
    amount: str
    clientOrderId: Optional[str] = None

    @field_validator("market", "amount")
    @classmethod
    def validate_required_fields(cls, v: Any) -> Any:
        """Validate that required fields are not empty.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is empty.
        """
        if not v:
            raise ValueError("This field is required and cannot be empty")
        return v


class CreateStopLimitOrderRequest(BaseModel):
    """Create stop limit order request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        side: Order side (buy or sell)
        amount: Order amount
        price: Order price
        activation_price: Activation price
        clientOrderId: Client order ID (optional)
    """

    market: str
    side: OrderType
    amount: str
    price: str
    activation_price: str
    clientOrderId: Optional[str] = None

    @field_validator("market", "amount", "price", "activation_price")
    @classmethod
    def validate_required_fields(cls, v: Any) -> Any:
        """Validate that required fields are not empty.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is empty.
        """
        if not v:
            raise ValueError("This field is required and cannot be empty")
        return v


class CreateStopMarketOrderRequest(BaseModel):
    """Create stop market order request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        side: Order side (buy or sell)
        amount: Order amount
        activation_price: Activation price
        clientOrderId: Client order ID (optional)
    """

    market: str
    side: OrderType
    amount: str
    activation_price: str
    clientOrderId: Optional[str] = None

    @field_validator("market", "amount", "activation_price")
    @classmethod
    def validate_required_fields(cls, v: Any) -> Any:
        """Validate that required fields are not empty.

        Args:
            v: The value to validate.

        Returns:
            The validated value.

        Raises:
            ValueError: If the value is empty.
        """
        if not v:
            raise ValueError("This field is required and cannot be empty")
        return v


class CancelOrderRequest(BaseModel):
    """Cancel order request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        orderId: Order ID
    """

    market: str
    orderId: int

    @field_validator("market")
    @classmethod
    def validate_market(cls, v: Any) -> Any:
        """Validate that market parameter is not empty.

        Args:
            v: The market value to validate.

        Returns:
            The validated market value.

        Raises:
            ValueError: If the market value is empty.
        """
        if not v:
            raise ValueError("Market parameter is required")
        return v

    @field_validator("orderId")
    @classmethod
    def validate_order_id(cls, v: Any) -> Any:
        """Validate that order ID is a positive integer.

        Args:
            v: The order ID to validate.

        Returns:
            The validated order ID.

        Raises:
            ValueError: If the order ID is not a positive integer.
        """
        if v <= 0:
            raise ValueError("Order ID must be a positive integer")
        return v


class ActiveOrdersRequest(BaseModel):
    """Active orders request model.

    Attributes:
        market: Market (e.g. BTC_USDT)
        limit: Limit of results (default: 50, min: 1, max: 100)
        offset: Offset (default: 0, min: 0, max: 10000)
    """

    market: str
    limit: Optional[int] = None
    offset: Optional[int] = None

    @field_validator("market")
    @classmethod
    def validate_market(cls, v: Any) -> Any:
        """Validate that market parameter is not empty.

        Args:
            v: The market value to validate.

        Returns:
            The validated market value.

        Raises:
            ValueError: If the market value is empty.
        """
        if not v:
            raise ValueError("Market parameter is required")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Any) -> Any:
        """Validate that limit is within allowed range.

        Args:
            v: The limit value to validate.

        Returns:
            The validated limit value.

        Raises:
            ValueError: If the limit is not within the allowed range.
        """
        if v is not None and (v < 1 or v > 100):
            raise ValueError("Limit must be between 1 and 100")
        return v

    @field_validator("offset")
    @classmethod
    def validate_offset(cls, v: Any) -> Any:
        """Validate that offset is within allowed range.

        Args:
            v: The offset value to validate.

        Returns:
            The validated offset value.

        Raises:
            ValueError: If the offset is not within the allowed range.
        """
        if v is not None and (v < 0 or v > 10000):
            raise ValueError("Offset must be between 0 and 10000")
        return v


class ExecutedOrderHistoryRequest(ActiveOrdersRequest):
    """Executed order history request model.

    Attributes:
        market: Market (e.g. BTC_USDT) (optional)
        limit: Limit of results (default: 50, min: 1, max: 100)
        offset: Offset (default: 0, min: 0, max: 10000)
    """

    market: Optional[str] = None

    @field_validator("market")
    @classmethod
    def validate_market(cls, v: Any) -> Any:
        """Validate market parameter (optional for this request).

        Args:
            v: The market value to validate.

        Returns:
            The validated market value.
        """
        # Market is optional for this request
        return v


class ExecutedOrderDealsRequest(BaseModel):
    """Executed order deals request model.

    Attributes:
        orderId: Order ID
        limit: Limit of results (default: 50, min: 1, max: 100)
        offset: Offset (default: 0, min: 0, max: 10000)
    """

    orderId: int
    limit: Optional[int] = None
    offset: Optional[int] = None

    @field_validator("orderId")
    @classmethod
    def validate_order_id(cls, v: Any) -> Any:
        """Validate that order ID is a positive integer.

        Args:
            v: The order ID to validate.

        Returns:
            The validated order ID.

        Raises:
            ValueError: If the order ID is not a positive integer.
        """
        if v <= 0:
            raise ValueError("Order ID must be a positive integer")
        return v

    @field_validator("limit")
    @classmethod
    def validate_limit(cls, v: Any) -> Any:
        """Validate that limit is within allowed range.

        Args:
            v: The limit value to validate.

        Returns:
            The validated limit value.

        Raises:
            ValueError: If the limit is not within the allowed range.
        """
        if v is not None and (v < 1 or v > 100):
            raise ValueError("Limit must be between 1 and 100")
        return v

    @field_validator("offset")
    @classmethod
    def validate_offset(cls, v: Any) -> Any:
        """Validate that offset is within allowed range.

        Args:
            v: The offset value to validate.

        Returns:
            The validated offset value.

        Raises:
            ValueError: If the offset is not within the allowed range.
        """
        if v is not None and (v < 0 or v > 10000):
            raise ValueError("Offset must be between 0 and 10000")
        return v


class ExecutedOrdersByMarket(ExecutedOrderHistoryRequest):
    """Executed orders by market request model."""

    pass
