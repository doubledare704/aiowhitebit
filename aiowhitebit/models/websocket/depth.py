"""Market Depth WebSocket models for the WhiteBit API."""

from typing import Optional

from pydantic import BaseModel

from aiowhitebit.models.base import BaseWebSocketResponse


class DepthItem(BaseModel):
    """Depth item model representing a single bid or ask.
    
    Attributes:
        price: Price level
        quantity: Quantity at this price level
    """
    
    price: str
    quantity: str


class DepthData(BaseModel):
    """Market depth data model.
    
    Attributes:
        market: Trading pair symbol (e.g., "BTC_USDT")
        bids: List of bid orders [price, quantity]
        asks: List of ask orders [price, quantity]
    """
    
    market: str
    bids: list[list[str]]
    asks: list[list[str]]


class DepthUpdateResponse(BaseWebSocketResponse):
    """Market depth update WebSocket response model.
    
    Attributes:
        method: Method name ("depth_update")
        params: Market depth data
        event_time: Timestamp of the event
        update_id: Unique identifier for each update
    """
    
    method: str
    params: DepthData
    event_time: Optional[int] = None
    update_id: Optional[int] = None


class DepthSubscribeResponse(BaseWebSocketResponse):
    """Market depth subscribe response model.
    
    Attributes:
        id: Request ID
        result: Subscription result data
        error: Error information (if any)
        event_time: Timestamp of the event
        update_id: Unique identifier for each update
    """
    
    id: int
    result: Optional[dict] = None
    error: Optional[dict] = None
    event_time: Optional[int] = None
    update_id: Optional[int] = None
