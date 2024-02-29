import unittest
from unittest.mock import patch

import pyupbit as pu
import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.preprocess import *
from src.main.cryptoAI.predicator import *
from src.test.mockUpbit.mockUpbit import MockUpbit

def fetch_data_from_api():
    return pu.get_current_price("KRW-BTC")

class MockUpbitTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.upbit = MockUpbit(1_000_000, 0)

    def test_buy_market_order(self):
        with patch("pyupbit.get_current_price") as mock:
            mock.return_value = 78_000_000

            self.upbit.buy_market_order("KRW-BTC", 100000)
            result = fetch_data_from_api()

            self.assertEqual(self.upbit.get_balance("KRW"), 900000)
            self.assertAlmostEqual(self.upbit.get_balance("BTC"), 100000 * 0.95 / 78_000_000, places=6)
            self.assertAlmostEqual(self.upbit.get_amount("BTC"), 100000 * 0.95, places=1)


    """
    상황
    팔천에 10만원 사고  => first_avg = 10만
    6천에 5만원 팔고
    다시 6천에 45만원 사고 => second_avg = (이전 수량 * 이전 평단 + 현재 구매 가격) / 전체 수량
    7천에 30만원 팔고
    7천에 20만원 사고   => third_avg
    """
    def test_avg_amount(self):
        price_list = [1000, 2000, 3000]
        first_buy = 100000
        second_buy = 450000
        third_buy = 200000

        first_sell = 50000
        second_sell = 300000

        with patch("pyupbit.get_current_price") as mock:
            mock.return_value = price_list[0]
            self.upbit.buy_market_order("KRW-BTC", first_buy)
            first_avg = self.upbit.get_avg_buy_price("BTC")

            mock.return_value = price_list[1]
            self.upbit.sell_market_order("KRW-BTC", first_sell / price_list[1])
            self.upbit.buy_market_order("KRW-BTC", second_buy)
            second_avg = self.upbit.get_avg_buy_price("BTC")

            mock.return_value = price_list[2]
            self.upbit.sell_market_order("KRW-BTC", second_sell / price_list[2])
            self.upbit.buy_market_order("KRW-BTC", third_buy)
            third_avg = self.upbit.get_avg_buy_price("BTC")

            print("first_avg", first_avg)       # => 1000
            print("second_avg", second_avg)     # => 1750.0
            print("third_avg", third_avg)       # => 2062.5


if __name__ == "__main__":
    unittest.main()
    # m = MockUpbitTest()
    # m.test_avg_amount()
