"""Request models for the WhiteBit Public API v1."""

from typing import Any, Optional

from pydantic import BaseModel, field_validator


class KlineRequest(BaseModel):
    """Request model for getting kline data.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        start: Start time (UNIX timestamp)
        end: End time (UNIX timestamp)
        interval: Interval in seconds (60, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200)
        limit: Limit of results (default: 720, min: 1, max: 1440)
    """

    market: str
    start: int
    end: int
    interval: int
    limit: Optional[int] = None

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

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, v: Any) -> Any:
        """Validate that interval is one of the allowed values.

        Args:
            v: The interval value to validate.

        Returns:
            The validated interval value.

        Raises:
            ValueError: If the interval is not one of the allowed values.
        """
        allowed_intervals = [60, 300, 900, 1800, 3600, 7200, 14400, 21600, 43200, 86400, 259200]
        if v not in allowed_intervals:
            raise ValueError(f"Interval must be one of {allowed_intervals}")
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
        if v is not None and (v < 1 or v > 1440):
            raise ValueError("Limit must be between 1 and 1440")
        return v


class OrderDepthRequest(BaseModel):
    """Request model for getting order depth.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        limit: Limit of results. Default: 100, Max: 100
    """

    market: str
    limit: Optional[int] = None

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


class TradeHistoryRequest(BaseModel):
    """Request model for getting trade history.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        lastId: Last ID (optional)
        limit: Limit of results (default: 50, min: 1, max: 100)
    """

    market: str
    lastId: Optional[int] = None
    limit: Optional[int] = None

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


class SingleMarketRequest(BaseModel):
    """Request model for getting single market info.

    Attributes:
        market: Available market (e.g. BTC_USDT)
    """

    market: str

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
