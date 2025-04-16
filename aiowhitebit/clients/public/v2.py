"""WhiteBit Public API v2 client."""

from aiowhitebit.clients.base import BaseClient
from aiowhitebit.config import APIEndpoints
from aiowhitebit.constants import BASE_URL
from aiowhitebit.converters.public import (
    convert_asset_status_to_object,
    convert_order_depth_to_object_v2,
)
from aiowhitebit.models.public.v2 import (
    AssetStatus,
    FeeResponse,
    MarketInfo,
    OrderDepthV2,
    RecentTrades,
    Tickers,
)


class PublicV2Client(BaseClient):
    """WhiteBit Public API v2 client

    This client provides methods to interact with the WhiteBit Public API v2.
    All endpoints return time in Unix-time format and either a JSON object or array.

    Rate limit: 1000 requests/10 sec for all endpoints.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
    ) -> None:
        """Initialize the WhiteBit Public API v2 client

        Args:
            base_url: Base URL for the WhiteBit API. Defaults to the official WhiteBit API URL.
        """
        super().__init__(base_url)

    async def get_market_info(self) -> MarketInfo:
        """Get information about all available markets

        This endpoint retrieves all information about available markets.
        Response is cached for 1 second.

        Returns:
            MarketInfo: Information about all available markets

        Example:
            ```python
            client = PublicV2Client()
            markets = await client.get_market_info()
            ```
        """
        return await self._make_request(APIEndpoints.MARKET_INFO_V2, converter=lambda x: MarketInfo(**x))

    async def get_tickers(self) -> Tickers:
        """Get information about recent trading activity on all markets

        This endpoint retrieves information about recent trading activity on all markets.
        Response is cached for 1 second.

        Returns:
            Tickers: Information about recent trading activity on all markets

        Example:
            ```python
            client = PublicV2Client()
            tickers = await client.get_tickers()
            ```
        """
        return await self._make_request(APIEndpoints.TICKER_V2, converter=lambda x: Tickers(**x))

    async def get_recent_trades(self, market: str) -> RecentTrades:
        """Get recent trades for the requested market

        This endpoint retrieves recent trades for the requested market.
        Response is cached for 1 second.

        Args:
            market: Available market (e.g. BTC_USDT)

        Returns:
            RecentTrades: Recent trades for the requested market

        Example:
            ```python
            client = PublicV2Client()
            recent_trades = await client.get_recent_trades("BTC_USDT")
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        return await self._make_request(
            APIEndpoints.RECENT_TRADES_V2.format(market=market), converter=lambda x: RecentTrades(**x)
        )

    async def get_fee(self) -> FeeResponse:
        """Get fee information

        This endpoint retrieves fee information.
        Response is cached for 1 second.

        Returns:
            FeeResponse: Fee information

        Example:
            ```python
            client = PublicV2Client()
            fee = await client.get_fee()
            ```
        """
        return await self._make_request(APIEndpoints.FEE_V2, converter=lambda x: FeeResponse(**x))

    async def get_asset_status_list(self) -> AssetStatus:
        """Get asset status list

        This endpoint retrieves asset status list.
        Response is cached for 1 second.

        Returns:
            AssetStatus: Asset status list

        Example:
            ```python
            client = PublicV2Client()
            asset_status = await client.get_asset_status_list()
            ```
        """
        return await self._make_request(APIEndpoints.ASSET_STATUS_V2, converter=convert_asset_status_to_object)

    async def get_order_depth(self, market: str) -> OrderDepthV2:
        """Get the current order book as two arrays (bids / asks)

        This endpoint retrieves the current order book as two arrays (bids / asks).
        Response is cached for 100 ms.

        Args:
            market: Available market (e.g. BTC_USDT)

        Returns:
            OrderDepthV2: Current order book as two arrays (bids / asks)

        Example:
            ```python
            client = PublicV2Client()
            order_depth = await client.get_order_depth("BTC_USDT")
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        return await self._make_request(
            APIEndpoints.DEPTH_V2.format(market=market), converter=convert_order_depth_to_object_v2
        )
