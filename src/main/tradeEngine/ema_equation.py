import numpy as np
import pandas as pd
import pyupbit as pu

#단순 이동평균
def sma_equation(n):
    n_value=pu.get_ohlcv("KRW-BTC",interval='day',count=n)['close'].mean()
    return n_value

#지수 이동평균
def ema_equation(n):
    cur_price=pu.get_current_price("KRW-BTC")
    K = 2 / (n + 1)
    prev_ema=sma_equation(n)

    return (cur_price * K) + (prev_ema * (1 - K))

#판단 지표
def discriminant():
    cur_price=pu.get_current_price("KRW-BTC")
    day5,day10,day20=ema_equation(5),ema_equation(10),ema_equation(20)

    if cur_price>=day5 and cur_price>=day10 and cur_price>=day20:
        return True
    else:
        return False