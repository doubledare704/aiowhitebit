"""Models for the WhiteBit API."""

from aiowhitebit.models.base import (
    BasePrivateResponse,
    BasePublicV1Response,
    BasePublicV2Response,
    BaseResponse,
    BaseWebSocketResponse,
)
from aiowhitebit.models.private import (
    CreateLimitOrderRequest,
    CreateOrderResponse,
    ExecutedOrdersResponse,
    TradingBalanceItem,
    TradingBalanceList,
    # Add other specific imports from private module
)
from aiowhitebit.models.public.v1 import (
    OrderDepth,
    Ticker,
    Tickers,
    # Add other specific imports from public.v1 module
)
from aiowhitebit.models.public.v2 import (
    OrderDepthV2,
    # Add other specific imports from public.v2 module
)
from aiowhitebit.models.public.v4 import (
    Asset,
    AssetStatus,
    MarketActivity,
    MarketInfo,
    Orderbook,
    # Add other specific imports from public.v4 module
)
from aiowhitebit.models.websocket import (
    WSError,
    # Add other specific imports from websocket module
    WSRequest,
    WSResponse,
)

__all__ = [
    "Asset",
    "AssetStatus",
    "BasePrivateResponse",
    "BasePublicV1Response",
    "BasePublicV2Response",
    "BaseResponse",
    "BaseWebSocketResponse",
    "CreateLimitOrderRequest",
    "CreateOrderResponse",
    "ExecutedOrdersResponse",
    "MarketActivity",
    "MarketInfo",
    "OrderDepth",
    "OrderDepthV2",
    "Orderbook",
    "Ticker",
    "Tickers",
    "TradingBalanceItem",
    "TradingBalanceList",
    "WSError",
    "WSRequest",
    "WSResponse",
]
