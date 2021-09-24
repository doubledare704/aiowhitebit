__all__ = ["ws_subscribe_builder", "SubscribeRequest"]

import json
import pprint
from datetime import datetime
from typing import List

import websocket

from aiowhitebit.constants import BASE_WS_PUBLIC_URL
from aiowhitebit.ws_data_models import WSRequest


def infinite_sequence():
    num = 1
    while True:
        yield num
        num += 1


id_gen = infinite_sequence()


class SubscribeRequest:
    @staticmethod
    def candles_subscribe(market: str, interval: int) -> dict:
        return WSRequest(
            method="candles_subscribe", params=[market, interval], id=next(id_gen)
        ).dict()

    @staticmethod
    def lastprice_subscribe(markets: List[str]) -> dict:
        return WSRequest(
            method="lastprice_subscribe", params=[*markets], id=next(id_gen)
        ).dict()

    @staticmethod
    def market_subscribe(markets: List[str]) -> dict:
        return WSRequest(
            method="market_subscribe", params=[*markets], id=next(id_gen)
        ).dict()

    @staticmethod
    def market_today_subscribe(markets: List[str]) -> dict:
        return WSRequest(
            method="marketToday_subscribe", params=[*markets], id=next(id_gen)
        ).dict()

    @staticmethod
    def trades_subscribe(markets: List[str]) -> dict:
        return WSRequest(
            method="trades_subscribe", params=[*markets], id=next(id_gen)
        ).dict()

    @staticmethod
    def depth_subscribe(
            market: str,
            limit: int = 100,
            price_intervals: str = "0",
            multiple_sub: bool = True,
    ) -> dict:
        """
        :param multiple_sub:
        :param market:
        :param limit:
        :param price_intervals: "0.00000001", "0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.01", "0.1"
        """
        return WSRequest(
            method="depth_subscribe",
            params=[market, limit, price_intervals, multiple_sub],
            id=next(id_gen),
        ).dict()


def ws_subscribe_builder(sub_msg: dict) -> None:
    def on_open(wsapp):
        print(f">>> Opened subscriber: {sub_msg['method']}")
        wsapp.send(json.dumps(sub_msg))

    def on_message(wsapp, message, prev=None):
        print(f"<<<<Received : {datetime.now()} {sub_msg['method']}")
        pprint.pprint(json.loads(message))

    def on_close(wsapp):
        print("Closed connection")

    endpoint = BASE_WS_PUBLIC_URL
    ws = websocket.WebSocketApp(
        endpoint, on_open=on_open, on_message=on_message, on_close=on_close
    )

    ws.run_forever()
