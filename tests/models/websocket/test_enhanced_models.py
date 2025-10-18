"""Tests for enhanced WebSocket models with event metadata."""

import unittest

from aiowhitebit.models.base import BaseWebSocketResponse
from aiowhitebit.models.websocket import (
    DepthData,
    DepthUpdateResponse,
    WSResponse,
)


class TestEnhancedWebSocketModels(unittest.TestCase):
    """Test enhanced WebSocket models with event metadata."""

    def test_base_websocket_response_with_metadata(self):
        """Test BaseWebSocketResponse with event metadata fields."""
        data = {"event_time": 1640995200000, "update_id": 12345}

        response = BaseWebSocketResponse(**data)

        assert response.event_time == 1640995200000
        assert response.update_id == 12345

    def test_base_websocket_response_without_metadata(self):
        """Test BaseWebSocketResponse without event metadata fields (backward compatibility)."""
        response = BaseWebSocketResponse()

        assert response.event_time is None
        assert response.update_id is None

    def test_ws_response_inherits_metadata(self):
        """Test that WSResponse inherits event metadata fields."""
        data = {"id": 123, "result": {"status": "ok"}, "error": None, "event_time": 1640995200000, "update_id": 12345}

        response = WSResponse(**data)

        assert response.id == 123
        assert response.result["status"] == "ok"
        assert response.event_time == 1640995200000
        assert response.update_id == 12345

    def test_depth_data_model(self):
        """Test DepthData model validation."""
        data = {
            "market": "BTC_USDT",
            "bids": [["45000.00", "0.5"], ["44999.00", "0.3"]],
            "asks": [["45001.00", "0.4"], ["45002.00", "0.6"]],
        }

        depth = DepthData(**data)

        assert depth.market == "BTC_USDT"
        assert len(depth.bids) == 2
        assert len(depth.asks) == 2
        assert depth.bids[0] == ["45000.00", "0.5"]
        assert depth.asks[0] == ["45001.00", "0.4"]

    def test_depth_update_response_with_metadata(self):
        """Test DepthUpdateResponse with event metadata."""
        data = {
            "method": "depth_update",
            "params": {"market": "BTC_USDT", "bids": [["45000.00", "0.5"]], "asks": [["45001.00", "0.4"]]},
            "event_time": 1640995200000,
            "update_id": 12345,
        }

        response = DepthUpdateResponse(**data)

        assert response.method == "depth_update"
        assert response.params.market == "BTC_USDT"
        assert response.event_time == 1640995200000
        assert response.update_id == 12345

    def test_depth_update_response_without_metadata(self):
        """Test DepthUpdateResponse without event metadata (backward compatibility)."""
        data = {
            "method": "depth_update",
            "params": {"market": "BTC_USDT", "bids": [["45000.00", "0.5"]], "asks": [["45001.00", "0.4"]]},
        }

        response = DepthUpdateResponse(**data)

        assert response.method == "depth_update"
        assert response.params.market == "BTC_USDT"
        assert response.event_time is None
        assert response.update_id is None


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility of enhanced models."""

    def test_existing_websocket_responses_still_work(self):
        """Test that existing WebSocket responses without metadata still work."""
        # Test old-style response without metadata
        old_response_data = {"id": 123, "result": {"status": "ok"}, "error": None}

        response = WSResponse(**old_response_data)

        assert response.id == 123
        assert response.result["status"] == "ok"
        assert response.error is None
        # New fields should be None for backward compatibility
        assert response.event_time is None
        assert response.update_id is None

    def test_partial_metadata_support(self):
        """Test responses with only some metadata fields."""
        # Test response with only event_time
        data_with_event_time = {"id": 123, "result": {"status": "ok"}, "error": None, "event_time": 1640995200000}

        response = WSResponse(**data_with_event_time)

        assert response.id == 123
        assert response.event_time == 1640995200000
        assert response.update_id is None

        # Test response with only update_id
        data_with_update_id = {"id": 124, "result": {"status": "ok"}, "error": None, "update_id": 12345}

        response = WSResponse(**data_with_update_id)

        assert response.id == 124
        assert response.update_id == 12345
        assert response.event_time is None
