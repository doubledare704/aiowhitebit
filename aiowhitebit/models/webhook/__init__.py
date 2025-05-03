"""Webhook models for WhiteBit API.

This package contains Pydantic models for parsing and validating webhook payloads
received from the WhiteBit API, including transaction notifications and code applications.
"""

from .payload import CodeApplyParams, ConfirmationsInfo, TransactionParams, WebhookParams, WebhookRequest

__all__ = [
    "CodeApplyParams",
    "ConfirmationsInfo",
    "TransactionParams",
    "WebhookParams",
    "WebhookRequest",
]
