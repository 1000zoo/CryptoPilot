import pyupbit
import datetime
import time

#로그인
#upbit=pyupbit.Upbit(access_key,secret_key)
upbit=1     #임시

#매도
def sell(amount):
    #upbit.sell_market_order("KRW-BTC",amount)
    pass

#매수
def buy(price):
    #upbit.buy_market_order("KRW-BTC",price)
    pass

#매수, 매도 진행 코드
def trade_engine(flag,amount,money):
    #현재 비트코인의 가격(보유중인 가격 혹은 현재 시장가격)
    #현재 가격에 대한 코드는 추가 작업이 필요함(보유중이지 않다면 예측값을 저장해서 가지고 있어야함)
    #current_price=upbit.get_balance('KRW-BTC')['avg_buy_price']
    current_price=75000000      #임시

    #1분뒤 예측되는 비트코인의 가격
    #predict_price=예측값 호출
    predict_price=76000000        #임시

    #현재 비트코인을 보유하고 있을 때
    if flag:
        #예측값이 더 오를것으로 예상될 경우, 아무 행동도 취하지 않음
        if is_wait(current_price,predict_price):
            pass
        #예측값이 떨어질 것으로 예상될 경우, 매도 진행
        else:
            sell(amount)        #수량은 나중에 따로 관리
    #비트코인을 보유하고 있지 않을 때
    else:
        #예측값이 오를 것으로 예상될 경우, 매수 진행
        if is_wait(current_price,predict_price):
            buy(money*0.95)     #수수료 제외
        #예측값이 떨어질 것으로 예상될 경우, 아무 행동도 취하지 않음
        else:
            pass
#판별식
def is_wait(current,next):
    #기울기
    inclination=(next-current)/current

    #기울기가 0이상일 경우
    if inclination>=0:
        return True
    
    #기울기가 음수일 경우
    #미세 조정 필요
    else:
        #수익률이 -0.05%보다는 높다면 True
        if inclination>-0.05:
            return True
        #수익률이 -0.05%이하면 False
        else:
            return False

def main():
    #현재 보유중인 현금
    #money=upbit.get_balance('KRW-BTC')
    money=80000000

    #보유중인 비트코인 수량
    amount=10       #임시

    #현재 보유중인지 아닌지 상태 저장
    flag=True if amount>0 else False

    #이전 시간 기록
    previous_minute=None

    #매 분마다 매매 진행
    while True:
        current_time=datetime.datetime.now()
        current_minute=current_time.minute

        #시간이 변경됐으면 매매함수 호출
        if current_minute!=previous_minute:
            previous_minute=current_minute
            trade_engine(flag,amount,money)

        #1초마다 시간 확인
        time.sleep(1)