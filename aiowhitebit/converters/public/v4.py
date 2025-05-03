"""Converters for the WhiteBit Public API v4."""

from typing import Any

from aiowhitebit.models.public.v4.response import (
    Asset,
    AssetStatus,
    MarketActivity,
    MarketActivityItem,
    Orderbook,
    RecentTrade,
    RecentTrades,
)


def convert_market_activity_to_object(json_body: dict) -> MarketActivity:
    """Convert market activity JSON response to MarketActivity object.

    Args:
        json_body: JSON response from the API

    Returns:
        MarketActivity object
    """
    result = {}
    for market, data in json_body.items():
        result[market] = MarketActivityItem(**data)
    return MarketActivity(result)


def convert_asset_status_to_object(json_body: dict) -> AssetStatus:
    """Convert asset status JSON response to AssetStatus object.

    Args:
        json_body: JSON response from the API

    Returns:
        AssetStatus object
    """
    result = {}
    for asset, data in json_body.items():
        result[asset] = Asset(**data)
    return AssetStatus(result)


def convert_orderbook_to_object(json_body: dict) -> Orderbook:
    """Convert orderbook JSON response to Orderbook object.

    Args:
        json_body: JSON response from the API

    Returns:
        Orderbook object
    """
    return Orderbook(**json_body)


def convert_recent_trades_to_object(json_body: list[dict[str, Any]]) -> RecentTrades:
    """Convert recent trades JSON response to RecentTrades object.

    Args:
        json_body: JSON response from the API

    Returns:
        RecentTrades object
    """
    trades = [RecentTrade(**trade) for trade in json_body]
    return RecentTrades(trades)
