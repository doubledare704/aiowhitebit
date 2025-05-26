"""WhiteBit Private API v4 client."""

import base64
import hashlib
import hmac
import json
import time
from typing import Callable, Optional, Union

import aiohttp
from pydantic import BaseModel

from aiowhitebit.constants import API_KEY, BASE_URL, SECRET_KEY
from aiowhitebit.converters.private import (
    convert_active_orders_to_dto,
    convert_cancel_order_to_dto,
    convert_executed_deals_to_dto,
    convert_executed_orders_by_market_to_dto,
    convert_executed_orders_to_dto,
    convert_get_trading_balance_to_dto,
    convert_order_response_to_dto,
)
from aiowhitebit.exceptions import WhitebitAPIError, handle_errors
from aiowhitebit.models.private import (
    ActiveOrdersRequest,
    CancelOrderRequest,
    CancelOrderResponse,
    CreateLimitOrderRequest,
    CreateOrderResponse,
    CreateStockMarketOrderRequest,
    CreateStopLimitOrderRequest,
    CreateStopMarketOrderRequest,
    ExecutedDealsResponse,
    ExecutedOrderDealsRequest,
    ExecutedOrderHistoryRequest,
    ExecutedOrdersByMarket,
    ExecutedOrdersByMarketResponse,
    ExecutedOrdersResponse,
    TradingBalanceItem,
    TradingBalanceList,
)


class PrivateV4Client:
    """WhiteBit Private API v4 client.

    This client provides methods to interact with the WhiteBit Private API v4.
    All endpoints require authentication with API key and secret key.

    Rate limit: 60 requests/minute for all endpoints.
    """

    def __init__(
        self,
        api_key: str = API_KEY or "",  # Default to empty string if None
        secret_key: str = SECRET_KEY or "",  # Default to empty string if None
        base_url: str = BASE_URL,
    ) -> None:
        """Initialize the WhiteBit Private API v4 client.

        Args:
            api_key: API key for authentication
            secret_key: Secret key for authentication
            base_url: Base URL for the WhiteBit API. Defaults to the official WhiteBit API URL.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.payload: Optional[bytes] = None
        self.signature: Optional[str] = None
        self.session = None

    def gen_nonce(self) -> str:
        """Generate a nonce for the request.

        Returns:
            Current timestamp as string
        """
        return str(int(time.time()))

    def gen_request_payload(self, data_json: str) -> None:
        """Generate the request payload.

        Args:
            data_json: JSON data to encode
        """
        self.payload = base64.b64encode(data_json.encode("ascii"))

    @property
    def request_signature(self) -> str:
        """Generate the request signature.

        Returns:
            HMAC-SHA512 signature of the payload
        """
        return hmac.new(self.secret_key.encode("ascii"), self.payload, hashlib.sha512).hexdigest()

    def request_url(self, path: str) -> str:
        """Construct the full URL for an API endpoint.

        Args:
            path: API endpoint path

        Returns:
            Full URL for the API endpoint
        """
        return f"{self.base_url}{path}"

    @property
    def prepared_headers(self) -> dict:
        """Prepare the headers for the request.

        Returns:
            Headers for the request
        """
        if self.payload is None:
            raise ValueError("Payload must be generated before preparing headers")

        return {
            "Content-type": "application/json",
            "X-TXC-APIKEY": self.api_key,
            "X-TXC-PAYLOAD": str(self.payload, "UTF-8"),  # aiohttp session doesnt accept bytes
            "X-TXC-SIGNATURE": self.request_signature,
        }

    async def get_trading_balance(
        self,
        ticker: Optional[str] = None,
    ) -> Union[TradingBalanceItem, TradingBalanceList]:
        """Get trading balance for all or a specific currency.

        Args:
            ticker: Ticker of the currency (optional). If provided, returns balance for this currency only.

        Returns:
            TradingBalanceItem if ticker is provided, TradingBalanceList otherwise

        Raises:
            WhitebitAPIError: If the API returns an error
        """
        request_path = "/api/v4/trade-account/balance"
        full_url = self.request_url(request_path)
        data = {"request": request_path, "nonce": self.gen_nonce()}
        if ticker:
            data.update({"ticker": ticker})  # for example for obtaining trading balance for BTC currency
        data_json = json.dumps(data, separators=(",", ":"))  # use separators param for deleting spaces
        self.gen_request_payload(data_json)

        async with aiohttp.ClientSession(headers=self.prepared_headers) as session:
            async with session.post(full_url, data=data_json) as r:
                json_body = await r.json()
                if r.status == 200:
                    return convert_get_trading_balance_to_dto(json_body, ticker)
                handle_errors(json_body)
                # This line is unreachable as handle_errors should raise an exception
                # Adding it to satisfy type checker
                raise WhitebitAPIError(r.status, str(json_body))

    async def create_base_orders(
        self,
        path: str,
        data_model: BaseModel,
        converter: Callable,
    ) -> Union[
        CreateOrderResponse,
        CancelOrderResponse,
        list[CreateOrderResponse],
        ExecutedOrdersResponse,
        ExecutedDealsResponse,
        ExecutedOrdersByMarketResponse,
    ]:
        """Base method for creating orders.

        Args:
            path: API endpoint path
            data_model: Request data model
            converter: Converter function for the response

        Returns:
            Response from the API

        Raises:
            WhitebitAPIError: If the API returns an error
        """
        request_path = path
        full_url = self.request_url(request_path)
        data = data_model.model_dump(exclude_none=True)
        data.update({"request": request_path, "nonce": self.gen_nonce()})
        data_json = json.dumps(data, separators=(",", ":"))  # use separators param for deleting spaces
        self.gen_request_payload(data_json)

        async with aiohttp.ClientSession(headers=self.prepared_headers) as session:
            async with session.post(full_url, data=data_json) as r:
                json_body = await r.json()
                if r.status == 200:
                    return converter(json_body)
                handle_errors(json_body)
                # This line is unreachable as handle_errors should raise an exception
                # Adding it to satisfy type checker
                raise WhitebitAPIError(r.status, str(json_body))

    async def create_limit_order(
        self,
        req: CreateLimitOrderRequest,
    ) -> CreateOrderResponse:
        """Create a limit order.

        Args:
            req: Limit order request

        Returns:
            CreateOrderResponse: Information about the created order

        Example:
            ```python
            client = PrivateV4Client()
            order = await client.create_limit_order(
                CreateLimitOrderRequest(
                    market="BTC_USDT",
                    side="buy",
                    amount="0.01",
                    price="9800",
                )
            )
            ```
        """
        request_path = "/api/v4/order/new"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_order_response_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, CreateOrderResponse):
            raise TypeError(f"Expected CreateOrderResponse, got {type(result).__name__}")
        return result

    async def create_stock_market_order(
        self,
        req: CreateStockMarketOrderRequest,
    ) -> CreateOrderResponse:
        """Create a stock market order.

        Args:
            req: Stock market order request

        Returns:
            CreateOrderResponse: Information about the created order

        Example:
            ```python
            client = PrivateV4Client()
            order = await client.create_stock_market_order(
                CreateStockMarketOrderRequest(
                    market="BTC_USDT",
                    side="buy",
                    amount="0.01",
                )
            )
            ```
        """
        request_path = "/api/v4/order/stock_market"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_order_response_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, CreateOrderResponse):
            raise TypeError(f"Expected CreateOrderResponse, got {type(result).__name__}")
        return result

    async def create_stop_limit_order(
        self,
        req: CreateStopLimitOrderRequest,
    ) -> CreateOrderResponse:
        """Create a stop limit order.

        Args:
            req: Stop limit order request

        Returns:
            CreateOrderResponse: Information about the created order

        Example:
            ```python
            client = PrivateV4Client()
            order = await client.create_stop_limit_order(
                CreateStopLimitOrderRequest(
                    market="BTC_USDT",
                    side="buy",
                    amount="0.01",
                    price="9800",
                    activation_price="9900",
                )
            )
            ```
        """
        request_path = "/api/v4/order/stop_limit"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_order_response_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, CreateOrderResponse):
            raise TypeError(f"Expected CreateOrderResponse, got {type(result).__name__}")
        return result

    async def create_stop_market_order(
        self,
        req: CreateStopMarketOrderRequest,
    ) -> CreateOrderResponse:
        """Create a stop market order.

        Args:
            req: Stop market order request

        Returns:
            CreateOrderResponse: Information about the created order

        Example:
            ```python
            client = PrivateV4Client()
            order = await client.create_stop_market_order(
                CreateStopMarketOrderRequest(
                    market="BTC_USDT",
                    side="buy",
                    amount="0.01",
                    activation_price="9900",
                )
            )
            ```
        """
        request_path = "/api/v4/order/stop_market"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_order_response_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, CreateOrderResponse):
            raise TypeError(f"Expected CreateOrderResponse, got {type(result).__name__}")
        return result

    async def cancel_order(
        self,
        req: CancelOrderRequest,
    ) -> CancelOrderResponse:
        """Cancel an order.

        Args:
            req: Cancel order request

        Returns:
            CancelOrderResponse: Information about the canceled order

        Example:
            ```python
            client = PrivateV4Client()
            order = await client.cancel_order(
                CancelOrderRequest(
                    market="BTC_USDT",
                    orderId=123456,
                )
            )
            ```
        """
        request_path = "/api/v4/order/cancel"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_cancel_order_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, CancelOrderResponse):
            raise TypeError(f"Expected CancelOrderResponse, got {type(result).__name__}")
        return result

    async def active_orders(
        self,
        req: ActiveOrdersRequest,
    ) -> list[CreateOrderResponse]:
        """Get active orders.

        Args:
            req: Active orders request

        Returns:
            List[CreateOrderResponse]: List of active orders

        Example:
            ```python
            client = PrivateV4Client()
            orders = await client.active_orders(
                ActiveOrdersRequest(
                    market="BTC_USDT",
                    limit=10,
                    offset=0,
                )
            )
            ```
        """
        request_path = "/api/v4/orders"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_active_orders_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, list) or (result and not isinstance(result[0], CreateOrderResponse)):
            raise TypeError(f"Expected list[CreateOrderResponse], got {type(result).__name__}")
        return result

    async def executed_order_history(
        self,
        req: ExecutedOrderHistoryRequest,
    ) -> ExecutedOrdersResponse:
        """Get executed order history.

        Args:
            req: Executed order history request

        Returns:
            ExecutedOrdersResponse: Executed order history

        Example:
            ```python
            client = PrivateV4Client()
            history = await client.executed_order_history(
                ExecutedOrderHistoryRequest(
                    market="BTC_USDT",
                    limit=10,
                    offset=0,
                )
            )
            ```
        """
        request_path = "/api/v4/trade-account/executed-history"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_executed_orders_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, ExecutedOrdersResponse):
            raise TypeError(f"Expected ExecutedOrdersResponse, got {type(result).__name__}")
        return result

    async def executed_order_deals(
        self,
        req: ExecutedOrderDealsRequest,
    ) -> ExecutedDealsResponse:
        """Get executed order deals.

        Args:
            req: Executed order deals request

        Returns:
            ExecutedDealsResponse: Executed order deals

        Example:
            ```python
            client = PrivateV4Client()
            deals = await client.executed_order_deals(
                ExecutedOrderDealsRequest(
                    orderId=123456,
                    limit=10,
                    offset=0,
                )
            )
            ```
        """
        request_path = "/api/v4/trade-account/order"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_executed_deals_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, ExecutedDealsResponse):
            raise TypeError(f"Expected ExecutedDealsResponse, got {type(result).__name__}")
        return result

    async def executed_orders_by_market(
        self,
        req: ExecutedOrdersByMarket,
    ) -> ExecutedOrdersByMarketResponse:
        """Get executed orders by market.

        Args:
            req: Executed orders by market request

        Returns:
            ExecutedOrdersByMarketResponse: Executed orders by market

        Example:
            ```python
            client = PrivateV4Client()
            orders = await client.executed_orders_by_market(
                ExecutedOrdersByMarket(
                    market="BTC_USDT",
                    limit=10,
                    offset=0,
                )
            )
            ```
        """
        request_path = "/api/v4/trade-account/order/history"
        result = await self.create_base_orders(
            request_path, req, lambda json_body: convert_executed_orders_by_market_to_dto(json_body)
        )
        # Type narrowing for type checkers
        if not isinstance(result, ExecutedOrdersByMarketResponse):
            raise TypeError(f"Expected ExecutedOrdersByMarketResponse, got {type(result).__name__}")
        return result
