__all__ = [
    "WSError",
    "WSResponse",
]

from typing import Any, Optional

from pydantic import BaseModel


class WSError(BaseModel):
    message: str
    code: int


class WSResponse(BaseModel):
    id: int
    result: Any
    error: Optional[WSError]
