__all__ = [
    "WSRequest",
]

import time
from typing import List

from pydantic.main import BaseModel


class WSRequest(BaseModel):
    method: str
    params: List
    id: int = int(time.time())
