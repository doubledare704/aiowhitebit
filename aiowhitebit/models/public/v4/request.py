"""Request models for the WhiteBit Public API v4."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class OrderbookRequest(BaseModel):
    """Request model for getting orderbook.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        limit: Orders depth quantity: 0 - 100. Not defined or 0 will return 100 entries.
        level: Optional parameter that allows API user to see different level of aggregation.
               Level 0 - default level, no aggregation.
               Starting from level 1 (lowest possible aggregation) and up to level 5.
    """

    market: str
    limit: Optional[int] = None
    level: Optional[int] = None

    model_config = ConfigDict(frozen=True)

    @field_validator("market")
    @classmethod
    def validate_market(cls, v):
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
    def validate_limit(cls, v):
        """Validate that limit is within allowed range.

        Args:
            v: The limit value to validate.

        Returns:
            The validated limit value.

        Raises:
            ValueError: If the limit is not within the allowed range.
        """
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Limit must be between 0 and 100")
        return v

    @field_validator("level")
    @classmethod
    def validate_level(cls, v):
        """Validate that level is within allowed range.

        Args:
            v: The level value to validate.

        Returns:
            The validated level value.

        Raises:
            ValueError: If the level is not within the allowed range.
        """
        if v is not None and (v < 0 or v > 5):
            raise ValueError("Level must be between 0 and 5")
        return v


class RecentTradesRequest(BaseModel):
    """Request model for getting recent trades.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        type: Can be buy or sell
    """

    market: str
    type: Optional[str] = None

    model_config = ConfigDict(frozen=True)

    @field_validator("market")
    @classmethod
    def validate_market(cls, v):
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

    @field_validator("type")
    @classmethod
    def validate_type(cls, v):
        """Validate that type is one of the allowed values.

        Args:
            v: The type value to validate.

        Returns:
            The validated type value.

        Raises:
            ValueError: If the type is not one of the allowed values.
        """
        if v is not None and v not in ["buy", "sell"]:
            raise ValueError("Type must be 'buy' or 'sell'")
        return v
