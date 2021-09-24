__all__ = [
    "BaseWhitebitWSClient",
    "WhitebitPublicWSClient",
    "get_ws_public_client",
]

import json
import logging
from typing import Optional

import websockets

from aiowhitebit.constants import BASE_WS_PUBLIC_URL
from aiowhitebit.ws_data_models import WSRequest, WSResponse


class BaseWhitebitWSClient:
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self.connection: Optional[websockets.WebSocketClientProtocol] = None

    async def connect(self):
        if not self.connection:
            self.connection = await websockets.connect(self.uri)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def send_message(self, request: dict) -> dict:
        await self.connect()
        # async with websockets.connect(self.uri) as websocket:
        await self.connection.send(json.dumps(request))
        logging.info(f">>> {request}")

        response = await self.connection.recv()
        msg_json = json.loads(response)
        logging.info(f">>> {response}")
        return msg_json


class WhitebitPublicWSClient:
    def __init__(self, ws: BaseWhitebitWSClient = None) -> None:
        self.ws = ws

    async def base_ws_requester(self, req: WSRequest) -> WSResponse:
        response = await self.ws.send_message(req.dict())
        return WSResponse(**response)

    async def ping(self) -> WSResponse:
        return await self.base_ws_requester(WSRequest(method="ping", params=[]))

    async def time(self) -> WSResponse:
        return await self.base_ws_requester(WSRequest(method="time", params=[]))

    async def kline(
        self, market: str, start_time: int, end_time: int, interval_secs: int
    ) -> WSResponse:
        return await self.base_ws_requester(
            WSRequest(
                method="candles_request",
                params=[market, start_time, end_time, interval_secs],
            )
        )

    async def last_price(self, market: str) -> WSResponse:
        return await self.base_ws_requester(
            WSRequest(method="lastprice_request", params=[market])
        )

    async def market_stats(self, market: str, period_secs: int) -> WSResponse:
        return await self.base_ws_requester(
            WSRequest(method="market_request", params=[market, period_secs])
        )

    async def market_stats_today(self, market: str) -> WSResponse:
        """
        Market statistics for current day UTC
        """
        return await self.base_ws_requester(
            WSRequest(method="marketToday_query", params=[market])
        )

    async def market_trades(
        self, market: str, limit: int, largest_id: int
    ) -> WSResponse:
        return await self.base_ws_requester(
            WSRequest(method="trades_request", params=[market, limit, largest_id])
        )

    async def market_depth(self, market: str, limit: int, intervals: str) -> WSResponse:
        """
        :param market:
        :param limit:
        :param intervals: "0" - no interval,
        available values - "0.00000001", "0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.01", "0.1"
        :return:
        """
        return await self.base_ws_requester(
            WSRequest(method="depth_request", params=[market, limit, intervals])
        )

    async def close(self):
        await self.ws.close()


def get_ws_public_client() -> WhitebitPublicWSClient:
    return WhitebitPublicWSClient(BaseWhitebitWSClient(BASE_WS_PUBLIC_URL))
