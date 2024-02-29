import pyupbit as pu
import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.runner.invastor import *
from src.test.mockUpbit.mockUpbit import *


def test_log():
    logger = Logger("tes1t_na311me")
    logger.write_trade_log("BTC", "buy", 44.44, 55.55, 66.66, 77.77)

class InvastorTest:
    def __init__(self) -> None:
        self.user = Invastor(MockUpbit(100000, 0), Logger("invastorTest"))
    
    def test_buy(self):
        self.user.buy_market_order("KRW-BTC", 10000)

if __name__ == "__main__":
    # test_log()

    invastor = InvastorTest()
    invastor.test_buy()