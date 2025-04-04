"""WhiteBit Public API v1 client."""

from aiowhitebit.clients.base import base_get_request
from aiowhitebit.constants import BASE_URL
from aiowhitebit.converters.public import (
    convert_tickers_to_object_v1,
    convert_kline_to_object_v1,
    convert_order_depth_to_object_v1,
)
from aiowhitebit.models.public.v1 import (
    Market,
    MarketInfo,
    Tickers,
    MarketSingleResponse,
    Kline,
    Symbols,
    OrderDepth,
    TradeHistory,
)


class PublicV1Client:
    """WhiteBit Public API v1 client

    This client provides methods to interact with the WhiteBit Public API v1.
    All endpoints return time in Unix-time format and either a JSON object or array.

    Rate limit: 1000 requests/10 sec for all endpoints.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
    ) -> None:
        """Initialize the WhiteBit Public API v1 client

        Args:
            base_url: Base URL for the WhiteBit API. Defaults to the official WhiteBit API URL.
        """
        self.base_url = base_url

    def request_url(self, path: str) -> str:
        """Construct the full URL for an API endpoint

        Args:
            path: API endpoint path

        Returns:
            Full URL for the API endpoint
        """
        return f"{self.base_url}{path}"

    async def get_market_info(self) -> MarketInfo:
        """Get information about all available markets

        This endpoint retrieves all information about available markets.
        Response is cached for 1 second.

        Returns:
            MarketInfo: Information about all available markets

        Example:
            ```python
            client = PublicV1Client()
            markets = await client.get_market_info()
            ```
        """
        request_path = "/api/v1/public/markets"
        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return MarketInfo(**json_obj)

    async def _get_request(self, url: str) -> dict:
        """Make a GET request to the WhiteBit API.

        This method is used to make GET requests to the WhiteBit API.
        It can be overridden in tests to mock the API responses.

        Args:
            url: URL to make the request to

        Returns:
            JSON response from the API
        """
        return await base_get_request(url)

    async def get_tickers(self) -> Tickers:
        """Get information about recent trading activity on all markets

        This endpoint retrieves information about recent trading activity on all markets.
        Response is cached for 1 second.

        Returns:
            Tickers: Information about recent trading activity on all markets

        Example:
            ```python
            client = PublicV1Client()
            tickers = await client.get_tickers()
            ```
        """
        request_path = "/api/v1/public/tickers"
        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return convert_tickers_to_object_v1(json_obj)

    async def get_single_market(self, market: str) -> MarketSingleResponse:
        """Get information about recent trading activity on the requested market

        This endpoint retrieves information about recent trading activity on the requested market.
        Response is cached for 1 second.

        Args:
            market: Available market (e.g. BTC_USDT)

        Returns:
            MarketSingleResponse: Information about recent trading activity on the requested market

        Example:
            ```python
            client = PublicV1Client()
            market_info = await client.get_single_market("BTC_USDT")
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        request_path = f"/api/v1/public/ticker?market={market}"
        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return MarketSingleResponse(**json_obj)

    async def get_kline_market(
        self, market: str, start: int = None, end: int = None, interval: str = None, limit: int = None
    ) -> Kline:
        """Get information about market kline (candlestick)

        This endpoint retrieves information about market kline (candlestick).
        Response is cached for 1 second.
        Max numbers of candles cannot exceed 1440.

        Args:
            market: Available market (e.g. BTC_USDT)
            start: Start time in seconds, default value is one week earlier from the current time.
                Cannot be greater than end parameter. Example: 1596848400
            end: End time in seconds, default value is current time.
                Cannot be less than start parameter. Example: 1596927600
            interval: Possible values - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M.
                By default in case start and end parameters were not specified, for minutes intervals
                the server will return candlesticks for a period of 1 day. For hours intervals will
                return candlesticks for 1 week, for days and week intervals will return candlesticks
                for 1 month and for month interval will return candlesticks for 1 year. Default value is 1h.
            limit: Possible values from 1 to 1440. Default value is 1440.

        Returns:
            Kline: Information about market kline (candlestick)

        Example:
            ```python
            client = PublicV1Client()
            kline = await client.get_kline_market(
                "BTC_USDT",
                start=1596848400,
                end=1596927600,
                interval="1h",
                limit=100
            )
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        # Validate interval if provided
        valid_intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
        if interval and interval not in valid_intervals:
            raise ValueError(f"Invalid interval. Must be one of: {', '.join(valid_intervals)}")

        # Validate limit if provided
        if limit is not None and (limit < 1 or limit > 1440):
            raise ValueError("Limit must be between 1 and 1440")

        # Validate start and end if both provided
        if start is not None and end is not None and start > end:
            raise ValueError("Start time cannot be greater than end time")

        request_path = f"/api/v1/public/kline?market={market}"
        if start is not None:
            request_path = request_path + f"&start={start}"
        if end is not None:
            request_path = request_path + f"&end={end}"
        if interval is not None:
            request_path = request_path + f"&interval={interval}"
        if limit is not None:
            request_path = request_path + f"&limit={limit}"

        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return convert_kline_to_object_v1(json_obj)

    async def get_symbols(self) -> Symbols:
        """Get information about all available markets for trading

        This endpoint retrieves information about all available markets for trading.
        Response is cached for 1 second.

        Returns:
            Symbols: Information about all available markets for trading

        Example:
            ```python
            client = PublicV1Client()
            symbols = await client.get_symbols()
            ```
        """
        request_path = "/api/v1/public/symbols"
        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return Symbols(**json_obj)

    async def get_order_depth(self, market: str, limit: int = None) -> OrderDepth:
        """Get the current order book as two arrays (bids / asks)

        This endpoint retrieves the current order book as two arrays (bids / asks).
        Response is cached for 100 ms.

        Args:
            market: Available market (e.g. BTC_USDT)
            limit: Limit of results. Default: 100, Max: 100

        Returns:
            OrderDepth: Current order book as two arrays (bids / asks)

        Example:
            ```python
            client = PublicV1Client()
            order_depth = await client.get_order_depth("BTC_USDT", limit=50)
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        # Validate limit if provided
        if limit is not None and (limit < 1 or limit > 100):
            raise ValueError("Limit must be between 1 and 100")

        request_path = f"/api/v1/public/depth/result?market={market}"
        if limit is not None:
            request_path = request_path + f"&limit={limit}"

        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return convert_order_depth_to_object_v1(json_obj)

    async def get_trade_history(self, market: str, last_id: int, limit: int = None) -> TradeHistory:
        """Get trades that have been executed for the requested market

        This endpoint retrieves trades that have been executed for the requested market.
        Response is cached for 1 second.

        Args:
            market: Available market (e.g. BTC_USDT)
            last_id: Largest id of last returned result
            limit: Limit of results. Default: 50

        Returns:
            TradeHistory: Trades that have been executed for the requested market

        Example:
            ```python
            client = PublicV1Client()
            trade_history = await client.get_trade_history("BTC_USDT", last_id=6, limit=100)
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        if last_id < 0:
            raise ValueError("Last ID must be a positive integer")

        request_path = f"/api/v1/public/history?market={market}&lastId={last_id}"
        if limit is not None:
            request_path = request_path + f"&limit={limit}"

        full_url = self.request_url(request_path)
        json_obj = await self._get_request(full_url)

        return TradeHistory(**json_obj)
