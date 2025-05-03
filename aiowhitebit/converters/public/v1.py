"""Converters for the WhiteBit Public API v1."""

from aiowhitebit.models.public.v1.response import (
    Kline,
    KlineItem,
    OrderDepth,
    OrderDepthItem,
    Ticker,
    Tickers,
)


def convert_tickers_to_object(json_body: dict) -> Tickers:
    """Convert tickers JSON response to Tickers object.

    Args:
        json_body: JSON response from the API

    Returns:
        Tickers object
    """
    items = []
    for k, v in json_body.get("result", {}).items():
        ticker_body = dict(v["ticker"])
        ticker_body["name"] = k
        ticker_body["at"] = v["at"]
        item = Ticker(**ticker_body)
        items.append(item)

    success = bool(json_body.get("success", False))
    message = json_body.get("message", "")
    return Tickers(success=success, message=message, result=items)


def convert_kline_to_object(json_body: dict) -> Kline:
    """Convert kline JSON response to Kline object.

    Args:
        json_body: JSON response from the API

    Returns:
        Kline object
    """
    items = []
    for i in json_body.get("result", []):
        t_sec, op, close, high, low, vol_st, vol_mon = i
        kline = KlineItem(
            time_seconds=t_sec, open=op, close=close, high=high, low=low, volume_stock=vol_st, volume_mmoney=vol_mon
        )
        items.append(kline)

    success = bool(json_body.get("success", False))
    message = json_body.get("message", "")
    return Kline(success=success, message=message, result=items)


def gen_order(arr: list) -> list[OrderDepthItem]:
    """Generate a list of OrderDepthItem objects from a list of price-amount pairs.

    Args:
        arr: List of price-amount pairs

    Returns:
        List of OrderDepthItem objects
    """
    temp = []
    for item in arr:
        price, amount = item
        order = OrderDepthItem(price=price, amount=amount)
        temp.append(order)
    return temp


def convert_order_depth_to_object(json_body: dict) -> OrderDepth:
    """Convert order depth JSON response to OrderDepth object.

    Args:
        json_body: JSON response from the API

    Returns:
        OrderDepth object
    """
    asks = gen_order(json_body.get("asks", []))
    bids = gen_order(json_body.get("bids", []))

    return OrderDepth(asks=asks, bids=bids)
