import unittest

import pytest

from aiowhitebit.clients.public import PublicV1Client

# Use the new model imports
from aiowhitebit.models.public.v1 import (
    MarketInfo,
    Tickers,
    MarketSingleResponse,
    Kline,
    Symbols,
    OrderDepth,
    TradeHistory,
)


class TestPublicV1Client(unittest.TestCase):
    def setUp(self):
        self.client = PublicV1Client()
        self.base_url = "https://whitebit.com"

    def test_init(self):
        self.assertEqual(self.client.base_url, self.base_url)

    def test_request_url(self):
        path = "/api/v1/public/markets"
        expected_url = f"{self.base_url}{path}"
        self.assertEqual(self.client.request_url(path), expected_url)


class TestPublicV1ClientAsync:
    @pytest.fixture
    def client(self):
        return PublicV1Client()

    @pytest.mark.asyncio
    async def test_get_market_info(self, client):
        # Create a test client with a mocked _get_request method
        mock_response = {
            "success": True,
            "message": None,
            "result": [
                {
                    "name": "BTC_USDT",
                    "stock": "BTC",
                    "money": "USDT",
                    "stockPrec": 6,
                    "moneyPrec": 2,
                    "feePrec": 4,
                    "makerFee": 0.001,
                    "takerFee": 0.001,
                    "minAmount": 0.0001,
                }
            ],
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_market_info()

        # Verify the result
        assert isinstance(result, MarketInfo)
        assert result.success is True
        assert result.message is None
        assert len(result.result) == 1
        assert result.result[0].name == "BTC_USDT"
        assert result.result[0].stock == "BTC"
        assert result.result[0].money == "USDT"

    @pytest.mark.asyncio
    async def test_get_tickers(self, client):
        # Mock response data
        mock_response = {
            "success": True,
            "message": None,
            "result": {
                "BTC_USDT": {
                    "ticker": {
                        "bid": "9412.1",
                        "ask": "9416.33",
                        "low": "9203.13",
                        "high": "9469.99",
                        "last": "9414.4",
                        "vol": "27324.819448",
                        "deal": "254587570.43407191",
                        "change": "1.53",
                    },
                    "at": 159423219,
                }
            },
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_tickers()

        # Verify the result
        assert isinstance(result, Tickers)
        assert result.success is True
        assert result.message is None
        assert len(result.result) == 1
        assert result.result[0].name == "BTC_USDT"
        assert result.result[0].bid == 9412.1
        assert result.result[0].ask == 9416.33

    @pytest.mark.asyncio
    async def test_get_single_market(self, client):
        # Mock response data
        mock_response = {
            "success": True,
            "message": None,
            "result": {
                "open": "9267.98",
                "bid": "9417.4",
                "ask": "9421.64",
                "low": "9203.13",
                "high": "9469.99",
                "last": "9419.55",
                "volume": "27303.824558",
                "deal": "254399191.68843464",
                "change": "1.63",
            },
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_single_market("BTC_USDT")

        # Verify the result
        assert isinstance(result, MarketSingleResponse)
        assert result.success is True
        assert result.message is None
        assert float(result.result.open) == 9267.98
        assert float(result.result.bid) == 9417.4
        assert float(result.result.ask) == 9421.64

    @pytest.mark.asyncio
    async def test_get_single_market_validation(self, client):
        # Test validation for empty market parameter
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_single_market("")

    @pytest.mark.asyncio
    async def test_get_kline_market(self, client):
        # Mock response data
        mock_response = {
            "success": True,
            "message": None,
            "result": [[1631440800, "45865.62", "45958.14", "45981.3", "45750.23", "15.327634", "703140.24230131"]],
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_kline_market("BTC_USDT", start=1596848400, end=1596927600, interval="1h", limit=100)

        # Verify the result
        assert isinstance(result, Kline)
        assert result.success is True
        assert result.message is None
        assert len(result.result) == 1
        assert result.result[0].time_seconds == 1631440800
        assert result.result[0].open == 45865.62
        assert result.result[0].close == 45958.14

    @pytest.mark.asyncio
    async def test_get_kline_market_validation(self, client):
        # Test validation for empty market parameter
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_kline_market("")

        # Test validation for invalid interval
        with pytest.raises(ValueError, match="Invalid interval"):
            await client.get_kline_market("BTC_USDT", interval="invalid")

        # Test validation for invalid limit
        with pytest.raises(ValueError, match="Limit must be between 1 and 1440"):
            await client.get_kline_market("BTC_USDT", limit=0)
        with pytest.raises(ValueError, match="Limit must be between 1 and 1440"):
            await client.get_kline_market("BTC_USDT", limit=1441)

        # Test validation for start > end
        with pytest.raises(ValueError, match="Start time cannot be greater than end time"):
            await client.get_kline_market("BTC_USDT", start=1596927600, end=1596848400)

    @pytest.mark.asyncio
    async def test_get_symbols(self, client):
        # Mock response data
        mock_response = {"success": True, "message": None, "result": ["BTC_USDT", "ETH_BTC", "ETH_USDT"]}

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_symbols()

        # Verify the result
        assert isinstance(result, Symbols)
        assert result.success is True
        assert result.message is None
        assert len(result.result) == 3
        assert "BTC_USDT" in result.result
        assert "ETH_BTC" in result.result
        assert "ETH_USDT" in result.result

    @pytest.mark.asyncio
    async def test_get_order_depth(self, client):
        # Mock response data
        mock_response = {
            "asks": [["9431.9", "0.705088"], ["9433.67", "0.324509"]],
            "bids": [["9427.65", "0.547909"], ["9427.3", "0.669249"]],
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_order_depth("BTC_USDT", limit=50)

        # Verify the result
        assert isinstance(result, OrderDepth)
        assert len(result.asks) == 2
        assert len(result.bids) == 2
        assert result.asks[0].price == 9431.9
        assert result.asks[0].amount == 0.705088
        assert result.bids[0].price == 9427.65
        assert result.bids[0].amount == 0.547909

    @pytest.mark.asyncio
    async def test_get_order_depth_validation(self, client):
        # Test validation for empty market parameter
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_order_depth("")

        # Test validation for invalid limit
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await client.get_order_depth("BTC_USDT", limit=0)
        with pytest.raises(ValueError, match="Limit must be between 1 and 100"):
            await client.get_order_depth("BTC_USDT", limit=101)

    @pytest.mark.asyncio
    async def test_get_trade_history(self, client):
        # Mock response data
        mock_response = {
            "success": True,
            "message": None,
            "result": [
                {"id": 156720314, "time": 1594240477.849703, "price": "9429.66", "amount": "0.002784", "type": "sell"},
                {"id": 156720309, "time": 1594240476.832347, "price": "9429.66", "amount": "0.002455", "type": "sell"},
            ],
        }

        # Create a mock for _get_request
        async def mock_get_request(url):
            return mock_response

        # Replace the _get_request method
        client._get_request = mock_get_request

        # Call the method
        result = await client.get_trade_history("BTC_USDT", last_id=6, limit=100)

        # Verify the result
        assert isinstance(result, TradeHistory)
        assert result.success is True
        assert result.message is None
        assert len(result.result) == 2
        assert result.result[0].id == 156720314
        assert result.result[0].time == 1594240477.849703
        assert result.result[0].price == 9429.66
        assert result.result[0].amount == 0.002784
        assert result.result[0].type == "sell"

    @pytest.mark.asyncio
    async def test_get_trade_history_validation(self, client):
        # Test validation for empty market parameter
        with pytest.raises(ValueError, match="Market parameter is required"):
            await client.get_trade_history("", last_id=6)

        # Test validation for negative last_id
        with pytest.raises(ValueError, match="Last ID must be a positive integer"):
            await client.get_trade_history("BTC_USDT", last_id=-1)
