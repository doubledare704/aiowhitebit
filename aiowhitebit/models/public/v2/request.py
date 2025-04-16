"""Request models for the WhiteBit Public API v2."""

try:
    from pydantic.v1 import BaseModel, validator  # For Pydantic v2
except ImportError:
    from pydantic import BaseModel, validator  # For Pydantic v1


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

        frozen = True

        # Add compatibility for both v1 and v2
        try:
            from pydantic.v1 import Extra

            extra = Extra.forbid
        except ImportError:
            extra = "forbid"


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
