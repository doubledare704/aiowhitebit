from aiowhitebit.clients.public_ws_subscriber import ws_subscribe_builder, SubscribeRequest

if __name__ == '__main__':
    import threading

    sub_conf = SubscribeRequest()
    possible_sub_requests = [
        sub_conf.candles_subscribe("BTC_USD", 900),
        sub_conf.lastprice_subscribe(["ETH_BTC", "BTC_USDT"]),
        sub_conf.market_subscribe(["ETH_BTC", "BTC_USDT"]),
        sub_conf.market_today_subscribe(["ETH_BTC", "BTC_USDT"]),
        sub_conf.trades_subscribe(["ETH_BTC", "BTC_USDT"]),
        sub_conf.depth_subscribe("ETH_BTC"),
    ]

    for item in possible_sub_requests:
        current_thread = threading.Thread(target=ws_subscribe_builder, args=(item,), daemon=True)
        current_thread.start()
    input('Hit enter to terminate...\n')
