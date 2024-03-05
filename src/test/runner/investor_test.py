import pyupbit as pu
import os
import sys
import time
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


def cal(investor : Investor):
    state = predict()
    print(state)
    btc_balance = investor.get_balance("BTC")
    krw_balance = investor.get_balance("KRW")
    
    if btc_balance > 0:
        if state==0 or state==1:
            pass
        else:
            investor.sell_market_order("KRW-BTC", btc_balance)
    else:
        if state==1:
            investor.buy_market_order("KRW-BTC", krw_balance)
        else:
            pass

    current_time = datetime.datetime.now().strftime("%Y-%m-%d - %H:%M:%S")
    krw = investor.get_balance("KRW")
    btc = investor.get_balance("BTC")
    btc_amount = investor.get_amount("BTC")
    print(f"{current_time} ==> krw: {krw}, btc: {btc}, btc to krw: {btc_amount}")

def loop_test():
    previous_minute = None
    cnt = 0
    investor = Investor(MockUpbit(10000000, 0), 
                        Logger(str(datetime.datetime.now().strftime("%Y-%m-%d - %H-%M"))))
    while cnt<60 * 300:
        current_time = datetime.datetime.now()
        current_minute = current_time.minute
        #시간이 변경됐으면 매매함수 호출
        if previous_minute==None or current_minute!=previous_minute:
            previous_minute=current_minute
            cal(investor)
        #1초마다 시간 확인
        time.sleep(1)
        cnt+=1

def main():
    loop_test()

if __name__ == "__main__":
    # test_log()

    # investor = InvestorTest()
    # investor.test_buy()
    main()