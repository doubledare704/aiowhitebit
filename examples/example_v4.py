import asyncio

from aiowhitebit.clients.public import PublicV4Client


async def main():
    client = PublicV4Client()

    # Get maintenance status
    status = await client.get_maintenance_status()
    print(f"Maintenance status: {status.status}")

    # Get market info
    markets = await client.get_market_info()
    print(f"Number of markets: {len(markets)}")
    print(f"First market: {markets[0]['name']}")

    # Get market activity
    activity = await client.get_market_activity()
    print(f"Number of active markets: {len(activity)}")
    print(f"BTC_USDT last price: {activity.get('BTC_USDT').last_price}")

    # Get asset status list
    assets = await client.get_asset_status_list()
    print(f"Number of assets: {len(assets)}")
    print(f"BTC name: {assets.get('BTC').name}")

    # Get orderbook
    orderbook = await client.get_orderbook("BTC_USDT", limit=5)
    print(f"Orderbook timestamp: {orderbook.timestamp}")
    print(f"Top ask: {orderbook.asks[0]}")
    print(f"Top bid: {orderbook.bids[0]}")

    # Get depth
    depth = await client.get_depth("BTC_USDT")
    print(f"Depth timestamp: {depth.timestamp}")
    print(f"Number of asks: {len(depth.asks)}")
    print(f"Number of bids: {len(depth.bids)}")

    # Get recent trades
    trades = await client.get_recent_trades("BTC_USDT", trade_type="sell")
    print(f"Number of trades: {len(trades)}")
    print(f"First trade: {trades[0].tradeID}, {trades[0].price}, {trades[0].type}")

    # Get server time
    time = await client.get_server_time()
    print(f"Server time: {time.time}")

    # Get server status
    server_status = await client.get_server_status()
    print(f"Server status: {server_status}")

    # Get collateral markets
    collateral_markets = await client.get_collateral_markets()
    print(f"Number of collateral markets: {len(collateral_markets)}")
    print(f"First collateral market: {collateral_markets[0]}")

    # Get futures markets
    futures_markets = await client.get_futures_markets()
    print(f"Number of futures markets: {len(futures_markets.result)}")
    print(f"First futures market: {futures_markets.result[0].ticker_id}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
