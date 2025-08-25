"""WebSocket API models."""

from aiowhitebit.models.websocket.bookticker import (
    BookTickerData,
    BookTickerResponse,
    BookTickerSubscribeRequest,
    BookTickerUnsubscribeRequest,
)
from aiowhitebit.models.websocket.depth import (
    DepthData,
    DepthItem,
    DepthSubscribeResponse,
    DepthUpdateResponse,
)
from aiowhitebit.models.websocket.request import WSRequest
from aiowhitebit.models.websocket.response import WSError, WSResponse

__all__ = [
    "BookTickerData",
    "BookTickerResponse",
    "BookTickerSubscribeRequest",
    "BookTickerUnsubscribeRequest",
    "DepthData",
    "DepthItem",
    "DepthSubscribeResponse",
    "DepthUpdateResponse",
    "WSError",
    "WSRequest",
    "WSResponse",
]
