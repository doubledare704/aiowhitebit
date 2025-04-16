import unittest

from aiowhitebit.converters.public import (
    convert_kline_to_object_v1,
    convert_order_depth_to_object_v1,
    convert_tickers_to_object_v1,
)
from aiowhitebit.models.public.v1 import Kline, OrderDepth, Tickers


class TestConverters(unittest.TestCase):
    def test_convert_tickers_to_object(self):
        # Test data
        json_data = {
            "success": True,
            "message": None,
            "result": {
                "BTC_USDT": {
                    "ticker": {
                        "bid": "9412.1",
                        "ask": "9416.33",
                        "low": "9203.13",
                        "high": "9469.99",
                        "last": "9414.4",
                        "vol": "27324.819448",
                        "deal": "254587570.43407191",
                        "change": "1.53",
                    },
                    "at": 159423219,
                },
                "ETH_BTC": {
                    "ticker": {
                        "bid": "0.032512",
                        "ask": "0.032544",
                        "low": "0.032301",
                        "high": "0.032990",
                        "last": "0.032519",
                        "vol": "1175.32",
                        "deal": "38.2275",
                        "change": "-0.76",
                    },
                    "at": 159423219,
                },
            },
        }

        # Convert to object
        result = convert_tickers_to_object_v1(json_data)

        # Verify the result
        self.assertIsInstance(result, Tickers)
        self.assertEqual(result.success, True)
        self.assertEqual(result.message, None)
        self.assertEqual(len(result.result), 2)

        # Check first ticker
        btc_ticker = next(ticker for ticker in result.result if ticker.name == "BTC_USDT")
        self.assertEqual(btc_ticker.bid, 9412.1)
        self.assertEqual(btc_ticker.ask, 9416.33)
        self.assertEqual(btc_ticker.low, 9203.13)
        self.assertEqual(btc_ticker.high, 9469.99)
        self.assertEqual(btc_ticker.last, 9414.4)
        self.assertEqual(btc_ticker.vol, 27324.819448)
        self.assertEqual(btc_ticker.deal, 254587570.43407191)
        self.assertEqual(btc_ticker.change, 1.53)
        self.assertEqual(btc_ticker.at, 159423219)

        # Check second ticker
        eth_ticker = next(ticker for ticker in result.result if ticker.name == "ETH_BTC")
        self.assertEqual(eth_ticker.bid, 0.032512)
        self.assertEqual(eth_ticker.ask, 0.032544)
        self.assertEqual(eth_ticker.low, 0.032301)
        self.assertEqual(eth_ticker.high, 0.032990)
        self.assertEqual(eth_ticker.last, 0.032519)
        self.assertEqual(eth_ticker.vol, 1175.32)
        self.assertEqual(eth_ticker.deal, 38.2275)
        self.assertEqual(eth_ticker.change, -0.76)
        self.assertEqual(eth_ticker.at, 159423219)

    def test_convert_kline_to_object(self):
        # Test data
        json_data = {
            "success": True,
            "message": None,
            "result": [
                [1631440800, "45865.62", "45958.14", "45981.3", "45750.23", "15.327634", "703140.24230131"],
                [1631444400, "45958.14", "46280.19", "46280.19", "45958.14", "12.432913", "573142.58990234"],
            ],
        }

        # Convert to object
        result = convert_kline_to_object_v1(json_data)

        # Verify the result
        self.assertIsInstance(result, Kline)
        self.assertEqual(result.success, True)
        self.assertEqual(result.message, None)
        self.assertEqual(len(result.result), 2)

        # Check first kline
        self.assertEqual(result.result[0].time_seconds, 1631440800)
        self.assertEqual(result.result[0].open, 45865.62)
        self.assertEqual(result.result[0].close, 45958.14)
        self.assertEqual(result.result[0].high, 45981.3)
        self.assertEqual(result.result[0].low, 45750.23)
        self.assertEqual(result.result[0].volume_stock, 15.327634)
        self.assertEqual(result.result[0].volume_mmoney, 703140.24230131)

        # Check second kline
        self.assertEqual(result.result[1].time_seconds, 1631444400)
        self.assertEqual(result.result[1].open, 45958.14)
        self.assertEqual(result.result[1].close, 46280.19)
        self.assertEqual(result.result[1].high, 46280.19)
        self.assertEqual(result.result[1].low, 45958.14)
        self.assertEqual(result.result[1].volume_stock, 12.432913)
        self.assertEqual(result.result[1].volume_mmoney, 573142.58990234)

    def test_convert_order_depth_to_object(self):
        # Test data
        json_data = {
            "asks": [["9431.9", "0.705088"], ["9433.67", "0.324509"]],
            "bids": [["9427.65", "0.547909"], ["9427.3", "0.669249"]],
        }

        # Convert to object
        result = convert_order_depth_to_object_v1(json_data)

        # Verify the result
        self.assertIsInstance(result, OrderDepth)
        self.assertEqual(len(result.asks), 2)
        self.assertEqual(len(result.bids), 2)

        # Check asks
        self.assertEqual(result.asks[0].price, 9431.9)
        self.assertEqual(result.asks[0].amount, 0.705088)
        self.assertEqual(result.asks[1].price, 9433.67)
        self.assertEqual(result.asks[1].amount, 0.324509)

        # Check bids
        self.assertEqual(result.bids[0].price, 9427.65)
        self.assertEqual(result.bids[0].amount, 0.547909)
        self.assertEqual(result.bids[1].price, 9427.3)
        self.assertEqual(result.bids[1].amount, 0.669249)


if __name__ == "__main__":
    unittest.main()
