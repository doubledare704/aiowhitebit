"""WhiteBit Public API v2 client."""

from aiowhitebit.clients.base import base_get_request
from aiowhitebit.constants import BASE_URL
from aiowhitebit.converters.public import (
    convert_asset_status_to_object,
    convert_order_depth_to_object_v2,
)
from aiowhitebit.models.public.v2 import (
    MarketInfo,
    Tickers,
    RecentTrades,
    FeeResponse,
    AssetStatus,
    OrderDepthV2,
)


class PublicV2Client:
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
            client = PublicV2Client()
            markets = await client.get_market_info()
            ```
        """
        request_path = "/api/v2/public/markets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MarketInfo(**json_obj)

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
        request_path = "/api/v2/public/ticker"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return Tickers(**json_obj)

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

        request_path = f"/api/v2/public/trades/{market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return RecentTrades(**json_obj)

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
        request_path = "/api/v2/public/fee"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return FeeResponse(**json_obj)

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
        request_path = "/api/v2/public/assets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_asset_status_to_object(json_obj)

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

        request_path = f"/api/v2/public/depth/{market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_order_depth_to_object_v2(json_obj)
