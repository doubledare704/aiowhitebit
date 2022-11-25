from typing import List

from aiowhitebit.http_data_models.response_models import TickersV1, TickerItem, KlineV1, KlineItem, OrderDepthV1, \
    OrderDepthItem, AssetItemV2, AssetStatusV2, OrderDepthV2


def convert_tickers_to_object(
        json_body: dict,
) -> TickersV1:
    items = []
    for k, v in json_body.get("result", {}).items():
        ticker_body = dict(v["ticker"])
        ticker_body["name"] = k
        ticker_body["at"] = v["at"]
        item = TickerItem(**ticker_body)
        items.append(item)

    return TickersV1(
        success=json_body.get("success"),
        message=json_body.get("message"),
        result=items
    )


def convert_kline_to_object(
        json_body: dict,
) -> KlineV1:
    items = []
    for i in json_body.get("result", []):
        t_sec, op, close, high, low, vol_st, vol_mon = i
        kline = KlineItem(
            time_seconds=t_sec,
            open=op,
            close=close,
            high=high,
            low=low,
            volume_stock=vol_st,
            volume_mmoney=vol_mon
        )
        items.append(kline)

    return KlineV1(
        success=json_body.get("success"),
        message=json_body.get("message"),
        result=items
    )


def gen_order(arr: List):
    temp = []
    for item in arr:
        price, amount = item
        order = OrderDepthItem(price=price, amount=amount)
        temp.append(order)
    return temp


def convert_order_depth_to_object(
        json_body: dict,
) -> OrderDepthV1:
    asks = gen_order(json_body.get("asks", []))
    bids = gen_order(json_body.get("bids", []))

    return OrderDepthV1(asks=asks, bids=bids)


def convert_asset_status_to_object(
        json_body: dict,
) -> AssetStatusV2:
    items = []
    for k, v in json_body.get("result", {}).items():
        temp = dict(v)
        temp["asset_name"] = k
        asset = AssetItemV2(**temp)
        items.append(asset)
    return AssetStatusV2(
        success=json_body.get("success"),
        message=json_body.get("message"),
        result=items
    )


def convert_order_depth_to_object_v2(
        json_body: dict,
) -> OrderDepthV2:
    result = json_body["result"]
    asks = gen_order(result.get("asks", []))
    bids = gen_order(result.get("bids", []))
    last_update = result.get("lastUpdateTimestamp")
    return OrderDepthV2(lastUpdateTimestamp=last_update, asks=asks, bids=bids)
