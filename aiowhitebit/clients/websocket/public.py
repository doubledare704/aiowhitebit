"""WhiteBit WebSocket Public API client."""

import json
import logging
from typing import Optional

import websockets

from aiowhitebit.constants import BASE_WS_PUBLIC_URL
from aiowhitebit.models.websocket import WSRequest, WSResponse


class BaseWebSocketClient:
    """Base WebSocket client for WhiteBit API.

    This class provides basic WebSocket functionality for the WhiteBit API.
    """

    def __init__(self, uri: str) -> None:
        """Initialize the WebSocket client

        Args:
            uri: WebSocket URI
        """
        self.uri = uri
        self.connection: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self):
        """Connect to the WebSocket server

        Establishes a connection to the WebSocket server if not already connected.
        """
        if not self.connection:
            self.connection = await websockets.connect(self.uri)

    async def close(self):
        """Close the WebSocket connection

        Closes the connection to the WebSocket server if it exists.
        """
        if self.connection:
            await self.connection.close()

    async def send_message(self, request: dict) -> dict:
        """Send a message to the WebSocket server

        Args:
            request: Request to send

        Returns:
            Response from the server
        """
        await self.connect()
        await self.connection.send(json.dumps(request))
        logging.info(f">>> {request}")

        response = await self.connection.recv()
        msg_json = json.loads(response)
        logging.info(f">>> {response}")
        return msg_json


class PublicWebSocketClient:
    """WhiteBit Public WebSocket API client

    This client provides methods to interact with the WhiteBit Public WebSocket API.
    """

    def __init__(self, ws: BaseWebSocketClient = None) -> None:
        """Initialize the WhiteBit Public WebSocket API client

        Args:
            ws: WebSocket client. If None, a new client will be created.
        """
        self.ws = ws or BaseWebSocketClient(BASE_WS_PUBLIC_URL)

    async def base_ws_requester(self, req: WSRequest) -> WSResponse:
        """Base method for making WebSocket requests

        Args:
            req: WebSocket request

        Returns:
            WebSocket response
        """
        response = await self.ws.send_message(req.dict())
        return WSResponse(**response)

    async def ping(self) -> WSResponse:
        """Ping the server

        Returns:
            WebSocket response

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.ping()
            ```
        """
        return await self.base_ws_requester(WSRequest(method="ping", params=[]))

    async def time(self) -> WSResponse:
        """Get server time

        Returns:
            WebSocket response with server time

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.time()
            ```
        """
        return await self.base_ws_requester(WSRequest(method="time", params=[]))

    async def kline(self, market: str, start_time: int, end_time: int, interval_secs: int) -> WSResponse:
        """Get kline (candlestick) data

        Args:
            market: Market (e.g. BTC_USDT)
            start_time: Start time in seconds
            end_time: End time in seconds
            interval_secs: Interval in seconds

        Returns:
            WebSocket response with kline data

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.kline("BTC_USDT", 1579569940, 1580894800, 900)
            ```
        """
        return await self.base_ws_requester(
            WSRequest(
                method="candles_request",
                params=[market, start_time, end_time, interval_secs],
            )
        )

    async def last_price(self, market: str) -> WSResponse:
        """Get last price for a market

        Args:
            market: Market (e.g. BTC_USDT)

        Returns:
            WebSocket response with last price

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.last_price("BTC_USDT")
            ```
        """
        return await self.base_ws_requester(WSRequest(method="lastprice_request", params=[market]))

    async def market_stats(self, market: str, period_secs: int) -> WSResponse:
        """Get market statistics

        Args:
            market: Market (e.g. BTC_USDT)
            period_secs: Period in seconds

        Returns:
            WebSocket response with market statistics

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.market_stats("BTC_USDT", 86400)
            ```
        """
        return await self.base_ws_requester(WSRequest(method="market_request", params=[market, period_secs]))

    async def market_stats_today(self, market: str) -> WSResponse:
        """Get market statistics for current day UTC

        Args:
            market: Market (e.g. BTC_USDT)

        Returns:
            WebSocket response with market statistics for current day

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.market_stats_today("BTC_USDT")
            ```
        """
        return await self.base_ws_requester(WSRequest(method="marketToday_query", params=[market]))

    async def market_trades(self, market: str, limit: int, largest_id: int) -> WSResponse:
        """Get market trades

        Args:
            market: Market (e.g. BTC_USDT)
            limit: Limit of results
            largest_id: Largest ID

        Returns:
            WebSocket response with market trades

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.market_trades("BTC_USDT", 100, 41358445)
            ```
        """
        return await self.base_ws_requester(WSRequest(method="trades_request", params=[market, limit, largest_id]))

    async def market_depth(self, market: str, limit: int, intervals: str) -> WSResponse:
        """Get market depth

        Args:
            market: Market (e.g. BTC_USDT)
            limit: Limit of results
            intervals: "0" - no interval, available values - "0.00000001", "0.0000001", "0.000001",
                "0.00001", "0.0001", "0.001", "0.01", "0.1"

        Returns:
            WebSocket response with market depth

        Example:
            ```python
            client = PublicWebSocketClient()
            response = await client.market_depth("BTC_USDT", 100, "0.0001")
            ```
        """
        return await self.base_ws_requester(WSRequest(method="depth_request", params=[market, limit, intervals]))

    async def close(self):
        """Close the WebSocket connection

        Example:
            ```python
            client = PublicWebSocketClient()
            # ... use client ...
            await client.close()
            ```
        """
        await self.ws.close()


def get_public_websocket_client() -> PublicWebSocketClient:
    """Get a new PublicWebSocketClient

    Returns:
        PublicWebSocketClient

    Example:
        ```python
        client = get_public_websocket_client()
        ```
    """
    return PublicWebSocketClient(BaseWebSocketClient(BASE_WS_PUBLIC_URL))
