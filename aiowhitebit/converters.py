from typing import List, Union, Optional

from aiowhitebit.http_data_models import (
    ExecutedDealsResponse,
    ExecutedOrdersByMarketResponse,
    ExecutedOrdersResponse,
    CreateOrderResponse,
    CancelOrderResponse,
    TradingBalanceItem,
    TradingBalanceList,
)


def convert_executed_deals_to_dto(
    json_body: dict,
) -> ExecutedDealsResponse:
    return ExecutedDealsResponse(result=json_body)


def convert_executed_orders_by_market_to_dto(
    json_body: dict,
) -> ExecutedOrdersByMarketResponse:
    return ExecutedOrdersByMarketResponse(result=json_body)


def convert_executed_orders_to_dto(
    json_body: dict,
) -> ExecutedOrdersResponse:
    return ExecutedOrdersResponse(result=json_body)


def convert_active_orders_to_dto(
    json_list: list,
) -> List[CreateOrderResponse]:
    return [CreateOrderResponse(**js_obj) for js_obj in json_list]


def convert_cancel_order_to_dto(
    json_body: dict,
) -> CancelOrderResponse:
    return CancelOrderResponse(**json_body)


def convert_order_response_to_dto(
    json_body: dict,
) -> CreateOrderResponse:
    return CreateOrderResponse(**json_body)


def convert_get_trading_balance_to_dto(
    json_obj: dict,
    ticker: Optional[str] = None,
) -> Union[TradingBalanceItem, TradingBalanceList]:
    if ticker:
        r = TradingBalanceItem(**json_obj)
        r.ticker = ticker
        return r
    return TradingBalanceList(
        result=[
            TradingBalanceItem(ticker=k, available=v["available"], freeze=v["freeze"])
            for k, v in json_obj.items()
        ]
    )
