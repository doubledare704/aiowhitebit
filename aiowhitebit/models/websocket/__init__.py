"""WebSocket API models."""

from aiowhitebit.models.websocket.request import WSRequest
from aiowhitebit.models.websocket.response import WSError, WSResponse

__all__ = [
    "WSError",
    "WSRequest",
    "WSResponse",
]
