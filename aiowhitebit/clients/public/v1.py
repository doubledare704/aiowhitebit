"""WhiteBit Public API v1 client."""

from typing import Optional

from aiowhitebit.clients.base import BaseClient
from aiowhitebit.config import APIEndpoints
from aiowhitebit.converters.public import (
    convert_kline_to_object_v1,
    convert_order_depth_to_object_v1,
    convert_tickers_to_object_v1,
)
from aiowhitebit.exceptions import WhitebitValidationError
from aiowhitebit.models.public.v1 import (
    Kline,
    MarketInfo,
    MarketSingleResponse,
    OrderDepth,
    Symbols,
    Tickers,
    TradeHistory,
)
from aiowhitebit.utils.rate_limiting import rate_limit
from aiowhitebit.utils.validation import validate_market


class PublicV1Client(BaseClient):
    """WhiteBit Public API v1 client.

    This client provides methods to interact with the WhiteBit Public API v1.
    All endpoints return time in Unix-time format and either a JSON object or array.

    Rate limit: 1000 requests/10 sec for all endpoints.
    """

    @rate_limit(limit=1000, window=10.0)
    async def get_market_info(self) -> MarketInfo:
        """Get information about all available markets.

        This endpoint retrieves all information about available markets.
        Response is cached for 1 second.
        """
        return await self._make_request(APIEndpoints.MARKET_INFO_V1, converter=lambda x: MarketInfo(**x))

    @rate_limit(limit=1000, window=10.0)
    async def get_tickers(self) -> Tickers:
        """Get information about recent trading activity on all markets."""
        return await self._make_request(APIEndpoints.TICKERS_V1, converter=convert_tickers_to_object_v1)

    @rate_limit(limit=1000, window=10.0)
    async def get_single_market(self, market: str) -> MarketSingleResponse:
        """Get information about recent trading activity on the requested market."""
        validate_market(market)
        return await self._make_request(
            f"{APIEndpoints.TICKER_V1}?market={market}", converter=lambda x: MarketSingleResponse(**x)
        )

    @rate_limit(limit=1000, window=10.0)
    async def get_kline_market(
        self,
        market: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        interval: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Kline:
        """Get kline data for the requested market."""
        validate_market(market)

        # Validate interval if provided
        valid_intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
        if interval and interval not in valid_intervals:
            raise WhitebitValidationError(f"Invalid interval. Must be one of: {', '.join(valid_intervals)}")

        # Validate limit if provided
        if limit is not None and (limit < 1 or limit > 1440):
            raise WhitebitValidationError("Limit must be between 1 and 1440")

        # Validate start and end times
        if start is not None and end is not None and start >= end:
            raise WhitebitValidationError("Start time cannot be greater than end time")

        # Build query parameters
        params = []
        if start is not None:
            params.append(f"start={start}")
        if end is not None:
            params.append(f"end={end}")
        if interval is not None:
            params.append(f"interval={interval}")
        if limit is not None:
            params.append(f"limit={limit}")

        query_string = f"market={market}"
        if params:
            query_string += "&" + "&".join(params)

        return await self._make_request(f"{APIEndpoints.KLINE_V1}?{query_string}", converter=convert_kline_to_object_v1)

    @rate_limit(limit=1000, window=10.0)
    async def get_symbols(self) -> Symbols:
        """Get information about all available markets for trading."""
        return await self._make_request(APIEndpoints.SYMBOLS_V1, converter=lambda x: Symbols(**x))

    @rate_limit(limit=1000, window=10.0)
    async def get_order_depth(self, market: str, limit: Optional[int] = None) -> OrderDepth:
        """Get order book for the requested market.

        Args:
            market: Available market (e.g. BTC_USDT)
            limit: Limit of results. Default: 100, Max: 100

        Returns:
            OrderDepth: Order book data

        Raises:
            WhitebitValidationError: If market is empty or limit is invalid
        """
        validate_market(market)

        if limit is not None and (limit < 1 or limit > 100):
            raise WhitebitValidationError("Limit must be between 1 and 100")

        query_string = f"{APIEndpoints.DEPTH_V1.format(market=market)}"
        if limit is not None:
            query_string += f"?limit={limit}"

        return await self._make_request(query_string, converter=convert_order_depth_to_object_v1)

    @rate_limit(limit=1000, window=10.0)
    async def get_trade_history(
        self, market: str, last_id: Optional[int] = None, limit: Optional[int] = None
    ) -> TradeHistory:
        """Get trade history for the requested market."""
        validate_market(market)

        if limit is not None and (limit < 1 or limit > 100):
            raise WhitebitValidationError("Limit must be between 1 and 100")

        if last_id is not None and last_id < 0:
            raise WhitebitValidationError("Last ID must be a positive integer")

        params = []
        if last_id is not None:
            params.append(f"lastId={last_id}")
        if limit is not None:
            params.append(f"limit={limit}")

        query_string = f"market={market}"
        if params:
            query_string += "&" + "&".join(params)

        return await self._make_request(
            f"{APIEndpoints.HISTORY_V1}?{query_string}", converter=lambda x: TradeHistory(**x)
        )
