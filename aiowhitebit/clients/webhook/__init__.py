"""Webhook client for WhiteBit API.

This package provides functionality for handling and validating webhook requests from WhiteBit,
including signature verification and processing of different webhook event types.
"""

from .webhook_client import WebhookDataLoader, get_webhook_data_loader

__all__ = [
    "WebhookDataLoader",
    "get_webhook_data_loader",
]
