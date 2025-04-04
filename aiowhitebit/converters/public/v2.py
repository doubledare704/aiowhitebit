"""Converters for the WhiteBit Public API v2."""

from aiowhitebit.converters.public.v1 import gen_order
from aiowhitebit.models.public.v2.response import (
    Asset,
    AssetStatus,
    OrderDepthV2,
)


def convert_asset_status_to_object(json_body: dict) -> AssetStatus:
    """Convert asset status JSON response to AssetStatus object.

    Args:
        json_body: JSON response from the API

    Returns:
        AssetStatus object
    """
    items = []
    for k, v in json_body.get("result", {}).items():
        temp = dict(v)
        temp["asset_name"] = k
        asset = Asset(**temp)
        items.append(asset)
    return AssetStatus(success=json_body.get("success"), message=json_body.get("message"), result=items)


def convert_order_depth_to_object_v2(json_body: dict) -> OrderDepthV2:
    """Convert order depth JSON response to OrderDepthV2 object.

    Args:
        json_body: JSON response from the API

    Returns:
        OrderDepthV2 object
    """
    result = json_body["result"]
    asks = gen_order(result.get("asks", []))
    bids = gen_order(result.get("bids", []))
    last_update = result.get("lastUpdateTimestamp")
    return OrderDepthV2(lastUpdateTimestamp=last_update, asks=asks, bids=bids)
