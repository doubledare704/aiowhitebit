"""Request models for the WhiteBit Public API v4."""

from typing import Optional

from pydantic import BaseModel, validator


class OrderbookRequest(BaseModel):
    """Request model for getting orderbook.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        limit: Orders depth quantity: 0 - 100. Not defined or 0 will return 100 entries.
        level: Optional parameter that allows API user to see different level of aggregation.
               Level 0 – default level, no aggregation.
               Starting from level 1 (lowest possible aggregation) and up to level 5.
    """

    market: str
    limit: Optional[int] = None
    level: Optional[int] = None

    @validator("market")
    def validate_market(cls, v):
        if not v:
            raise ValueError("Market parameter is required")
        return v

    @validator("limit")
    def validate_limit(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Limit must be between 0 and 100")
        return v

    @validator("level")
    def validate_level(cls, v):
        if v is not None and (v < 0 or v > 5):
            raise ValueError("Level must be between 0 and 5")
        return v

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable


class RecentTradesRequest(BaseModel):
    """Request model for getting recent trades.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        type: Can be buy or sell
    """

    market: str
    type: Optional[str] = None

    @validator("market")
    def validate_market(cls, v):
        if not v:
            raise ValueError("Market parameter is required")
        return v

    @validator("type")
    def validate_type(cls, v):
        if v is not None and v not in ["buy", "sell"]:
            raise ValueError("Type must be 'buy' or 'sell'")
        return v

    class Config:
        """Pydantic model configuration"""

        frozen = True  # Makes the model immutable
