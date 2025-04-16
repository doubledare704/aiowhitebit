"""Exceptions for the WhiteBit API."""
import logging
from typing import Optional, Any
from dataclasses import dataclass

from aiowhitebit.constants import KNOWN_ERRORS


@dataclass
class ErrorDetails:
    code: int
    message: str
    data: Optional[Any] = None

class WhitebitException(Exception):
    """Base exception for WhiteBit API"""
    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(message)
        self.details = details

class WhitebitAPIError(WhitebitException):
    """API-specific errors"""
    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        details = ErrorDetails(code=code, message=message, data=data)
        super().__init__(f"API Error {code}: {message}", details)

class WhitebitValidationError(WhitebitException):
    """Validation errors"""
    def __init__(self, message: str):
        super().__init__(f"Validation Error: {message}")

def handle_errors(resp: dict) -> None:
    """Handle API error responses"""
    if not isinstance(resp, dict):
        raise WhitebitValidationError("Invalid response format")
    
    if "code" in resp:
        code = resp["code"]
        message = KNOWN_ERRORS.get(code, resp.get("message", "Unknown error"))
        data = resp.get("data")
        
        logging.error(f"API Error: {message}", extra={
            "code": code,
            "data": data,
            "response": resp
        })
        
        raise WhitebitAPIError(code, message, data)
