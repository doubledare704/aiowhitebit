"""WhiteBit Public API v4 client."""

from typing import Dict, Union

from aiowhitebit.clients.base import BaseClient
from aiowhitebit.config import APIEndpoints
from aiowhitebit.converters.public import (
    convert_asset_status_to_object_v4,
    convert_market_activity_to_object,
)
from aiowhitebit.models.public.v4 import (
    AssetStatus,
    CollateralMarkets,
    Depth,
    Fee,
    FeeResponse,
    FuturesMarkets,
    MaintenanceStatus,
    MarketActivity,
    MarketInfo,
    Orderbook,
    RecentTrade,
    RecentTrades,
    ServerStatus,
    ServerTime,
)
from aiowhitebit.models.public.v4.response import FeeDetails, MiningPoolOverview
from aiowhitebit.utils.rate_limiting import rate_limit
from aiowhitebit.utils.validation import WhitebitValidationError, validate_market


class PublicV4Client(BaseClient):
    """WhiteBit Public API v4 client"""

    @rate_limit(limit=2000, window=10.0)
    async def get_market_info(self) -> MarketInfo:
        """Get information about all available spot and futures markets"""
        return await self._make_request(APIEndpoints.MARKET_INFO, converter=lambda x: MarketInfo(x))

    @rate_limit(limit=2000, window=10.0)
    async def get_market_activity(self) -> MarketActivity:
        """Get 24-hour pricing and volume summary"""
        return await self._make_request(APIEndpoints.MARKET_ACTIVITY, converter=convert_market_activity_to_object)

    @rate_limit(limit=2000, window=10.0)
    async def get_asset_status_list(self) -> AssetStatus:
        """Get asset status list"""
        return await self._make_request(APIEndpoints.ASSET_STATUS, converter=convert_asset_status_to_object_v4)

    @rate_limit(limit=2000, window=10.0)
    async def get_maintenance_status(self) -> MaintenanceStatus:
        """Get system maintenance status

        Returns:
            MaintenanceStatus: System maintenance status
                status: "1" - system operational
                       "0" - system maintenance
        """
        return await self._make_request(APIEndpoints.MAINTENANCE_STATUS, converter=lambda x: MaintenanceStatus(**x))

    @rate_limit(limit=2000, window=10.0)
    async def get_orderbook(self, market: str, limit: int = None, level: int = None) -> Orderbook:
        """Get orderbook for specific market

        Args:
            market: Available market (e.g. BTC_USDT)
            limit: Limit of orderbook levels. Default: 100
            level: Aggregation level of orderbook:
                   1 - no aggregation (default)
                   2 - aggregation by 2 decimals
                   3 - aggregation by 3 decimals
                   ...and so on up to 8

        Returns:
            Orderbook: Current orderbook data including asks and bids

        Raises:
            WhitebitValidationError: If market is empty or parameters are invalid
        """
        validate_market(market)

        params = []

        if limit is not None:
            if not isinstance(limit, int) or limit < 1:
                raise WhitebitValidationError("Limit must be a positive integer")
            params.append(f"limit={limit}")

        if level is not None:
            if not isinstance(level, int) or level < 1 or level > 8:
                raise WhitebitValidationError("Level must be an integer between 1 and 8")
            params.append(f"level={level}")

        url = APIEndpoints.ORDERBOOK_V4.format(market=market)
        if params:
            url += "?" + "&".join(params)

        return await self._make_request(url, converter=lambda x: Orderbook(**x))

    @rate_limit(limit=2000, window=10.0)
    async def get_depth(self, market: str) -> Depth:
        """Get market depth within ±2% of the market last price

        Args:
            market: Available market (e.g. BTC_USDT)

        Returns:
            Depth: Market depth data including asks and bids within ±2% range

        Raises:
            WhitebitValidationError: If market is empty
        """
        validate_market(market)

        url = APIEndpoints.DEPTH_V4.format(market=market)
        return await self._make_request(url, converter=lambda x: Depth(**x))

    @rate_limit(limit=2000, window=10.0)
    async def get_recent_trades(self, market: str, trade_type: str = None) -> RecentTrades:
        """Get recent trades for specific market

        Args:
            market: Available market (e.g. BTC_USDT)
            trade_type: Optional filter by trade type: "buy" or "sell"

        Returns:
            RecentTrades: List of recent trades

        Raises:
            WhitebitValidationError: If market is empty or trade_type is invalid
        """
        validate_market(market)

        if trade_type is not None and trade_type not in ["buy", "sell"]:
            raise WhitebitValidationError("Trade type must be either 'buy' or 'sell'")

        url = APIEndpoints.TRADES_V4.format(market=market)
        if trade_type:
            url += f"?type={trade_type}"

        return await self._make_request(url, converter=lambda x: RecentTrades([RecentTrade(**trade) for trade in x]))

    @rate_limit(limit=2000, window=10.0)
    async def get_fee(self) -> FeeResponse:
        """Get fee information for all available assets

        Returns:
            FeeResponse: Dictionary mapping currency tickers to their fee information
        """

        def convert_fee_details(details) -> Union[FeeDetails, Dict[str, FeeDetails]]:
            if not details:  # Handle empty dictionaries
                return FeeDetails(min_amount="0", max_amount="0", fixed=None, flex=None)

            # Handle provider-specific fees (like USD case)
            if any(isinstance(v, dict) and "ticker" in v for v in details.values()):
                provider_fees = {}
                for provider, provider_details in details.items():
                    provider_fees[provider] = FeeDetails(
                        min_amount=provider_details.get("min_amount", "0"),
                        max_amount=provider_details.get("max_amount", "0"),
                        fixed=provider_details.get("fixed"),
                        flex=provider_details.get("flex"),
                        is_depositable=provider_details.get("is_depositable"),
                        is_withdrawal=provider_details.get("is_withdrawal"),
                        is_api_withdrawal=provider_details.get("is_api_withdrawal"),
                        is_api_depositable=provider_details.get("is_api_depositable"),
                        name=provider_details.get("name"),
                        ticker=provider_details.get("ticker"),
                    )
                return provider_fees

            # Handle simple fee details (like USDT case)
            return FeeDetails(
                min_amount=details.get("min_amount", "0"),
                max_amount=details.get("max_amount", "0"),
                fixed=details.get("fixed"),
                flex=details.get("flex"),
            )

        response = await self._make_request(APIEndpoints.FEE_V4)
        result = {}

        for display_name, details in response.items():
            try:
                fee = Fee(
                    ticker=details["ticker"],
                    name=details["name"],
                    providers=details.get("providers", []),
                    deposit=convert_fee_details(details.get("deposit", {})),
                    withdraw=convert_fee_details(details.get("withdraw", {})),
                    is_depositable=details.get("is_depositable", False),
                    is_withdrawal=details.get("is_withdrawal", False),
                    is_api_withdrawal=details.get("is_api_withdrawal", False),
                    is_api_depositable=details.get("is_api_depositable", False),
                )
                result[details["ticker"]] = fee
            except Exception as e:
                print(f"Error processing currency {display_name}:")
                print(f"Details: {details}")
                print(f"Error: {e!s}")
                raise

        return FeeResponse(result)

    @rate_limit(limit=2000, window=10.0)
    async def get_server_time(self) -> ServerTime:
        """Get current server time

        Returns:
            ServerTime: Current server time in Unix timestamp format
        """
        return await self._make_request(APIEndpoints.TIME_V4, converter=lambda x: ServerTime(**x))

    @rate_limit(limit=2000, window=10.0)
    async def get_server_status(self) -> ServerStatus:
        """Get server status by sending a ping request

        Returns:
            ServerStatus: Server status response, a list containing a single "pong" string
        """
        return await self._make_request(APIEndpoints.PING_V4, converter=lambda x: ServerStatus(x))

    @rate_limit(limit=2000, window=10.0)
    async def get_collateral_markets(self) -> CollateralMarkets:
        """Get list of markets available for collateral trading

        Returns:
            CollateralMarkets: List of market names that are available for collateral trading
        """
        return await self._make_request(APIEndpoints.COLLATERAL_MARKETS, converter=lambda x: CollateralMarkets(x))

    @rate_limit(limit=2000, window=10.0)
    async def get_futures_markets(self) -> FuturesMarkets:
        """Get list of available futures markets and their details

        Returns:
            FuturesMarkets: Information about all available futures markets including:
                - Ticker information
                - Price data
                - Volume data
                - Product details
                - Funding rates
                - Leverage brackets
        """
        return await self._make_request(
            APIEndpoints.FUTURES_MARKETS,
            converter=lambda x: FuturesMarkets(**x),  # Pass the entire response object
        )

    @rate_limit(limit=2000, window=10.0)
    async def get_mining_pool_overview(self) -> MiningPoolOverview:
        """Get mining pool overview information

        Returns:
            MiningPoolOverview: Information about the mining pool including:
                - Connection links
                - Location
                - Supported assets
                - Reward schemes
                - Number of workers
                - Current hash rate
                - Last 7 days hash rate
                - Recent blocks
        """
        return await self._make_request(APIEndpoints.MINING_POOL, converter=lambda x: MiningPoolOverview(**x))
