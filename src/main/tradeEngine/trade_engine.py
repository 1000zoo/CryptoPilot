import pyupbit as pu
import datetime
import time
from src.main.cryptoAI.predicator import predict, time_embedding_predict
from src.main.runner.investor import Investor
from src.main.tradeEngine.ema_equation import *

#매수, 매도 진행 코드
def trade_engine(investor : Investor):
    #현재 비트코인의 가격(보유중인 가격 혹은 현재 시장가격)
    #현재 가격에 대한 코드는 추가 작업이 필요함(보유중이지 않다면 예측값을 저장해서 가지고 있어야함)
    #current_price=upbit.get_balance('KRW-BTC')['avg_buy_price'] if flag else 0
    krw_amount = investor.get_balance("KRW")
    btc_amount = investor.get_balance("BTC")
    flag = btc_amount > 0

    #1분뒤 예측되는 비트코인의 가격
    #predict_price=예측값 호출
    predict_state = time_embedding_predict()
    dis_state= True
    #현재 비트코인을 보유하고 있을 때
    if flag:
        #예측값이 더 오를것으로 예상될 경우, 아무 행동도 취하지 않음
        if predict_state == 1 and dis_state:
            pass
        #예측값이 떨어질 것으로 예상될 경우, 매도 진행
        else:
            investor.sell_market_order("KRW-BTC", btc_amount)       #수량은 나중에 따로 관리
    #비트코인을 보유하고 있지 않을 때
    else:
        #예측값이 오를 것으로 예상될 경우, 매수 진행
        if predict_state ==1 and dis_state:
            investor.buy_market_order("KRW-BTC", krw_amount)     #수수료 제외
        #예측값이 떨어질 것으로 예상될 경우, 아무 행동도 취하지 않음
        else:
            pass


def main(investor : Investor):
    #이전 시간 기록
    previous_minute=None

    #매 분마다 매매 진행
    while True:

        current_time=datetime.datetime.now()
        current_minute=current_time.minute

        # #시간이 변경됐으면 매매함수 호출
        # if previous_minute==None:
        #     previous_minute=current_minute

        if current_minute!=previous_minute or previous_minute == None:
            previous_minute=current_minute
            trade_engine(investor)
            print(current_time,investor.get_balance("KRW"),investor.get_balance("BTC"))
        #1초마다 시간 확인
        time.sleep(1)