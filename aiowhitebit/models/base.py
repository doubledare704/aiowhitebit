"""Base models for the WhiteBit API."""

from typing import Any, Optional

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
    """Base model for WebSocket API responses."""

    pass
