import os
import sys
import pyupbit as pu
import datetime
import time
import keras
from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame
import unittest
from unittest.mock import patch

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.tradeEngine.trade_engine import *
from src.test.mockUpbit.mockUpbit import *

upbit=MockUpbit(10_000_000,0)

def cal(flag,money,amount):
    state=predict()

    if flag:
        if state==1:
            pass
        else:
            upbit.sell_market_order("KRW-BTC",amount)
    else:
        if state==1:
            upbit.buy_market_order("KRW-BTC",money)
        else:
            pass

def loop_test():
    previous_minute=None

    cnt=0
    while True:
        money=upbit.krw_balance
        amount=upbit.btc_balance
        flag=True if amount>0 else False

        current_time=datetime.datetime.now()
        current_minute=current_time.minute

        #시간이 변경됐으면 매매함수 호출
        if previous_minute==None:
            previous_minute=current_minute

        elif current_minute!=previous_minute:
            previous_minute=current_minute
            cal(flag,money,amount)
            print(current_time,upbit.get_balances())
        #1초마다 시간 확인
        time.sleep(1)
        cnt+=1

def main():
    loop_test()

print(main())