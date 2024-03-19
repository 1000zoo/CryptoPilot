import pyupbit as pu
import datetime
import time
from src.main.cryptoAI.predicator import predict
from src.main.runner.investor import Investor
from src.main.tradeEngine.ema_equation import *
from src.main.tradeEngine.rsi_equation import rsi

#매수, 매도 진행 코드
def trade_engine(investor : Investor):
    prev_state=None
    cnt=0
    while cnt<=4:
        state = rsi()
        if state==0:
            return 0
        if prev_state==None:
            prev_state=state
            continue
        
        if prev_state==state:
            cnt+=1
        else:
            return 0
        time.sleep(1)

    return state   

def main(investor : Investor):
    #이전 시간 기록
    previous_minute=None
    
    #매 분마다 매매 진행
    while True:
        current_time=datetime.datetime.now()
        current_minute=current_time.minute

        state=trade_engine(investor)

        flag=investor.get_balance("BTC")>0
        
        if flag:
            if state==-1:
                investor.sell_market_order('KRW-BTC',investor.get_balance('BTC'))
        else:
            if state==1:
                investor.buy_market_order("KRW-BTC",investor.get_balance('KRW'))

        if previous_minute==None:
            previous_minute=current_minute
        
        elif current_minute!=previous_minute:
            previous_minute=current_minute
            print(current_time,investor.get_balance("KRW"),investor.get_balance("BTC"))
        #1초마다 시간 확인
        time.sleep(1)