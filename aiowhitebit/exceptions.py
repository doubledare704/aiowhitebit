"""Exceptions for the WhiteBit API."""

import logging
from dataclasses import dataclass
from typing import Any, Optional

from aiowhitebit.constants import KNOWN_ERRORS


@dataclass
class ErrorDetails:
    """Details about an API error.

    This class stores information about an error returned by the WhiteBit API,
    including the error code, message, and any additional data.
    """

    code: int
    message: str
    data: Optional[Any] = None


class WhitebitError(Exception):
    """Base exception for WhiteBit API."""

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        """Initialize the base exception.

        Args:
            message: Error message
            details: Optional error details
        """
        super().__init__(message)
        self.details = details


class WhitebitAPIError(WhitebitError):
    """API-specific errors."""

    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        """Initialize the API error.

        Args:
            code: Error code
            message: Error message
            data: Optional additional error data
        """
        details = ErrorDetails(code=code, message=message, data=data)
        super().__init__(f"API Error {code}: {message}", details)


class WhitebitValidationError(WhitebitError):
    """Validation errors."""

    def __init__(self, message: str):
        """Initialize the validation error.

        Args:
            message: Validation error message
        """
        super().__init__(f"Validation Error: {message}")


def handle_errors(resp: dict) -> None:
    """Handle API error responses."""
    if not isinstance(resp, dict):
        raise WhitebitValidationError("Invalid response format")

    if "code" in resp:
        code = resp["code"]
        message = KNOWN_ERRORS.get(code, resp.get("message") or "Unknown error")
        data = resp.get("data")

        logging.error(f"API Error: {message}", extra={"code": code, "data": data, "response": resp})

        raise WhitebitAPIError(code, message, data)
