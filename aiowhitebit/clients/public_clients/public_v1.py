__all__ = ["AioWhitebitPublicV1Client"]

from typing import Dict

import aiohttp

from aiowhitebit.clients.public_clients.converters import (
    convert_tickers_to_object,
    convert_kline_to_object,
    convert_order_depth_to_object
)
from aiowhitebit.constants import BASE_URL
from aiowhitebit.http_data_models.response_models import (
    MarketInfoV1,
    TickersV1,
    MarketSingleResponse,
    KlineV1,
    SymbolsV1,
    OrderDepthV1, TradeHistoryV1
)


async def base_get_request(url) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return await r.json()


class AioWhitebitPublicV1Client:
    def __init__(
            self,
            base_url: str = BASE_URL,
    ) -> None:
        self.base_url = base_url
        self.payload = None
        self.signature = None
        self.session = None

    def request_url(self, path) -> str:
        return f"{self.base_url}{path}"

    async def get_market_info(self) -> MarketInfoV1:
        request_path = "/api/v1/public/markets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MarketInfoV1(**json_obj)

    async def get_tickers(self) -> TickersV1:
        request_path = "/api/v1/public/tickers"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_tickers_to_object(json_obj)

    async def get_single_market(self, market: str) -> MarketSingleResponse:
        request_path = f"/api/v1/public/ticker?market={market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MarketSingleResponse(**json_obj)

    async def get_kline_market(
            self,
            market: str,
            start: int = None,  # Example: 1596848400
            end: int = None,  # Example: 1596927600
            interval: str = None,  # Possible values - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M.
            limit: int = None  # Possible values from 1 to 1440. Default value is 1440 in api
    ) -> KlineV1:
        request_path = f"/api/v1/public/kline?market={market}"
        if start:
            request_path = request_path + f"&start={start}"
        if end:
            request_path = request_path + f"&end={end}"
        if interval:
            request_path = request_path + f"&interval={interval}"
        if limit:
            request_path = request_path + f"&limit={limit}"

        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_kline_to_object(json_obj)

    async def get_symbols(self) -> SymbolsV1:
        request_path = "/api/v1/public/symbols"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return SymbolsV1(**json_obj)

    async def get_order_depth(self, market: str) -> OrderDepthV1:
        request_path = f"/api/v1/public/depth/result?market={market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_order_depth_to_object(json_obj)

    async def get_trade_history(self, market: str, last_id: int, limit: int = None) -> TradeHistoryV1:
        request_path = f"/api/v1/public/history?market={market}&lastId={last_id}"
        if limit:
            request_path = request_path + f"&limit={limit}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return TradeHistoryV1(**json_obj)
