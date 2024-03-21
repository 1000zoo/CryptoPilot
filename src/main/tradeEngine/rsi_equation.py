import pyupbit as pu
import pandas as pd
import numpy as np
import pandas_ta as ta

def rsi():
    data=ta.rsi(pu.get_ohlcv("KRW-BTC",interval='minute1',count=200)['close'],length=14)

    check_num=data.iloc[-2]
    check_pos=data.iloc[-1]-data.iloc[-2]

    # 0 : stop, 1 : buy, -1 : sell
    if check_num>=70 and check_pos<0:
        return -1
    elif check_num>=70 and check_pos>0:
        return 0
    elif check_num<=30 and check_pos>0:
        return 1
    elif check_num<=30 and check_pos<0:
        return 0
    else:
        return 0