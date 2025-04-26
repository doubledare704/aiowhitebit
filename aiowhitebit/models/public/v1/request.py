"""Request models for the WhiteBit Public API v1."""

from typing import Optional

from pydantic import BaseModel, field_validator


class KlineRequest(BaseModel):
    """Request model for getting kline data.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        start: Start time in seconds, default value is one week earlier from the current time.
            Cannot be greater than end parameter. Example: 1596848400
        end: End time in seconds, default value is current time.
            Cannot be less than start parameter. Example: 1596927600
        interval: Possible values - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M.
            By default in case start and end parameters were not specified, for minutes intervals
            the server will return candlesticks for a period of 1 day. For hours intervals will
            return candlesticks for 1 week, for days and week intervals will return candlesticks
            for 1 month and for month interval will return candlesticks for 1 year. Default value is 1h.
        limit: Possible values from 1 to 1440. Default value is 1440.
    """

    market: str
    start: Optional[int] = None
    end: Optional[int] = None
    interval: Optional[str] = None
    limit: Optional[int] = None

    @field_validator("interval")
    def validate_interval(cls, v):
        if v is not None:
            valid_intervals = [
                "1m",
                "3m",
                "5m",
                "15m",
                "30m",
                "1h",
                "2h",
                "4h",
                "6h",
                "8h",
                "12h",
                "1d",
                "3d",
                "1w",
                "1M",
            ]
            if v not in valid_intervals:
                raise ValueError(f"Invalid interval. Must be one of: {', '.join(valid_intervals)}")
        return v

    @field_validator("limit")
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 1440):
            raise ValueError("Limit must be between 1 and 1440")
        return v

    @field_validator("start", "end")
    def validate_start_end(cls, v, info):
        if "start" in info.data and info.data["start"] is not None and v is not None and info.data["start"] > v:
            raise ValueError("Start time cannot be greater than end time")
        return v


class OrderDepthRequest(BaseModel):
    """Request model for getting order depth.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        limit: Limit of results. Default: 100, Max: 100
    """

    market: str
    limit: Optional[int] = None

    @field_validator("limit")
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError("Limit must be between 1 and 100")
        return v


class TradeHistoryRequest(BaseModel):
    """Request model for getting trade history.

    Attributes:
        market: Available market (e.g. BTC_USDT)
        last_id: Largest id of last returned result
        limit: Limit of results. Default: 50
    """

    market: str
    last_id: int
    limit: Optional[int] = None

    @field_validator("last_id")
    def validate_last_id(cls, v):
        if v < 0:
            raise ValueError("Last ID must be a positive integer")
        return v
