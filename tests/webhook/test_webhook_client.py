import base64
import hashlib
import hmac
import json
from unittest.mock import MagicMock, patch

import pytest
from multidict import CIMultiDict, CIMultiDictProxy

from aiowhitebit.clients.webhook import WebhookDataLoader
from aiowhitebit.models.webhook import WebhookRequest


class TestWebhookDataLoader:
    @pytest.fixture
    def webhook_key(self):
        return "test_webhook_key"

    @pytest.fixture
    def webhook_secret_key(self):
        return "test_webhook_secret_key"

    @pytest.fixture
    def webhook_loader(self, webhook_key, webhook_secret_key):
        return WebhookDataLoader(webhook_key=webhook_key, webhook_secret_key=webhook_secret_key)

    @pytest.fixture
    def valid_payload_dict(self):
        return {
            "id": 123,
            "method": "deposit.accepted",
            "params": {
                "ticker": "BTC",
                "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "amount": "0.1",
                "transactionHash": "0x123456789abcdef",
                "fee": "0.0001",
                "confirmations": 3,
            },
        }

    @pytest.fixture
    def valid_payload(self, valid_payload_dict):
        return base64.b64encode(json.dumps(valid_payload_dict).encode("ascii"))

    @pytest.fixture
    def valid_signature(self, webhook_secret_key, valid_payload):
        return hmac.new(webhook_secret_key.encode("ascii"), valid_payload, hashlib.sha512).hexdigest()

    @pytest.fixture
    def valid_headers(self, webhook_key, valid_payload, valid_signature):
        headers = {
            "X-TXC-APIKEY": webhook_key,
            "X-TXC-PAYLOAD": valid_payload,
            "X-TXC-SIGNATURE": valid_signature,
        }
        # Create a CIMultiDict first, then wrap it in CIMultiDictProxy
        multi_dict = CIMultiDict(headers)
        return CIMultiDictProxy(multi_dict)

    def test_init(self, webhook_loader, webhook_key, webhook_secret_key):
        assert webhook_loader._webhook_key == webhook_key
        assert webhook_loader._webhook_secret_key == webhook_secret_key
        assert webhook_loader.header_keys == ["X-TXC-APIKEY", "X-TXC-PAYLOAD", "X-TXC-SIGNATURE"]
        assert webhook_loader.current_request is None
        assert len(webhook_loader._handlers) == 9  # Check that default handlers are registered

    def test_register_handler(self, webhook_loader):
        # Define a test handler
        def test_handler(req):
            return "test_result"

        # Register the handler
        webhook_loader.register_handler("test.method", test_handler)

        # Verify the handler was registered
        assert "test.method" in webhook_loader._handlers
        assert webhook_loader._handlers["test.method"] == test_handler

    def test_validate_headers_success(self, webhook_loader, valid_headers):
        # Test successful validation
        assert webhook_loader.validate_headers(valid_headers) is True

    def test_validate_headers_missing_headers(self, webhook_loader):
        # Create headers with missing keys
        multi_dict = CIMultiDict({"X-TXC-APIKEY": "value"})
        headers = CIMultiDictProxy(multi_dict)

        # Test validation with missing headers
        assert webhook_loader.validate_headers(headers) is False

    def test_validate_headers_invalid_api_key(self, webhook_loader, valid_headers):
        # Create headers with invalid API key
        multi_dict = CIMultiDict(dict(valid_headers))
        multi_dict["X-TXC-APIKEY"] = "invalid_key"
        headers = CIMultiDictProxy(multi_dict)

        # Test validation with invalid API key
        assert webhook_loader.validate_headers(headers) is False

    def test_validate_headers_invalid_payload(self, webhook_loader, valid_headers):
        # Create headers with invalid payload (not base64 encoded)
        multi_dict = CIMultiDict(dict(valid_headers))
        multi_dict["X-TXC-PAYLOAD"] = "not_base64_encoded"
        headers = CIMultiDictProxy(multi_dict)

        # Test validation with invalid payload
        assert webhook_loader.validate_headers(headers) is False

    def test_validate_headers_missing_payload_keys(self, webhook_loader, webhook_key, webhook_secret_key):
        # Create payload missing required keys
        payload_dict = {"id": "123"}  # Missing method and params
        payload = base64.b64encode(json.dumps(payload_dict).encode("ascii"))
        signature = hmac.new(webhook_secret_key.encode("ascii"), payload, hashlib.sha512).hexdigest()

        headers = {
            "X-TXC-APIKEY": webhook_key,
            "X-TXC-PAYLOAD": payload,
            "X-TXC-SIGNATURE": signature,
        }
        multi_dict = CIMultiDict(headers)
        headers = CIMultiDictProxy(multi_dict)

        # Test validation with missing payload keys
        assert webhook_loader.validate_headers(headers) is False

    def test_validate_headers_invalid_signature(self, webhook_loader, valid_headers):
        # Create headers with invalid signature
        multi_dict = CIMultiDict(dict(valid_headers))
        multi_dict["X-TXC-SIGNATURE"] = "invalid_signature"
        headers = CIMultiDictProxy(multi_dict)

        # Test validation with invalid signature
        assert webhook_loader.validate_headers(headers) is False

    def test_handle_request(self, webhook_loader):
        # Create a test request
        req = WebhookRequest(
            id="123",
            method="deposit.accepted",
            params={
                "ticker": "BTC",
                "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "amount": "0.1",
                "transactionHash": "0x123456789abcdef",
                "fee": "0.0001",
                "confirmations": {"count": 3, "actual": 3, "required": 2},
                "createdAt": 1672531200,  # Unix timestamp for 2023-01-01T00:00:00Z
                "currency": "BTC",
            },
        )

        # Mock the handler
        webhook_loader._handlers["deposit.accepted"] = MagicMock(return_value="test_result")

        # Test handling the request
        result = webhook_loader.handle_request(req)

        # Verify the handler was called with the request
        webhook_loader._handlers["deposit.accepted"].assert_called_once_with(req)
        assert result == "test_result"
        assert webhook_loader.current_request == req

    def test_handle_request_no_handler(self, webhook_loader):
        # Create a test request with a method that has no handler
        req = WebhookRequest(id="123", method="unknown.method", params={})

        # Test handling the request with no handler
        with pytest.raises(ValueError, match="No handler registered for method: unknown.method"):
            webhook_loader.handle_request(req)

    @patch("logging.info")
    def test_handle_code_apply(self, mock_logging, webhook_loader):
        # Create a test request
        req = WebhookRequest(id="123", method="code.apply", params={"code": "TEST123", "user_id": 456})

        # Test handling the request
        webhook_loader._handle_code_apply(req)

        # Verify logging was called
        mock_logging.assert_called_once_with("Code applied: TEST123")

    @patch("logging.warning")
    def test_handle_code_apply_invalid_params(self, mock_logging, webhook_loader):
        # For this test, we need to create a WebhookRequest with a method of code.apply
        # but with params that will fail validation when passed to CodeApplyParams

        # Create a mock request object directly to bypass validation
        req = MagicMock(spec=WebhookRequest)
        req.id = "123"
        req.method = "code.apply"
        req.params = {"invalid_param": "value"}  # Missing required fields

        # Test handling the request with invalid params
        webhook_loader._handle_code_apply(req)

        # Verify warning was logged
        mock_logging.assert_called_once()
        assert "Invalid params type for code.apply" in mock_logging.call_args[0][0]

    @patch("logging.info")
    def test_handle_deposit_accepted(self, mock_logging, webhook_loader):
        # Create a test request
        req = WebhookRequest(
            id="123",
            method="deposit.accepted",
            params={
                "ticker": "BTC",
                "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "amount": "0.1",
                "transactionHash": "0x123456789abcdef",
                "fee": "0.0001",
                "confirmations": {"count": 3, "actual": 3, "required": 2},
                "createdAt": 1672531200,  # Unix timestamp for 2023-01-01T00:00:00Z
                "currency": "BTC",
            },
        )

        # Test handling the request
        webhook_loader._handle_deposit_accepted(req)

        # Verify logging was called
        mock_logging.assert_called_once_with("Deposit accepted: 0.1 BTC to bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")

    # Test other transaction handlers
    @patch("logging.info")
    def test_handle_deposit_updated(self, mock_logging, webhook_loader):
        req = WebhookRequest(
            id="123",
            method="deposit.updated",
            params={
                "ticker": "BTC",
                "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "amount": "0.1",
                "transactionHash": "0x123456789abcdef",
                "fee": "0.0001",
                "confirmations": {"count": 3, "actual": 3, "required": 2},
                "createdAt": 1672531200,  # Unix timestamp for 2023-01-01T00:00:00Z
                "currency": "BTC",
            },
        )
        webhook_loader._handle_deposit_updated(req)
        mock_logging.assert_called_once_with("Deposit updated: 0.1 BTC to bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")

    @patch("logging.info")
    def test_handle_withdraw_unconfirmed(self, mock_logging, webhook_loader):
        req = WebhookRequest(
            id="123",
            method="withdraw.unconfirmed",
            params={
                "ticker": "BTC",
                "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "amount": "0.1",
                "transactionHash": "0x123456789abcdef",
                "fee": "0.0001",
                "confirmations": {"count": 3, "actual": 3, "required": 2},
                "createdAt": 1672531200,  # Unix timestamp for 2023-01-01T00:00:00Z
                "currency": "BTC",
            },
        )
        webhook_loader._handle_withdraw_unconfirmed(req)
        mock_logging.assert_called_once_with(
            "Withdraw unconfirmed: 0.1 BTC from bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
        )
