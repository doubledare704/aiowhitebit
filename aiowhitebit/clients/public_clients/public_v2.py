from aiowhitebit.clients.public_clients.base import base_get_request
from aiowhitebit.clients.public_clients.converters import convert_asset_status_to_object, \
    convert_order_depth_to_object_v2
from aiowhitebit.constants import BASE_URL
from aiowhitebit.http_data_models import MarketInfoV2, TickersV2, RecentTradesV2, FeeV2, AssetStatusV2, OrderDepthV2


class AioWhitebitPublicV2Client:
    def __init__(
            self,
            base_url: str = BASE_URL,
    ) -> None:
        self.base_url = base_url

    def request_url(self, path) -> str:
        return f"{self.base_url}{path}"

    async def get_market_info(self) -> MarketInfoV2:
        request_path = "/api/v2/public/markets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return MarketInfoV2(**json_obj)

    async def get_tickers(self) -> TickersV2:
        request_path = "/api/v2/public/ticker"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return TickersV2(**json_obj)

    async def get_recent_trades(self, market: str) -> RecentTradesV2:
        request_path = f"/api/v2/public/trades/{market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return RecentTradesV2(**json_obj)

    async def get_fee(self) -> FeeV2:
        request_path = "/api/v2/public/fee"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return FeeV2(**json_obj)

    async def get_asset_status_list(self) -> AssetStatusV2:
        request_path = "/api/v2/public/assets"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_asset_status_to_object(json_obj)

    async def get_order_depth(self, market: str) -> OrderDepthV2:
        request_path = f"/api/v2/public/depth/{market}"
        full_url = self.request_url(request_path)
        json_obj = await base_get_request(full_url)

        return convert_order_depth_to_object_v2(json_obj)
