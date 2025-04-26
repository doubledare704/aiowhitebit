import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from aiowhitebit.clients.websocket.public import BaseWebSocketClient, PublicWebSocketClient
from aiowhitebit.models.websocket import WSRequest, WSResponse


class TestBaseWebSocketClient:
    @pytest.fixture
    def mock_websocket(self):
        """Mock websockets.connect and the connection object"""
        mock_connection = AsyncMock()
        mock_connection.send = AsyncMock()
        mock_connection.recv = AsyncMock(return_value=json.dumps({"id": 1, "result": "success"}))
        mock_connection.close = AsyncMock()
        
        with patch("websockets.connect", AsyncMock(return_value=mock_connection)) as mock_connect:
            yield mock_connection, mock_connect

    @pytest.mark.asyncio
    async def test_connect(self, mock_websocket):
        """Test connecting to the WebSocket server"""
        mock_connection, mock_connect = mock_websocket
        client = BaseWebSocketClient("wss://test.com")
        
        await client.connect()
        
        mock_connect.assert_called_once_with("wss://test.com")
        assert client.connection == mock_connection

    @pytest.mark.asyncio
    async def test_connect_already_connected(self, mock_websocket):
        """Test connecting when already connected"""
        mock_connection, mock_connect = mock_websocket
        client = BaseWebSocketClient("wss://test.com")
        client.connection = mock_connection
        
        await client.connect()
        
        mock_connect.assert_not_called()

    @pytest.mark.asyncio
    async def test_close(self, mock_websocket):
        """Test closing the WebSocket connection"""
        mock_connection, _ = mock_websocket
        client = BaseWebSocketClient("wss://test.com")
        client.connection = mock_connection
        
        await client.close()
        
        mock_connection.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_close_not_connected(self):
        """Test closing when not connected"""
        client = BaseWebSocketClient("wss://test.com")
        
        # Should not raise an exception
        await client.close()

    @pytest.mark.asyncio
    async def test_send_message(self, mock_websocket, caplog):
        """Test sending a message to the WebSocket server"""
        mock_connection, _ = mock_websocket
        client = BaseWebSocketClient("wss://test.com")
        
        request = {"method": "ping", "params": []}
        response = await client.send_message(request)
        
        mock_connection.send.assert_called_once_with(json.dumps(request))
        mock_connection.recv.assert_called_once()
        assert response == {"id": 1, "result": "success"}


class TestPublicWebSocketClient:
    @pytest.fixture
    def mock_base_client(self):
        """Mock BaseWebSocketClient"""
        mock_client = AsyncMock()
        mock_client.send_message = AsyncMock(return_value={"id": 1, "result": "success"})
        mock_client.close = AsyncMock()
        return mock_client

    @pytest.mark.asyncio
    async def test_base_ws_requester(self, mock_base_client):
        """Test the base WebSocket requester method"""
        client = PublicWebSocketClient(mock_base_client)
        request = WSRequest(method="test", params=["param1", "param2"])
        mock_base_client.send_message.return_value = {"result": "test_result", "id": 1}
        
        response = await client.base_ws_requester(request)
        
        mock_base_client.send_message.assert_called_once_with(request.model_dump())
        assert isinstance(response, WSResponse)
        assert response.result == "test_result"

    @pytest.mark.asyncio
    async def test_ping(self, mock_base_client):
        """Test the ping method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.ping()
        
        # Check that send_message was called with the correct parameters
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "ping"
        assert called_args["params"] == []

    @pytest.mark.asyncio
    async def test_time(self, mock_base_client):
        """Test the time method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.time()
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "time"
        assert called_args["params"] == []

    @pytest.mark.asyncio
    async def test_kline(self, mock_base_client):
        """Test the kline method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.kline("BTC_USDT", 1579569940, 1580894800, 900)
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "candles_request"
        assert called_args["params"] == ["BTC_USDT", 1579569940, 1580894800, 900]

    @pytest.mark.asyncio
    async def test_last_price(self, mock_base_client):
        """Test the last_price method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.last_price("BTC_USDT")
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "lastprice_request"
        assert called_args["params"] == ["BTC_USDT"]

    @pytest.mark.asyncio
    async def test_market_stats(self, mock_base_client):
        """Test the market_stats method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.market_stats("BTC_USDT", 86400)
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "market_request"
        assert called_args["params"] == ["BTC_USDT", 86400]

    @pytest.mark.asyncio
    async def test_market_stats_today(self, mock_base_client):
        """Test the market_stats_today method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.market_stats_today("BTC_USDT")
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "marketToday_query"
        assert called_args["params"] == ["BTC_USDT"]

    @pytest.mark.asyncio
    async def test_market_trades(self, mock_base_client):
        """Test the market_trades method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.market_trades("BTC_USDT", 100, 41358445)
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "trades_request"
        assert called_args["params"] == ["BTC_USDT", 100, 41358445]

    @pytest.mark.asyncio
    async def test_market_depth(self, mock_base_client):
        """Test the market_depth method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.market_depth("BTC_USDT", 100, "0.0001")
        
        called_args = mock_base_client.send_message.call_args[0][0]
        assert called_args["method"] == "depth_request"
        assert called_args["params"] == ["BTC_USDT", 100, "0.0001"]

    @pytest.mark.asyncio
    async def test_close(self, mock_base_client):
        """Test the close method"""
        client = PublicWebSocketClient(mock_base_client)
        
        await client.close()
        
        mock_base_client.close.assert_called_once()

    def test_get_public_websocket_client(self):
        """Test the get_public_websocket_client function"""
        from aiowhitebit.clients.websocket.public import get_public_websocket_client
        
        client = get_public_websocket_client()
        
        assert isinstance(client, PublicWebSocketClient)
        assert isinstance(client.ws, BaseWebSocketClient)