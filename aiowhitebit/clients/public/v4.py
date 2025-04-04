"""WhiteBit Public API v4 client."""

from typing import Optional

from aiowhitebit.clients.base import base_get_request
from aiowhitebit.constants import BASE_URL
from aiowhitebit.converters.public import (
    convert_market_activity_to_object,
    convert_asset_status_to_object_v4,
    convert_orderbook_to_object,
    convert_recent_trades_to_object,
)
from aiowhitebit.models.public.v4 import (
    MaintenanceStatus,
    MarketInfo,
    MarketActivity,
    AssetStatus,
    Orderbook,
    Depth,
    RecentTrades,
    FeeResponse,
    ServerTime,
    ServerStatus,
    CollateralMarkets,
    FuturesMarkets,
    MiningPoolOverview,
)


class PublicV4Client:
    """WhiteBit Public API v4 client

    This client provides methods to interact with the WhiteBit Public API v4.
    All endpoints return time in Unix-time format and either a JSON object or array.

    Rate limits vary by endpoint, check the documentation for each method.
    """

    def __init__(
        self,
        base_url: str = BASE_URL,
    ) -> None:
        """Initialize the WhiteBit Public API v4 client

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

    async def get_maintenance_status(self) -> MaintenanceStatus:
        """Get maintenance status

        This endpoint retrieves maintenance status.
        1 - system operational, 0 - system maintenance.

        Returns:
            MaintenanceStatus: Maintenance status

        Example:
            ```python
            client = PublicV4Client()
            status = await client.get_maintenance_status()
            ```
        """
        request_path = "/api/v4/public/platform/status"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MaintenanceStatus(**json_obj)

    async def get_market_info(self) -> MarketInfo:
        """Get information about all available spot and futures markets

        This endpoint retrieves all information about available spot and futures markets.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            MarketInfo: Information about all available markets

        Example:
            ```python
            client = PublicV4Client()
            markets = await client.get_market_info()
            ```
        """
        request_path = "/api/v4/public/markets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        # The API returns a list of dictionaries with market information
        return MarketInfo(json_obj)

    async def get_market_activity(self) -> MarketActivity:
        """Get 24-hour pricing and volume summary for each market pair

        This endpoint retrieves a 24-hour pricing and volume summary for each market pair available on the exchange.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            MarketActivity: 24-hour pricing and volume summary for each market pair

        Example:
            ```python
            client = PublicV4Client()
            activity = await client.get_market_activity()
            ```
        """
        request_path = "/api/v4/public/ticker"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_market_activity_to_object(json_obj)

    async def get_asset_status_list(self) -> AssetStatus:
        """Get assets status

        This endpoint retrieves the assets status.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            AssetStatus: Assets status

        Example:
            ```python
            client = PublicV4Client()
            assets = await client.get_asset_status_list()
            ```
        """
        request_path = "/api/v4/public/assets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_asset_status_to_object_v4(json_obj)

    async def get_orderbook(self, market: str, limit: Optional[int] = None, level: Optional[int] = None) -> Orderbook:
        """Get orderbook for the requested market

        This endpoint retrieves the current order book as two arrays (bids / asks) with additional parameters.
        Response is cached for 100 ms.

        Rate limit: 600 requests/10 sec.

        Args:
            market: Available market (e.g. BTC_USDT)
            limit: Orders depth quantity: 0 - 100. Not defined or 0 will return 100 entries.
            level: Optional parameter that allows API user to see different level of aggregation.
                   Level 0 – default level, no aggregation.
                   Starting from level 1 (lowest possible aggregation) and up to level 5.

        Returns:
            Orderbook: Orderbook for the requested market

        Example:
            ```python
            client = PublicV4Client()
            orderbook = await client.get_orderbook("BTC_USDT", limit=10, level=0)
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        request_path = f"/api/v4/public/orderbook/{market}"
        params = {}
        if limit is not None:
            params["limit"] = limit
        if level is not None:
            params["level"] = level

        full_url = self.request_url(request_path)
        if params:
            full_url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        json_obj = await base_get_request(full_url)

        return convert_orderbook_to_object(json_obj)

    async def get_depth(self, market: str) -> Depth:
        """Get depth price levels within ±2% of the market last price

        This endpoint retrieves depth price levels within ±2% of the market last price.
        Response is cached for 1 sec.

        Rate limit: 2000 requests/10 sec.

        Args:
            market: Available market (e.g. BTC_USDT)

        Returns:
            Depth: Depth price levels for the requested market

        Example:
            ```python
            client = PublicV4Client()
            depth = await client.get_depth("BTC_USDT")
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        request_path = f"/api/v4/public/orderbook/depth/{market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return Depth(**json_obj)

    async def get_recent_trades(self, market: str, trade_type: Optional[str] = None) -> RecentTrades:
        """Get recent trades for the requested market

        This endpoint retrieves the trades that have been executed recently on the requested market.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Args:
            market: Available market (e.g. BTC_USDT)
            trade_type: Can be buy or sell

        Returns:
            RecentTrades: Recent trades for the requested market

        Example:
            ```python
            client = PublicV4Client()
            trades = await client.get_recent_trades("BTC_USDT", trade_type="sell")
            ```
        """
        if not market:
            raise ValueError("Market parameter is required")

        request_path = f"/api/v4/public/trades/{market}"
        params = {}
        if trade_type is not None:
            if trade_type not in ["buy", "sell"]:
                raise ValueError("Type must be 'buy' or 'sell'")
            params["type"] = trade_type

        full_url = self.request_url(request_path)
        if params:
            full_url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])

        json_obj = await base_get_request(full_url)

        return convert_recent_trades_to_object(json_obj)

    async def get_fee(self) -> FeeResponse:
        """Get fee and min/max amount for deposits and withdraws

        This endpoint retrieves the list of fees and min/max amount for deposits and withdraws.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            FeeResponse: Fee and min/max amount for deposits and withdraws

        Example:
            ```python
            client = PublicV4Client()
            fee = await client.get_fee()
            ```
        """
        request_path = "/api/v4/public/fee"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return FeeResponse(json_obj)

    async def get_server_time(self) -> ServerTime:
        """Get server time

        This endpoint retrieves the current server time.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            ServerTime: Current server time

        Example:
            ```python
            client = PublicV4Client()
            time = await client.get_server_time()
            ```
        """
        request_path = "/api/v4/public/time"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return ServerTime(**json_obj)

    async def get_server_status(self) -> ServerStatus:
        """Get server status

        This endpoint retrieves the current API life-state.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            ServerStatus: Current API life-state

        Example:
            ```python
            client = PublicV4Client()
            status = await client.get_server_status()
            ```
        """
        request_path = "/api/v4/public/ping"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return ServerStatus(json_obj)

    async def get_collateral_markets(self) -> CollateralMarkets:
        """Get collateral markets list

        This endpoint returns the list of markets that available for collateral trading.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            CollateralMarkets: List of markets that available for collateral trading

        Example:
            ```python
            client = PublicV4Client()
            markets = await client.get_collateral_markets()
            ```
        """
        request_path = "/api/v4/public/collateral/markets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return CollateralMarkets(json_obj)

    async def get_futures_markets(self) -> FuturesMarkets:
        """Get available futures markets list

        This endpoint returns the list of available futures markets.
        Response is cached for 1 second.

        Rate limit: 2000 requests/10 sec.

        Returns:
            FuturesMarkets: List of available futures markets

        Example:
            ```python
            client = PublicV4Client()
            markets = await client.get_futures_markets()
            ```
        """
        request_path = "/api/v4/public/futures"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return FuturesMarkets(**json_obj)

    async def get_mining_pool_overview(self) -> MiningPoolOverview:
        """Get mining pool overview

        This endpoint returns an overall information about the current mining pool state.
        HashRate info represents in the H units.

        Rate limit: 1000 requests/10 sec.

        Returns:
            MiningPoolOverview: Overall information about the current mining pool state

        Example:
            ```python
            client = PublicV4Client()
            overview = await client.get_mining_pool_overview()
            ```
        """
        request_path = "/api/v4/public/mining-pool"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MiningPoolOverview(**json_obj)
