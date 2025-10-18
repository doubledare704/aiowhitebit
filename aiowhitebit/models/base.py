"""Base models for the WhiteBit API."""

from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Base model for API responses.

    Attributes:
        success: Whether the request was successful
        message: Error message if success is False, None otherwise
    """

    success: bool
    message: Any


class BasePublicV1Response(BaseResponse):
    """Base model for public API v1 responses."""

    pass


class BasePublicV2Response(BaseResponse):
    """Base model for public API v2 responses."""

    pass


class BasePrivateResponse(BaseResponse):
    """Base model for private API responses."""

    pass


class BaseWebSocketResponse(BaseModel):
    """Base model for WebSocket API responses.

    Attributes:
        event_time: Timestamp of the event (optional for backward compatibility)
        update_id: Unique identifier for each update (optional for backward compatibility)
    """

    event_time: int | None = None
    update_id: int | None = None
