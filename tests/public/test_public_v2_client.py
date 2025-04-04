import unittest

import pytest
from datetime import datetime

from aiowhitebit.clients.public import PublicV2Client
from aiowhitebit.models.public.v2 import (
    MarketInfo,
    Tickers,
    RecentTrades,
    FeeResponse,
    AssetStatus,
    OrderDepthV2,
)


class TestPublicV2Client(unittest.TestCase):
    def setUp(self):
        self.client = PublicV2Client()
        self.base_url = "https://whitebit.com"

    def test_init(self):
        self.assertEqual(self.client.base_url, self.base_url)

    def test_request_url(self):
        path = "/api/v2/public/markets"
        expected_url = f"{self.base_url}{path}"
        self.assertEqual(self.client.request_url(path), expected_url)


class TestPublicV2ClientAsync:
    @pytest.fixture
    def client(self):
        return PublicV2Client()

    @pytest.mark.asyncio
    async def test_get_market_info(self, client):
        result = await client.get_market_info()

        # Basic validation
        assert isinstance(result, MarketInfo)
        assert result.success is True
        assert result.message is None
        assert len(result.result) > 0

        # Get BTC_USDT market as it should always exist
        btc_usdt_market = next((market for market in result.result if market.name == "BTC_USDT"), None)
        assert btc_usdt_market is not None

        # Verify structure of BTC_USDT market
        assert isinstance(btc_usdt_market.name, str)
        assert isinstance(btc_usdt_market.stock, str)
        assert isinstance(btc_usdt_market.money, str)
        assert isinstance(btc_usdt_market.stockPrec, int)
        assert isinstance(btc_usdt_market.moneyPrec, int)
        assert isinstance(btc_usdt_market.feePrec, int)
        assert isinstance(btc_usdt_market.makerFee, (int, float))
        assert isinstance(btc_usdt_market.takerFee, (int, float))
        assert isinstance(btc_usdt_market.minAmount, (int, float))
        assert isinstance(btc_usdt_market.minTotal, (int, float))
        assert isinstance(btc_usdt_market.tradesEnabled, bool)

        # Verify BTC_USDT specific values
        assert btc_usdt_market.stock == "BTC"
        assert btc_usdt_market.money == "USDT"
        assert btc_usdt_market.stockPrec >= 0
        assert btc_usdt_market.moneyPrec >= 0
        assert btc_usdt_market.feePrec >= 0
        assert btc_usdt_market.makerFee >= 0
        assert btc_usdt_market.takerFee >= 0
        assert btc_usdt_market.minAmount > 0
        assert btc_usdt_market.minTotal > 0

    @pytest.mark.asyncio
    async def test_get_tickers(self, client):
        result = await client.get_tickers()

        # Verify the result structure
        assert isinstance(result, Tickers)
        assert result.success is True
        assert result.message is None
        assert len(result.result) > 0

        # Get BTC_USDT ticker as it should always exist
        btc_usdt_ticker = next((ticker for ticker in result.result if ticker.tradingPairs == "BTC_USDT"), None)
        assert btc_usdt_ticker is not None

        # Verify ticker structure
        assert isinstance(btc_usdt_ticker.lastUpdateTimestamp, datetime)
        assert isinstance(btc_usdt_ticker.tradingPairs, str)
        assert isinstance(btc_usdt_ticker.lastPrice, (int, float))
        assert isinstance(btc_usdt_ticker.lowestAsk, (int, float))
        assert isinstance(btc_usdt_ticker.highestBid, (int, float))
        assert isinstance(btc_usdt_ticker.baseVolume24h, (int, float))
        assert isinstance(btc_usdt_ticker.quoteVolume24h, (int, float))
        assert isinstance(btc_usdt_ticker.tradesEnabled, bool)

        # Verify reasonable values
        assert btc_usdt_ticker.lastPrice > 0
        assert btc_usdt_ticker.lowestAsk > 0
        assert btc_usdt_ticker.highestBid > 0
        assert btc_usdt_ticker.baseVolume24h >= 0
        assert btc_usdt_ticker.quoteVolume24h >= 0

    @pytest.mark.asyncio
    async def test_get_recent_trades(self, client):
        market = "BTC_USDT"
        result = await client.get_recent_trades(market)

        # Verify the result structure
        assert isinstance(result, RecentTrades)
        assert result.success is True
        assert result.message is None
        assert len(result.result) > 0

        # Verify first trade structure
        first_trade = result.result[0]
        assert isinstance(first_trade.tradeId, int)
        assert isinstance(first_trade.price, (int, float))
        assert isinstance(first_trade.volume, (int, float))
        assert isinstance(first_trade.time, datetime)
        assert isinstance(first_trade.isBuyerMaker, bool)

        # Verify reasonable values
        assert first_trade.price > 0
        assert first_trade.volume > 0
        assert first_trade.tradeId > 0

    @pytest.mark.asyncio
    async def test_get_recent_trades_with_empty_market(self, client):
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_recent_trades("")

    @pytest.mark.asyncio
    async def test_get_fee(self, client):
        result = await client.get_fee()

        # Verify the result structure
        assert isinstance(result, FeeResponse)
        assert result.success is True
        assert result.message is None

        # Verify fee data
        assert hasattr(result.result, "makerFee")
        assert hasattr(result.result, "takerFee")
        assert isinstance(result.result.makerFee, (int, float))
        assert isinstance(result.result.takerFee, (int, float))

        # Verify fee values are within reasonable range (0-100%)
        assert 0 <= result.result.makerFee <= 100
        assert 0 <= result.result.takerFee <= 100

    @pytest.mark.asyncio
    async def test_get_asset_status_list(self, client):
        result = await client.get_asset_status_list()

        # Verify basic structure
        assert isinstance(result, AssetStatus)
        assert result.success is True
        assert result.message is None
        assert len(result.result) > 0

        # Get BTC asset as it should always exist
        btc_asset = next((asset for asset in result.result if asset.asset_name == "BTC"), None)
        assert btc_asset is not None

        # Verify BTC asset structure
        assert isinstance(btc_asset.id, str)
        assert isinstance(btc_asset.name, str)
        assert isinstance(btc_asset.canWithdraw, bool)
        assert isinstance(btc_asset.canDeposit, bool)
        assert isinstance(btc_asset.minWithdrawal, (int, float))
        assert isinstance(btc_asset.maxWithdrawal, (int, float))
        assert isinstance(btc_asset.makerFee, (int, float))
        assert isinstance(btc_asset.takerFee, (int, float))

        # Verify BTC has valid values
        assert btc_asset.name == "Bitcoin"
        assert btc_asset.minWithdrawal >= 0
        assert btc_asset.makerFee >= 0
        assert btc_asset.takerFee >= 0

    @pytest.mark.asyncio
    async def test_get_order_depth(self, client):
        market = "BTC_USDT"
        result = await client.get_order_depth(market)

        # Basic structure validation
        assert result is not None
        assert isinstance(result, OrderDepthV2)

        # Verify we have data arrays
        assert isinstance(result.asks, list)
        assert isinstance(result.bids, list)
        assert len(result.asks) > 0
        assert len(result.bids) > 0

        all_asks = result.asks
        all_bids = result.bids

        # Verify each entry is a list with price and amount
        assert isinstance(all_asks, list)
        assert isinstance(all_bids, list)
        assert len(all_asks) > 0
        assert len(all_bids) > 0

        # Verify we can convert values to float
        ask_price = float(all_asks[0].price)
        ask_amount = float(all_asks[0].amount)
        bid_price = float(all_bids[0].price)
        bid_amount = float(all_bids[0].amount)

        # Verify values are positive
        assert ask_price > 0
        assert ask_amount > 0
        assert bid_price > 0
        assert bid_amount > 0

        # Verify price ordering
        if len(result.asks) > 1:
            assert float(all_asks[0].price) < float(all_asks[1].price)  # Ascending asks
        if len(result.bids) > 1:
            assert float(all_bids[0].price) > float(all_bids[1].price)  # Descending bids

    @pytest.mark.asyncio
    async def test_get_order_depth_with_empty_market(self, client):
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_order_depth("")
