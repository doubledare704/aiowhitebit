"""Request models for the WhiteBit WebSocket API."""

import time
from typing import Any, List

from pydantic import BaseModel, field_validator


class WSRequest(BaseModel):
    """WebSocket request model.

    Attributes:
        method: Method name
        params: Parameters
        id: Request ID (defaults to current timestamp)
    """

    method: str
    params: List[Any]
    id: int = int(time.time())

    @field_validator("method")
    def validate_method(cls, v):
        if not v:
            raise ValueError("Method parameter is required")
        return v
