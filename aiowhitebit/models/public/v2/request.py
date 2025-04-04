"""Request models for the WhiteBit Public API v2."""

from pydantic import BaseModel, validator


class RecentTradesRequest(BaseModel):
    """Request model for getting recent trades.

    Attributes:
        market: Available market (e.g. BTC_USDT)
    """

    market: str

    @validator("market")
    def validate_market(cls, v):
        if not v:
            raise ValueError("Market parameter is required")
        return v

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable


class OrderDepthRequest(BaseModel):
    """Request model for getting order depth.

    Attributes:
        market: Available market (e.g. BTC_USDT)
    """

    market: str

    @validator("market")
    def validate_market(cls, v):
        if not v:
            raise ValueError("Market parameter is required")
        return v

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
