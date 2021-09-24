import asyncio
import logging

from aiowhitebit.public_ws_client import WhitebitPublicWSClient, get_ws_public_client

logging.basicConfig()
logging.getLogger('ws_client').setLevel(logging.INFO)


async def main():
    ws_client: WhitebitPublicWSClient = get_ws_public_client()
    try:
        resp = await ws_client.ping()
        print(resp)
        resp = await ws_client.time()
        print(resp)
        resp = await ws_client.kline("ETH_BTC", 1579569940, 1580894800, 900)
        print(resp)
        resp = await ws_client.last_price("ETH_BTC")
        print(resp)
        resp = await ws_client.market_stats("ETH_BTC", 86400)
        print(resp)
        resp = await ws_client.market_stats_today("ETH_BTC")
        print(resp)
        resp = await ws_client.market_trades("ETH_BTC", 100, 41358445)
        print(resp)
        resp = await ws_client.market_depth("ETH_BTC", 100, "0.0001")
        print(resp)
    except KeyboardInterrupt:
        logging.error("Stop this")
        await asyncio.create_task(ws_client.close())


if __name__ == '__main__':
    asyncio.run(main())
