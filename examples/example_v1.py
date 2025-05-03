import asyncio

from aiowhitebit.clients.public import PublicV1Client



async def main():
    client = PublicV1Client()
    # For backward compatibility, you can also use:
    # client = AioWhitebitPublicV1Client()
    res = await client.get_market_info()
    print(res)
    res = await client.get_tickers()
    print(res)

    res = await client.get_single_market("BTC_USDT")
    print(res)

    res = await client.get_kline_market("BTC_USDT")
    print(res)

    res = await client.get_symbols()
    print(res)

    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
