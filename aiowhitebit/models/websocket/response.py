"""Response models for the WhiteBit WebSocket API."""

from typing import Any, Optional

from pydantic import BaseModel

from aiowhitebit.models.base import BaseWebSocketResponse


class WSError(BaseModel):
    """WebSocket error model.

    Attributes:
        message: Error message
        code: Error code
    """

    message: str
    code: int


class WSResponse(BaseWebSocketResponse):
    """WebSocket response model.

    Attributes:
        id: Request ID
        result: Result data
        error: Error information (if any)
    """

    id: int
    result: Any
    error: Optional[WSError] = None
