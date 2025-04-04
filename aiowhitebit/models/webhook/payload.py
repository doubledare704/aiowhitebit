__all__ = [
    "WebhookRequest",
]

from pydantic.main import BaseModel


class WebhookRequest(BaseModel):
    method: str
    params: dict
    id: str
