"""Converters for the WhiteBit Public API."""

from aiowhitebit.converters.public.v1 import (
    convert_kline_to_object as convert_kline_to_object_v1,
)
from aiowhitebit.converters.public.v1 import (
    convert_order_depth_to_object as convert_order_depth_to_object_v1,
)
from aiowhitebit.converters.public.v1 import (
    convert_tickers_to_object as convert_tickers_to_object_v1,
)
from aiowhitebit.converters.public.v1 import (
    gen_order,
)
from aiowhitebit.converters.public.v2 import (
    convert_asset_status_to_object,
    convert_order_depth_to_object_v2,
)
from aiowhitebit.converters.public.v4 import (
    convert_asset_status_to_object as convert_asset_status_to_object_v4,
)
from aiowhitebit.converters.public.v4 import (
    convert_market_activity_to_object,
    convert_orderbook_to_object,
    convert_recent_trades_to_object,
)

__all__ = [
    "convert_asset_status_to_object",
    "convert_asset_status_to_object_v4",
    "convert_kline_to_object_v1",
    "convert_market_activity_to_object",
    "convert_order_depth_to_object_v1",
    "convert_order_depth_to_object_v2",
    "convert_orderbook_to_object",
    "convert_recent_trades_to_object",
    "convert_tickers_to_object_v1",
    "gen_order",
]
