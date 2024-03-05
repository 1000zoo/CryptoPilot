import pyupbit as pu
import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.runner.investor import *
from src.test.mockUpbit.mockUpbit import *


def test_log():
    logger = Logger("tes1t_na311me")
    logger.write_trade_log("BTC", "buy", 44.44, 55.55, 66.66, 77.77)

class InvestorTest:
    def __init__(self) -> None:
        self.user = Investor(MockUpbit(100000, 0), Logger("investorTest"))
    
    def test_buy(self):
        self.user.buy_market_order("KRW-BTC", 10000)

if __name__ == "__main__":
    # test_log()

    investor = InvestorTest()
    investor.test_buy()