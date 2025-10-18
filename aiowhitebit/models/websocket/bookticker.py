"""BookTicker WebSocket models for the WhiteBit API."""

from pydantic import BaseModel

from aiowhitebit.models.base import BaseWebSocketResponse


class BookTickerData(BaseModel):
    """BookTicker data model.

    Attributes:
        symbol: Trading pair symbol (e.g., "BTC_USDT")
        bid_price: Best bid price
        bid_qty: Best bid quantity
        ask_price: Best ask price
        ask_qty: Best ask quantity
    """

    symbol: str
    bid_price: str
    bid_qty: str
    ask_price: str
    ask_qty: str


class BookTickerResponse(BaseWebSocketResponse):
    """BookTicker WebSocket response model.

    Attributes:
        method: Method name ("bookTicker_update")
        params: BookTicker data
        event_time: Timestamp of the event
        update_id: Unique identifier for each update
    """

    method: str
    params: BookTickerData
    event_time: int | None = None
    update_id: int | None = None


class BookTickerSubscribeRequest(BaseModel):
    """BookTicker subscribe request model.

    Attributes:
        method: Method name ("bookTicker_subscribe")
        params: List containing the market symbol
        id: Request ID
    """

    method: str = "bookTicker_subscribe"
    params: list[str]
    id: int


class BookTickerUnsubscribeRequest(BaseModel):
    """BookTicker unsubscribe request model.

    Attributes:
        method: Method name ("bookTicker_unsubscribe")
        params: List containing the market symbol
        id: Request ID
    """

    method: str = "bookTicker_unsubscribe"
    params: list[str]
    id: int
