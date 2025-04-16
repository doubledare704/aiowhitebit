"""Validation utilities for the WhiteBit API."""

from decimal import Decimal

from aiowhitebit.exceptions import WhitebitValidationError


def validate_market(market: str) -> None:
    """Validate market parameter"""
    if not market or not isinstance(market, str):
        raise WhitebitValidationError("Market parameter must be a non-empty string")
    if "_" not in market:
        raise WhitebitValidationError("Market must be in format BASE_QUOTE (e.g. BTC_USDT)")


def validate_amount(amount: str) -> None:
    """Validate amount parameter"""
    try:
        value = Decimal(amount)
        if value <= 0:
            raise WhitebitValidationError("Amount must be greater than 0")
    except:
        raise WhitebitValidationError("Amount must be a valid decimal string")


def validate_price(price: str) -> None:
    """Validate price parameter"""
    try:
        value = Decimal(price)
        if value <= 0:
            raise WhitebitValidationError("Price must be greater than 0")
    except:
        raise WhitebitValidationError("Price must be a valid decimal string")


def validate_limit(limit: int, max_limit: int = 1000) -> None:
    """Validate limit parameter"""
    if not isinstance(limit, int) or limit <= 0 or limit > max_limit:
        raise WhitebitValidationError(f"Limit must be an integer between 1 and {max_limit}")
