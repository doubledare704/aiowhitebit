"""Webhook client for WhiteBIT API."""

__all__ = [
    "WebhookDataLoader",
    "get_webhook_data_loader",
]

import base64
import hashlib
import hmac
import json
import logging
from typing import Any, Callable, Dict, Optional

from multidict import CIMultiDictProxy

from aiowhitebit.constants import WEBHOOK_KEY, WEBHOOK_SECRET_KEY
from aiowhitebit.models.webhook import CodeApplyParams, TransactionParams, WebhookRequest


class WebhookDataLoader:
    """WhiteBIT Webhook data loader.

    This class provides methods to validate webhook requests and handle different webhook methods.
    """

    def __init__(self, webhook_key: str = WEBHOOK_KEY, webhook_secret_key: str = WEBHOOK_SECRET_KEY) -> None:
        """Initialize the webhook data loader.

        Args:
            webhook_key: Webhook API key
            webhook_secret_key: Webhook secret key
        """
        self._webhook_key = webhook_key
        self._webhook_secret_key = webhook_secret_key
        self.header_keys = [
            "X-TXC-APIKEY",
            "X-TXC-PAYLOAD",
            "X-TXC-SIGNATURE",
        ]
        self.current_request: Optional[WebhookRequest] = None
        self._handlers: Dict[str, Callable[[WebhookRequest], Any]] = {}

        # Register default handlers
        self.register_handler("code.apply", self._handle_code_apply)
        self.register_handler("deposit.accepted", self._handle_deposit_accepted)
        self.register_handler("deposit.updated", self._handle_deposit_updated)
        self.register_handler("deposit.processed", self._handle_deposit_processed)
        self.register_handler("deposit.canceled", self._handle_deposit_canceled)
        self.register_handler("withdraw.unconfirmed", self._handle_withdraw_unconfirmed)
        self.register_handler("withdraw.pending", self._handle_withdraw_pending)
        self.register_handler("withdraw.canceled", self._handle_withdraw_canceled)
        self.register_handler("withdraw.successful", self._handle_withdraw_successful)

    def register_handler(self, method: str, handler: Callable[[WebhookRequest], Any]) -> None:
        """Register a handler for a webhook method.

        Args:
            method: Webhook method name
            handler: Handler function that takes a WebhookRequest and returns any value
        """
        self._handlers[method] = handler

    def validate_headers(self, headers: CIMultiDictProxy) -> bool:
        """Validate webhook request headers.

        Args:
            headers: Request headers

        Returns:
            True if headers are valid, False otherwise
        """
        # Check if all required headers are present
        if not all(name in headers for name in self.header_keys):
            logging.warning(f"Missing required headers. Expected: {self.header_keys}, Got: {headers.keys()}")
            return False

        # Check if API key matches
        if headers["X-TXC-APIKEY"] != self._webhook_key:
            logging.warning(f"Invalid API key. Expected: {self._webhook_key}, Got: {headers['X-TXC-APIKEY']}")
            return False

        # Decode payload
        try:
            payload = base64.b64decode(headers["X-TXC-PAYLOAD"]).decode("ascii")
            json_payload: dict = json.loads(payload)
        except Exception as e:
            logging.error(f"Failed to decode payload: {e}")
            return False

        # Check if payload has required keys
        request_keys = ["id", "params", "method"]
        if not all(key in json_payload for key in request_keys):
            logging.warning(f"Missing required keys in payload. Expected: {request_keys}, Got: {json_payload.keys()}")
            return False

        # Verify signature
        try:
            temp_hash = hmac.new(
                self._webhook_secret_key.encode("ascii"),
                headers["X-TXC-PAYLOAD"].encode("ascii")
                if isinstance(headers["X-TXC-PAYLOAD"], str)
                else headers["X-TXC-PAYLOAD"],
                hashlib.sha512,
            ).hexdigest()
            return hmac.compare_digest(temp_hash, headers["X-TXC-SIGNATURE"])
        except Exception as e:
            logging.error(f"Failed to verify signature: {e}")
            return False

    def handle_request(self, req: WebhookRequest) -> Any:
        """Handle a webhook request.

        Args:
            req: Webhook request

        Returns:
            Result of the handler function

        Raises:
            ValueError: If no handler is registered for the webhook method
        """
        self.current_request = req

        if req.method not in self._handlers:
            raise ValueError(f"No handler registered for method: {req.method}")

        return self._handlers[req.method](req)

    # Default handlers for webhook methods
    def _handle_code_apply(self, req: WebhookRequest) -> None:
        """Handle code.apply webhook method.

        Args:
            req: Webhook request with CodeApplyParams
        """
        params = req.params
        if isinstance(params, CodeApplyParams):
            logging.info(f"Code applied: {params.code}")
        else:
            logging.warning(f"Invalid params type for code.apply: {type(params)}")

    def _handle_deposit_accepted(self, req: WebhookRequest) -> None:
        """Handle deposit.accepted webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Deposit accepted: {params.amount} {params.ticker} to {params.address}")
        else:
            logging.warning(f"Invalid params type for deposit.accepted: {type(params)}")

    def _handle_deposit_updated(self, req: WebhookRequest) -> None:
        """Handle deposit.updated webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Deposit updated: {params.amount} {params.ticker} to {params.address}")
        else:
            logging.warning(f"Invalid params type for deposit.updated: {type(params)}")

    def _handle_deposit_processed(self, req: WebhookRequest) -> None:
        """Handle deposit.processed webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Deposit processed: {params.amount} {params.ticker} to {params.address}")
        else:
            logging.warning(f"Invalid params type for deposit.processed: {type(params)}")

    def _handle_deposit_canceled(self, req: WebhookRequest) -> None:
        """Handle deposit.canceled webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Deposit canceled: {params.amount} {params.ticker} to {params.address}")
        else:
            logging.warning(f"Invalid params type for deposit.canceled: {type(params)}")

    def _handle_withdraw_unconfirmed(self, req: WebhookRequest) -> None:
        """Handle withdraw.unconfirmed webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Withdraw unconfirmed: {params.amount} {params.ticker} from {params.address}")
        else:
            logging.warning(f"Invalid params type for withdraw.unconfirmed: {type(params)}")

    def _handle_withdraw_pending(self, req: WebhookRequest) -> None:
        """Handle withdraw.pending webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Withdraw pending: {params.amount} {params.ticker} from {params.address}")
        else:
            logging.warning(f"Invalid params type for withdraw.pending: {type(params)}")

    def _handle_withdraw_canceled(self, req: WebhookRequest) -> None:
        """Handle withdraw.canceled webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Withdraw canceled: {params.amount} {params.ticker} from {params.address}")
        else:
            logging.warning(f"Invalid params type for withdraw.canceled: {type(params)}")

    def _handle_withdraw_successful(self, req: WebhookRequest) -> None:
        """Handle withdraw.successful webhook method.

        Args:
            req: Webhook request with TransactionParams
        """
        params = req.params
        if isinstance(params, TransactionParams):
            logging.info(f"Withdraw successful: {params.amount} {params.ticker} from {params.address}")
        else:
            logging.warning(f"Invalid params type for withdraw.successful: {type(params)}")


def get_webhook_data_loader(
    webhook_key: str = WEBHOOK_KEY, webhook_secret_key: str = WEBHOOK_SECRET_KEY
) -> WebhookDataLoader:
    """Get a webhook data loader instance.

    Args:
        webhook_key: Webhook API key
        webhook_secret_key: Webhook secret key

    Returns:
        WebhookDataLoader instance
    """
    return WebhookDataLoader(webhook_key, webhook_secret_key)
