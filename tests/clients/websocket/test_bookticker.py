"""Tests for BookTicker WebSocket functionality."""

import unittest
from unittest.mock import AsyncMock

import pytest

from aiowhitebit.clients.websocket import PublicWebSocketClient, SubscribeRequest
from aiowhitebit.models.websocket import (
    BookTickerData,
    BookTickerResponse,
    WSResponse,
)


class TestBookTickerWebSocket(unittest.TestCase):
    """Test BookTicker WebSocket functionality."""

    def test_bookticker_subscribe_request(self):
        """Test BookTicker subscribe request generation."""
        request = SubscribeRequest.bookticker_subscribe("BTC_USDT")

        assert request["method"] == "bookTicker_subscribe"
        assert request["params"] == ["BTC_USDT"]
        assert "id" in request
        assert isinstance(request["id"], int)

    def test_bookticker_unsubscribe_request(self):
        """Test BookTicker unsubscribe request generation."""
        request = SubscribeRequest.bookticker_unsubscribe("BTC_USDT")

        assert request["method"] == "bookTicker_unsubscribe"
        assert request["params"] == ["BTC_USDT"]
        assert "id" in request
        assert isinstance(request["id"], int)


class TestBookTickerModels:
    """Test BookTicker data models."""

    def test_bookticker_data_model(self):
        """Test BookTickerData model validation."""
        data = {
            "symbol": "BTC_USDT",
            "bid_price": "45000.00",
            "bid_qty": "0.5",
            "ask_price": "45001.00",
            "ask_qty": "0.3",
        }

        bookticker = BookTickerData(**data)

        assert bookticker.symbol == "BTC_USDT"
        assert bookticker.bid_price == "45000.00"
        assert bookticker.bid_qty == "0.5"
        assert bookticker.ask_price == "45001.00"
        assert bookticker.ask_qty == "0.3"

    def test_bookticker_response_model(self):
        """Test BookTickerResponse model validation."""
        data = {
            "method": "bookTicker_update",
            "params": {
                "symbol": "BTC_USDT",
                "bid_price": "45000.00",
                "bid_qty": "0.5",
                "ask_price": "45001.00",
                "ask_qty": "0.3",
            },
            "event_time": 1640995200000,
            "update_id": 12345,
        }

        response = BookTickerResponse(**data)

        assert response.method == "bookTicker_update"
        assert response.params.symbol == "BTC_USDT"
        assert response.event_time == 1640995200000
        assert response.update_id == 12345

    def test_bookticker_response_optional_fields(self):
        """Test BookTickerResponse with optional fields."""
        data = {
            "method": "bookTicker_update",
            "params": {
                "symbol": "BTC_USDT",
                "bid_price": "45000.00",
                "bid_qty": "0.5",
                "ask_price": "45001.00",
                "ask_qty": "0.3",
            },
        }

        response = BookTickerResponse(**data)

        assert response.method == "bookTicker_update"
        assert response.params.symbol == "BTC_USDT"
        assert response.event_time is None
        assert response.update_id is None


@pytest.mark.asyncio
class TestBookTickerWebSocketClient:
    """Test BookTicker WebSocket client methods."""

    async def test_bookticker_subscribe(self):
        """Test BookTicker subscribe method."""
        # Create a mock WebSocket client
        mock_ws = AsyncMock()
        mock_response = {"id": 123, "result": {"status": "subscribed"}, "error": None}
        mock_ws.send_message.return_value = mock_response

        client = PublicWebSocketClient(ws=mock_ws)
        response = await client.bookticker_subscribe("BTC_USDT")

        # Verify the request was sent correctly
        mock_ws.send_message.assert_called_once()
        sent_data = mock_ws.send_message.call_args[0][0]
        assert sent_data["method"] == "bookTicker_subscribe"
        assert sent_data["params"] == ["BTC_USDT"]

        # Verify response
        assert isinstance(response, WSResponse)
        assert response.id == 123
        assert response.result["status"] == "subscribed"

    async def test_bookticker_unsubscribe(self):
        """Test BookTicker unsubscribe method."""
        # Create a mock WebSocket client
        mock_ws = AsyncMock()
        mock_response = {"id": 124, "result": {"status": "unsubscribed"}, "error": None}
        mock_ws.send_message.return_value = mock_response

        client = PublicWebSocketClient(ws=mock_ws)
        response = await client.bookticker_unsubscribe("BTC_USDT")

        # Verify the request was sent correctly
        mock_ws.send_message.assert_called_once()
        sent_data = mock_ws.send_message.call_args[0][0]
        assert sent_data["method"] == "bookTicker_unsubscribe"
        assert sent_data["params"] == ["BTC_USDT"]

        # Verify response
        assert isinstance(response, WSResponse)
        assert response.id == 124
        assert response.result["status"] == "unsubscribed"
