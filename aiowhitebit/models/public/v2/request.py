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
    def validate_market(cls, v):
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
    def validate_market(cls, v):
        if not v:
            raise ValueError("Market parameter is required")
        return v
