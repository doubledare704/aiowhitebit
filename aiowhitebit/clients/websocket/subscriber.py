"""WhiteBit WebSocket Subscriber client."""

import json
import pprint
from datetime import datetime
from typing import Any, Callable, Optional, TypeVar

import websocket

from aiowhitebit.constants import BASE_WS_PUBLIC_URL
from aiowhitebit.models.websocket import WSRequest

# Define a type variable for the websocket callbacks
WSCallback = TypeVar("WSCallback", bound=Callable[..., Any])


def infinite_sequence():
    """Generate an infinite sequence of integers starting from 1.

    Yields:
        Integer in the sequence
    """
    num = 1
    while True:
        yield num
        num += 1


id_gen = infinite_sequence()


class SubscribeRequest:
    """WebSocket subscribe request builder.

    This class provides methods to build subscribe requests for the WhiteBit WebSocket API.
    """

    @staticmethod
    def candles_subscribe(market: str, interval: int) -> dict:
        """Build a candles subscribe request.

        Args:
            market: Market (e.g. BTC_USDT)
            interval: Interval in seconds

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.candles_subscribe("BTC_USDT", 900)
            ```
        """
        return WSRequest(method="candles_subscribe", params=[market, interval], id=next(id_gen)).model_dump()

    @staticmethod
    def lastprice_subscribe(markets: list[str]) -> dict:
        """Build a lastprice subscribe request.

        Args:
            markets: List of markets (e.g. ["BTC_USDT", "ETH_BTC"])

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.lastprice_subscribe(["BTC_USDT", "ETH_BTC"])
            ```
        """
        return WSRequest(method="lastprice_subscribe", params=[*markets], id=next(id_gen)).model_dump()

    @staticmethod
    def market_subscribe(markets: list[str]) -> dict:
        """Build a market subscribe request.

        Args:
            markets: List of markets (e.g. ["BTC_USDT", "ETH_BTC"])

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.market_subscribe(["BTC_USDT", "ETH_BTC"])
            ```
        """
        return WSRequest(method="market_subscribe", params=[*markets], id=next(id_gen)).model_dump()

    @staticmethod
    def market_today_subscribe(markets: list[str]) -> dict:
        """Build a market today subscribe request.

        Args:
            markets: List of markets (e.g. ["BTC_USDT", "ETH_BTC"])

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.market_today_subscribe(["BTC_USDT", "ETH_BTC"])
            ```
        """
        return WSRequest(method="marketToday_subscribe", params=[*markets], id=next(id_gen)).model_dump()

    @staticmethod
    def trades_subscribe(markets: list[str]) -> dict:
        """Build a trades subscribe request.

        Args:
            markets: List of markets (e.g. ["BTC_USDT", "ETH_BTC"])

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.trades_subscribe(["BTC_USDT", "ETH_BTC"])
            ```
        """
        return WSRequest(method="trades_subscribe", params=[*markets], id=next(id_gen)).model_dump()

    @staticmethod
    def depth_subscribe(
        market: str,
        limit: int = 100,
        price_intervals: str = "0",
        multiple_sub: bool = True,
    ) -> dict:
        """Build a depth subscribe request.

        Args:
            market: Market (e.g. BTC_USDT)
            limit: Limit of results (default: 100)
            price_intervals: Price intervals (default: "0")
                Available values: "0.00000001", "0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.01", "0.1"
            multiple_sub: Whether to allow multiple subscriptions (default: True)

        Returns:
            Subscribe request

        Example:
            ```python
            request = SubscribeRequest.depth_subscribe("BTC_USDT", 100, "0.0001", True)
            ```
        """
        return WSRequest(
            method="depth_subscribe",
            params=[market, limit, price_intervals, multiple_sub],
            id=next(id_gen),
        ).model_dump()


def ws_subscribe_builder(
    sub_msg: dict,
    on_message_callback: Optional[WSCallback] = None,
    on_open_callback: Optional[WSCallback] = None,
    on_close_callback: Optional[WSCallback] = None,
) -> None:
    """Build a WebSocket subscriber.

    Args:
        sub_msg: Subscribe message
        on_message_callback: Callback for message events (optional)
        on_open_callback: Callback for open events (optional)
        on_close_callback: Callback for close events (optional)

    Example:
        ```python
        request = SubscribeRequest.depth_subscribe("BTC_USDT")
        ws_subscribe_builder(request)
        ```
    """

    def default_on_open(wsapp):
        print(f">>> Opened subscriber: {sub_msg['method']}")
        wsapp.send(json.dumps(sub_msg))

    def default_on_message(wsapp, message, prev=None):
        print(f"<<<<Received : {datetime.now()} {sub_msg['method']}")
        pprint.pprint(json.loads(message))

    def default_on_close(wsapp):
        print("Closed connection")

    on_open = on_open_callback or default_on_open
    on_message = on_message_callback or default_on_message
    on_close = on_close_callback or default_on_close

    endpoint = BASE_WS_PUBLIC_URL
    # Use type: ignore to tell the type checker to ignore this line
    ws = websocket.WebSocketApp(
        endpoint,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close,  # type: ignore
    )

    ws.run_forever()
