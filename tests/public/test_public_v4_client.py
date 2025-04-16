import unittest

import pytest

from aiowhitebit.clients.public import PublicV4Client
from aiowhitebit.models.public.v4 import (
    AssetStatus,
    CollateralMarkets,
    Depth,
    FeeResponse,
    FuturesMarkets,
    MaintenanceStatus,
    MarketActivity,
    MarketInfo,
    MiningPoolOverview,
    Orderbook,
    RecentTrades,
    ServerStatus,
    ServerTime,
)


class TestPublicV4Client(unittest.TestCase):
    def setUp(self):
        self.client = PublicV4Client()
        self.base_url = "https://whitebit.com"

    def test_init(self):
        self.assertEqual(self.client.base_url, self.base_url)

    def test_request_url(self):
        path = "/api/v4/public/markets"
        expected_url = f"{self.base_url}{path}"
        self.assertEqual(self.client.request_url(path), expected_url)


class TestPublicV4ClientAsync:
    @pytest.fixture
    def client(self):
        return PublicV4Client()

    @pytest.mark.asyncio
    async def test_get_maintenance_status(self, client):
        result = await client.get_maintenance_status()

        # Basic validation
        assert isinstance(result, MaintenanceStatus)
        assert result.status in ["0", "1"]

    @pytest.mark.asyncio
    async def test_get_market_info(self, client):
        result = await client.get_market_info()

        # Basic validation
        assert isinstance(result, MarketInfo)
        assert len(result) > 0

        # Get BTC_USDT market as it should always exist
        btc_usdt_market = next((market for market in result if market["name"] == "BTC_USDT"), None)
        assert btc_usdt_market is not None
        assert btc_usdt_market["stock"] == "BTC"
        assert btc_usdt_market["money"] == "USDT"
        assert "tradesEnabled" in btc_usdt_market

    @pytest.mark.asyncio
    async def test_get_market_activity(self, client):
        result = await client.get_market_activity()

        # Basic validation
        assert isinstance(result, MarketActivity)
        assert len(result) > 0

        # Get BTC_USDT market activity as it should always exist
        btc_usdt_activity = result.get("BTC_USDT")
        assert btc_usdt_activity is not None
        assert btc_usdt_activity.base_id is not None
        assert btc_usdt_activity.quote_id is not None
        assert btc_usdt_activity.last_price is not None
        assert btc_usdt_activity.quote_volume is not None
        assert btc_usdt_activity.base_volume is not None
        assert btc_usdt_activity.isFrozen is not None
        assert btc_usdt_activity.change is not None

    @pytest.mark.asyncio
    async def test_get_asset_status_list(self, client):
        result = await client.get_asset_status_list()

        # Basic validation
        assert isinstance(result, AssetStatus)
        assert len(result) > 0

        # Get BTC asset as it should always exist
        btc_asset = result.get("BTC")
        assert btc_asset is not None
        assert btc_asset.name is not None
        assert btc_asset.unified_cryptoasset_id is not None
        assert btc_asset.can_withdraw is not None
        assert btc_asset.can_deposit is not None
        assert btc_asset.min_withdraw is not None
        assert btc_asset.max_withdraw is not None
        assert btc_asset.maker_fee is not None
        assert btc_asset.taker_fee is not None
        assert btc_asset.min_deposit is not None
        assert btc_asset.max_deposit is not None
        assert btc_asset.currency_precision is not None
        assert btc_asset.is_memo is not None
        assert btc_asset.networks is not None
        assert btc_asset.limits is not None
        assert btc_asset.confirmations is not None

    @pytest.mark.asyncio
    async def test_get_orderbook(self, client):
        market = "BTC_USDT"
        result = await client.get_orderbook(market)

        # Basic validation
        assert isinstance(result, Orderbook)
        assert result.ticker_id == market
        assert result.timestamp is not None
        assert len(result.asks) > 0
        assert len(result.bids) > 0

    @pytest.mark.asyncio
    async def test_get_depth(self, client):
        market = "BTC_USDT"
        result = await client.get_depth(market)

        # Basic validation
        assert isinstance(result, Depth)
        assert result.ticker_id == market
        assert result.timestamp is not None
        assert len(result.asks) > 0
        assert len(result.bids) > 0

    @pytest.mark.asyncio
    async def test_get_recent_trades(self, client):
        market = "BTC_USDT"
        result = await client.get_recent_trades(market)

        # Basic validation
        assert isinstance(result, RecentTrades)
        assert len(result) > 0

        # Verify first trade structure
        first_trade = result[0]
        assert first_trade.tradeID is not None
        assert first_trade.price is not None
        assert first_trade.quote_volume is not None
        assert first_trade.base_volume is not None
        assert first_trade.trade_timestamp is not None
        assert first_trade.type in ["buy", "sell"]

    @pytest.mark.asyncio
    async def test_get_fee(self, client):
        result = await client.get_fee()

        # Basic validation
        assert isinstance(result, FeeResponse)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_server_time(self, client):
        result = await client.get_server_time()

        # Basic validation
        assert isinstance(result, ServerTime)
        assert result.time is not None
        assert result.time > 0

    @pytest.mark.asyncio
    async def test_get_server_status(self, client):
        result = await client.get_server_status()

        # Basic validation
        assert isinstance(result, ServerStatus)
        assert len(result) > 0
        assert result[0] == "pong"

    @pytest.mark.asyncio
    async def test_get_collateral_markets(self, client):
        result = await client.get_collateral_markets()

        # Basic validation
        assert isinstance(result, CollateralMarkets)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_futures_markets(self, client):
        result = await client.get_futures_markets()

        # Basic validation
        assert isinstance(result, FuturesMarkets)
        assert result.success is True
        assert result.message is None
        assert len(result.result) > 0

        # Verify first futures market structure
        first_market = result.result[0]
        assert first_market.ticker_id is not None
        assert first_market.stock_currency is not None
        assert first_market.money_currency is not None
        assert first_market.last_price is not None
        assert first_market.stock_volume is not None
        assert first_market.money_volume is not None
        assert first_market.bid is not None
        assert first_market.ask is not None
        assert first_market.high is not None
        assert first_market.low is not None
        assert first_market.product_type is not None
        assert first_market.open_interest is not None
        assert first_market.index_price is not None
        assert first_market.index_name is not None
        assert first_market.index_currency is not None
        assert first_market.funding_rate is not None
        assert first_market.next_funding_rate_timestamp is not None
        assert first_market.brackets is not None
        assert first_market.max_leverage is not None

    @pytest.mark.asyncio
    async def test_get_mining_pool_overview(self, client):
        result = await client.get_mining_pool_overview()

        # Basic validation
        assert isinstance(result, MiningPoolOverview)
        assert result.data is not None
