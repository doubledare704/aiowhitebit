import asyncio

from aiowhitebit.clients.public import PublicV1Client

# For backward compatibility, you can also use:
# from aiowhitebit.clients.public_clients import AioWhitebitPublicV1Client


async def main():
    client = PublicV1Client()
    # For backward compatibility, you can also use:
    # client = AioWhitebitPublicV1Client()
    res = await client.get_market_info()

    res = await client.get_tickers()

    res = await client.get_single_market("BTC_USDT")

    res = await client.get_kline_market("BTC_USDT")

    res = await client.get_symbols()

    res = await client.get_order_depth("BTC_USDT")

    res = await client.get_trade_history("BTC_USDT", 6)
    print(res)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
