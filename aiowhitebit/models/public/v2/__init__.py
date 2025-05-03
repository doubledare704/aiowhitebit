"""Public API v2 models."""

from aiowhitebit.models.public.v2.request import (
    OrderDepthRequest,
    RecentTradesRequest,
)
from aiowhitebit.models.public.v2.response import (
    Asset,
    AssetStatus,
    Fee,
    FeeResponse,
    Market,
    MarketInfo,
    OrderDepthV2,
    RecentTrade,
    RecentTrades,
    Ticker,
    Tickers,
)

__all__ = [
    "Asset",
    "AssetStatus",
    "Fee",
    "FeeResponse",
    "Market",
    "MarketInfo",
    "OrderDepthRequest",
    "OrderDepthV2",
    "RecentTrade",
    "RecentTrades",
    "RecentTradesRequest",
    "Ticker",
    "Tickers",
]
