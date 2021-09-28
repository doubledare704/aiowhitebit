import asyncio

from aiowhitebit.http_data_models import CreateLimitOrderRequest
from aiowhitebit.clients.private_http_client import AioWhitebitPrivateClient


async def main():
    client = AioWhitebitPrivateClient()
    res = await client.get_trading_balance("XTZ")
    print(res)
    await asyncio.sleep(1)
    res = await client.create_limit_order(
        CreateLimitOrderRequest(
            market="BTC_USDT",
            side="buy",
            amount="0.01",
            price="9800",
        )
    )
    print(res)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
