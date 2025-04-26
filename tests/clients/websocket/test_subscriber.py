import json
import threading
from unittest.mock import MagicMock, patch

import pytest

from aiowhitebit.clients.websocket.subscriber import (
    SubscribeRequest,
    ws_subscribe_builder,
    infinite_sequence,
)
from aiowhitebit.models.websocket import WSRequest


class TestInfiniteSequence:
    def test_infinite_sequence(self):
        """Test the infinite_sequence generator"""
        gen = infinite_sequence()
        assert next(gen) == 1
        assert next(gen) == 2
        assert next(gen) == 3


class TestSubscribeRequest:
    def test_candles_subscribe(self):
        """Test candles_subscribe method"""
        market = "BTC_USDT"
        interval = 900
        
        result = SubscribeRequest.candles_subscribe(market, interval)
        
        assert result["method"] == "candles_subscribe"
        assert result["params"] == [market, interval]
        assert isinstance(result["id"], int)

    def test_lastprice_subscribe(self):
        """Test lastprice_subscribe method"""
        markets = ["BTC_USDT", "ETH_BTC"]
        
        result = SubscribeRequest.lastprice_subscribe(markets)
        
        assert result["method"] == "lastprice_subscribe"
        assert result["params"] == markets
        assert isinstance(result["id"], int)

    def test_market_subscribe(self):
        """Test market_subscribe method"""
        markets = ["BTC_USDT", "ETH_BTC"]
        
        result = SubscribeRequest.market_subscribe(markets)
        
        assert result["method"] == "market_subscribe"
        assert result["params"] == markets
        assert isinstance(result["id"], int)

    def test_market_today_subscribe(self):
        """Test market_today_subscribe method"""
        markets = ["BTC_USDT", "ETH_BTC"]
        
        result = SubscribeRequest.market_today_subscribe(markets)
        
        assert result["method"] == "marketToday_subscribe"
        assert result["params"] == markets
        assert isinstance(result["id"], int)

    def test_trades_subscribe(self):
        """Test trades_subscribe method"""
        markets = ["BTC_USDT", "ETH_BTC"]
        
        result = SubscribeRequest.trades_subscribe(markets)
        
        assert result["method"] == "trades_subscribe"
        assert result["params"] == markets
        assert isinstance(result["id"], int)

    def test_depth_subscribe(self):
        """Test depth_subscribe method with default parameters"""
        market = "BTC_USDT"
        
        result = SubscribeRequest.depth_subscribe(market)
        
        assert result["method"] == "depth_subscribe"
        assert result["params"] == [market, 100, "0", True]
        assert isinstance(result["id"], int)

    def test_depth_subscribe_with_params(self):
        """Test depth_subscribe method with custom parameters"""
        market = "BTC_USDT"
        limit = 50
        price_intervals = "0.0001"
        multiple_sub = False
        
        result = SubscribeRequest.depth_subscribe(
            market, limit, price_intervals, multiple_sub
        )
        
        assert result["method"] == "depth_subscribe"
        assert result["params"] == [market, limit, price_intervals, multiple_sub]
        assert isinstance(result["id"], int)


class TestWsSubscribeBuilder:
    @patch("aiowhitebit.clients.websocket.subscriber.websocket.WebSocketApp")
    def test_ws_subscribe_builder_default_callbacks(self, mock_websocket_app, capsys):
        """Test ws_subscribe_builder with default callbacks"""
        # Create a mock WebSocketApp
        mock_ws = MagicMock()
        mock_websocket_app.return_value = mock_ws
        
        # Create a subscribe message
        sub_msg = {"method": "ping", "params": [], "id": 1}
        
        # Call the function
        ws_subscribe_builder(sub_msg)
        
        # Verify WebSocketApp was created with the correct parameters
        mock_websocket_app.assert_called_once()
        assert mock_websocket_app.call_args[1]["on_open"] is not None
        assert mock_websocket_app.call_args[1]["on_message"] is not None
        assert mock_websocket_app.call_args[1]["on_close"] is not None
        
        # Verify run_forever was called
        mock_ws.run_forever.assert_called_once()
        
        # Test the default callbacks
        on_open = mock_websocket_app.call_args[1]["on_open"]
        on_message = mock_websocket_app.call_args[1]["on_message"]
        on_close = mock_websocket_app.call_args[1]["on_close"]
        
        # Call the callbacks
        on_open(mock_ws)
        captured = capsys.readouterr()
        assert ">>> Opened subscriber: ping" in captured.out
        
        on_message(mock_ws, json.dumps({"result": "success"}))
        captured = capsys.readouterr()
        assert "<<<<Received : " in captured.out
        assert "ping" in captured.out
        
        on_close(mock_ws)
        captured = capsys.readouterr()
        assert "Closed connection" in captured.out

    @patch("aiowhitebit.clients.websocket.subscriber.websocket.WebSocketApp")
    def test_ws_subscribe_builder_custom_callbacks(self, mock_websocket_app):
        """Test ws_subscribe_builder with custom callbacks"""
        # Create a mock WebSocketApp
        mock_ws = MagicMock()
        mock_websocket_app.return_value = mock_ws
        
        # Create custom callbacks
        on_open_called = False
        on_message_called = False
        on_close_called = False
        
        def custom_on_open(wsapp):
            nonlocal on_open_called
            on_open_called = True
        
        def custom_on_message(wsapp, message):
            nonlocal on_message_called
            on_message_called = True
        
        def custom_on_close(wsapp):
            nonlocal on_close_called
            on_close_called = True
        
        # Create a subscribe message
        sub_msg = {"method": "ping", "params": [], "id": 1}
        
        # Call the function
        ws_subscribe_builder(
            sub_msg,
            on_message_callback=custom_on_message,
            on_open_callback=custom_on_open,
            on_close_callback=custom_on_close,
        )
        
        # Verify WebSocketApp was created with the correct parameters
        mock_websocket_app.assert_called_once()
        
        # Test the custom callbacks
        on_open = mock_websocket_app.call_args[1]["on_open"]
        on_message = mock_websocket_app.call_args[1]["on_message"]
        on_close = mock_websocket_app.call_args[1]["on_close"]
        
        # Call the callbacks
        on_open(mock_ws)
        assert on_open_called is True
        
        on_message(mock_ws, json.dumps({"result": "success"}))
        assert on_message_called is True
        
        on_close(mock_ws)
        assert on_close_called is True


@pytest.mark.integration
class TestSubscriberIntegration:
    """Integration tests for the subscriber module.
    
    These tests require an active internet connection and will connect to the WhiteBit WebSocket API.
    They are marked with the 'integration' marker and can be skipped with:
    pytest -m "not integration"
    """
    
    def test_candles_subscribe_integration(self):
        """Test candles_subscribe with the actual WhiteBit API"""
        # This is a simple integration test that connects to the API
        # and verifies that we receive a response
        
        received_message = False
        
        def on_message(wsapp, message):
            nonlocal received_message
            data = json.loads(message)
            # Check if we received a valid response
            if "method" in data and data["method"] == "candles_update":
                received_message = True
                wsapp.close()
        
        # Create a subscribe request
        request = SubscribeRequest.candles_subscribe("BTC_USDT", 900)
        
        # Start the WebSocket in a separate thread
        thread = threading.Thread(
            target=ws_subscribe_builder,
            args=(request,),
            kwargs={"on_message_callback": on_message},
            daemon=True,
        )
        thread.start()
        
        # Wait for up to 10 seconds for a response
        thread.join(10)
        
        # Verify that we received a message
        assert received_message, "Did not receive a candles_update message within the timeout"