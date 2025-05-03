"""Request models for the WhiteBit Public API v2."""

from pydantic import BaseModel, ConfigDict, field_validator


class RecentTradesRequest(BaseModel):
    """Request model for getting recent trades.

    Attributes:
        market: Available market (e.g. BTC_USDT)
    """

    market: str

    model_config = ConfigDict(frozen=True, extra="forbid")

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


class OrderDepthRequest(BaseModel):
    """Request model for getting order depth.

    Attributes:
        market: Available market (e.g. BTC_USDT)
    """

    market: str

    model_config = ConfigDict(frozen=True, extra="forbid")

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
