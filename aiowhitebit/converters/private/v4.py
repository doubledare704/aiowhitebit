"""Converters for the WhiteBit Private API v4."""

from typing import Optional, Union

from aiowhitebit.models.private.response import (
    CancelOrderResponse,
    CreateOrderResponse,
    ExecutedDealsResponse,
    ExecutedOrdersByMarketResponse,
    ExecutedOrdersResponse,
    TradingBalanceItem,
    TradingBalanceList,
)


def convert_executed_deals_to_dto(json_body: dict) -> ExecutedDealsResponse:
    """Convert executed deals JSON response to ExecutedDealsResponse object.

    Args:
        json_body: JSON response from the API

    Returns:
        ExecutedDealsResponse object
    """
    return ExecutedDealsResponse(result=json_body)


def convert_executed_orders_by_market_to_dto(json_body: dict) -> ExecutedOrdersByMarketResponse:
    """Convert executed orders by market JSON response to ExecutedOrdersByMarketResponse object.

    Args:
        json_body: JSON response from the API

    Returns:
        ExecutedOrdersByMarketResponse object
    """
    return ExecutedOrdersByMarketResponse(result=json_body)


def convert_executed_orders_to_dto(json_body: dict) -> ExecutedOrdersResponse:
    """Convert executed orders JSON response to ExecutedOrdersResponse object.

    Args:
        json_body: JSON response from the API

    Returns:
        ExecutedOrdersResponse object
    """
    return ExecutedOrdersResponse(result=json_body)


def convert_active_orders_to_dto(json_list: list) -> list[CreateOrderResponse]:
    """Convert active orders JSON response to a list of CreateOrderResponse objects.

    Args:
        json_list: JSON response from the API

    Returns:
        List of CreateOrderResponse objects
    """
    return [CreateOrderResponse(**js_obj) for js_obj in json_list]


def convert_cancel_order_to_dto(json_body: dict) -> CancelOrderResponse:
    """Convert cancel order JSON response to CancelOrderResponse object.

    Args:
        json_body: JSON response from the API

    Returns:
        CancelOrderResponse object
    """
    return CancelOrderResponse(**json_body)


def convert_order_response_to_dto(json_body: dict) -> CreateOrderResponse:
    """Convert order response JSON response to CreateOrderResponse object.

    Args:
        json_body: JSON response from the API

    Returns:
        CreateOrderResponse object
    """
    return CreateOrderResponse(**json_body)


def convert_get_trading_balance_to_dto(
    json_obj: dict, ticker: Optional[str] = None
) -> Union[TradingBalanceItem, TradingBalanceList]:
    """Convert trading balance JSON response to TradingBalanceItem or TradingBalanceList object.

    Args:
        json_obj: JSON response from the API
        ticker: Ticker of the currency (optional)

    Returns:
        TradingBalanceItem or TradingBalanceList object
    """
    if ticker:
        r = TradingBalanceItem(**json_obj)
        r.ticker = ticker
        return r
    return TradingBalanceList(
        result=[TradingBalanceItem(ticker=k, available=v["available"], freeze=v["freeze"]) for k, v in json_obj.items()]
    )
