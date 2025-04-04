import asyncio

from aiowhitebit.clients.public import PublicV2Client

# For backward compatibility, you can also use:
# from aiowhitebit.clients.public_clients import AioWhitebitPublicV2Client


async def main():
    client = PublicV2Client()
    # For backward compatibility, you can also use:
    # client = AioWhitebitPublicV2Client()
    res = await client.get_market_info()

    res = await client.get_tickers()

    res = await client.get_recent_trades("BTC_USDT")

    res = await client.get_fee()

    res = await client.get_asset_status_list()

    res = await client.get_order_depth("BTC_USDT")
    print(res)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
