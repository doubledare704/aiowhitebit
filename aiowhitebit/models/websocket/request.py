"""Request models for the WhiteBit WebSocket API."""

import time
from typing import Any

from pydantic import BaseModel, field_validator


class WSRequest(BaseModel):
    """WebSocket request model.

    Attributes:
        method: Method name
        params: Parameters
        id: Request ID (defaults to current timestamp)
    """

    method: str
    params: list[Any]
    id: int = int(time.time())

    @field_validator("method")
    @classmethod
    def validate_method(cls, v):
        """Validate that method parameter is not empty.

        Args:
            v: The method value to validate.

        Returns:
            The validated method value.

        Raises:
            ValueError: If the method value is empty.
        """
        if not v:
            raise ValueError("Method parameter is required")
        return v
