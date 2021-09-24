__all__ = ["AioWhitebitPrivateClient"]

import base64
import hashlib
import hmac
import json
import time
from typing import Optional, Union, List, Callable

import aiohttp
from pydantic import BaseModel

from aiowhitebit.http_data_models import (
    TradingBalanceItem,
    TradingBalanceList,
    CreateLimitOrderRequest,
    CreateOrderResponse,
    CreateStockMarketOrderRequest,
    CreateStopLimitOrderRequest,
    CreateStopMarketOrderRequest,
    CancelOrderRequest,
    CancelOrderResponse,
    ActiveOrdersRequest,
    ExecutedOrderHistoryRequest,
    ExecutedOrdersResponse,
    ExecutedOrderDealsRequest,
    ExecutedDealsResponse,
    ExecutedOrdersByMarket,
    ExecutedOrdersByMarketResponse,
)
from .constants import BASE_URL, API_KEY, SECRET_KEY
from .converters import (
    convert_executed_deals_to_dto,
    convert_executed_orders_by_market_to_dto,
    convert_executed_orders_to_dto,
    convert_active_orders_to_dto,
    convert_cancel_order_to_dto,
    convert_order_response_to_dto,
    convert_get_trading_balance_to_dto,
)
from .exceptions import handle_errors


class AioWhitebitPrivateClient:
    def __init__(
        self,
        api_key: str = API_KEY,
        secret_key: str = SECRET_KEY,
        base_url: str = BASE_URL,
    ) -> None:
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.payload = None
        self.signature = None
        self.session = None

    def gen_nonce(self) -> str:
        return str(int(time.time()))

    def gen_request_payload(self, data_json: str) -> None:
        self.payload = base64.b64encode(data_json.encode("ascii"))

    @property
    def request_signature(self) -> str:
        return hmac.new(
            self.secret_key.encode("ascii"), self.payload, hashlib.sha512
        ).hexdigest()

    def request_url(self, path) -> str:
        return f"{self.base_url}{path}"

    @property
    def prepared_headers(self) -> dict:
        return {
            "Content-type": "application/json",
            "X-TXC-APIKEY": self.api_key,
            "X-TXC-PAYLOAD": str(
                self.payload, "UTF-8"
            ),  # aiohttp session doesnt accept bytes
            "X-TXC-SIGNATURE": self.request_signature,
        }

    async def get_trading_balance(
        self,
        ticker: Optional[str] = None,
    ) -> Union[TradingBalanceItem, TradingBalanceList]:
        request_path = "/api/v4/trade-account/balance"
        full_url = self.request_url(request_path)
        data = {"request": request_path, "nonce": self.gen_nonce()}
        if ticker:
            data.update(
                {"ticker": ticker}
            )  # for example for obtaining trading balance for BTC currency
        data_json = json.dumps(
            data, separators=(",", ":")
        )  # use separators param for deleting spaces
        self.gen_request_payload(data_json)

        async with aiohttp.ClientSession(headers=self.prepared_headers) as session:
            async with session.post(full_url, data=data_json) as r:
                json_body = await r.json()
                if r.status == 200:
                    return convert_get_trading_balance_to_dto(json_body, ticker)
                handle_errors(json_body)

    async def create_base_orders(
        self,
        path: str,
        data_model: BaseModel,
        converter: Callable,
    ) -> Union[
        CreateOrderResponse,
        CancelOrderResponse,
        List[CreateOrderResponse],
        ExecutedOrdersResponse,
        ExecutedDealsResponse,
        ExecutedOrdersByMarketResponse,
    ]:
        request_path = path
        full_url = self.request_url(request_path)
        data = data_model.dict(exclude_none=True)
        data.update({"request": request_path, "nonce": self.gen_nonce()})
        data_json = json.dumps(
            data, separators=(",", ":")
        )  # use separators param for deleting spaces
        self.gen_request_payload(data_json)

        async with aiohttp.ClientSession(headers=self.prepared_headers) as session:
            async with session.post(full_url, data=data_json) as r:
                json_body = await r.json()
                if r.status == 200:
                    return converter()
                handle_errors(json_body)

    async def create_limit_order(
        self,
        req: CreateLimitOrderRequest,
    ) -> CreateOrderResponse:
        request_path = "/api/v4/order/new"
        return await self.create_base_orders(
            request_path, req, convert_order_response_to_dto
        )

    async def create_stock_market_order(
        self,
        req: CreateStockMarketOrderRequest,
    ) -> CreateOrderResponse:
        request_path = "/api/v4/order/stock_market"
        return await self.create_base_orders(
            request_path, req, convert_order_response_to_dto
        )

    async def create_stop_limit_order(
        self,
        req: CreateStopLimitOrderRequest,
    ) -> CreateOrderResponse:
        request_path = "/api/v4/order/stop_limit"
        return await self.create_base_orders(
            request_path, req, convert_order_response_to_dto
        )

    async def create_stop_market_order(
        self,
        req: CreateStopMarketOrderRequest,
    ) -> CreateOrderResponse:
        request_path = "/api/v4/order/stop_market"
        return await self.create_base_orders(
            request_path, req, convert_order_response_to_dto
        )

    async def cancel_order(
        self,
        req: CancelOrderRequest,
    ) -> CancelOrderResponse:
        request_path = "/api/v4/order/cancel"
        return await self.create_base_orders(
            request_path, req, convert_cancel_order_to_dto
        )

    async def active_orders(
        self,
        req: ActiveOrdersRequest,
    ) -> List[CreateOrderResponse]:
        request_path = "/api/v4/orders"
        return await self.create_base_orders(
            request_path, req, convert_active_orders_to_dto
        )

    async def executed_order_history(
        self,
        req: ExecutedOrderHistoryRequest,
    ) -> ExecutedOrdersResponse:
        request_path = "/api/v4/trade-account/executed-history"
        return await self.create_base_orders(
            request_path, req, convert_executed_orders_to_dto
        )

    async def executed_order_deals(
        self,
        req: ExecutedOrderDealsRequest,
    ) -> ExecutedDealsResponse:
        request_path = "/api/v4/trade-account/order"
        return await self.create_base_orders(
            request_path, req, convert_executed_deals_to_dto
        )

    async def executed_orders_by_market(
        self,
        req: ExecutedOrdersByMarket,
    ) -> ExecutedOrdersByMarketResponse:
        request_path = "/api/v4/trade-account/order/history"
        return await self.create_base_orders(
            request_path, req, convert_executed_orders_by_market_to_dto
        )
