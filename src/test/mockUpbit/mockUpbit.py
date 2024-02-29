import pyupbit as pu
import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.preprocess import *
from src.main.cryptoAI.predicator import *

class MockUpbit(pu.Upbit):
    def __init__(self, start_krw, start_btc):
        self.krw_balance = start_krw
        self.btc_balance = start_btc # 수량을 의미
        self.avg_buy_price = pu.get_current_price("KRW-BTC") if start_btc > 0 else 0

    def get_balances(self):
        return f"krw amount: {self.krw_balance}, btc amount: {self.btc_balance}"
    
    def get_balance(self, ticker="KRW"):
        return self.btc_balance if ticker.upper() == "BTC" else self.krw_balance
    
    def get_balance_t(self, ticker='KRW'):
        return self.get_balance(ticker)
    
    def get_avg_buy_price(self, ticker='KRW'):
        if ticker.upper() == "KRW":
            return self.krw_balance
        return self.avg_buy_price

    def get_amount(self, ticker):
        if ticker.upper() != "BTC":
            return 0
        return self.btc_balance * pu.get_current_price("KRW-BTC")
    
    def buy_market_order(self, ticker, price, contain_req=False):
        if ticker != "KRW-BTC":
            return
        if self.krw_balance < price:
            return
        self.krw_balance -= price
        buy_amount = (price * 0.95)/ (pu.get_current_price("KRW-BTC"))
        self.avg_buy_price = ((self.avg_buy_price * self.btc_balance) + price) / (self.btc_balance + buy_amount)
        self.btc_balance += buy_amount

    def sell_market_order(self, ticker, volume, contain_req=False):
        if ticker != "KRW-BTC":
            return
        if self.btc_balance < volume:
            return
        self.btc_balance -= volume
        self.krw_balance += volume * pu.get_current_price("KRW-BTC") * 0.95
    
    # 안쓰는 메서드여도 최소 주문 관련 메서드는 만일을 대비하여 빈 메서드 구현
    def get_chance(self, ticker, contain_req=False):
        return ""
    
    def get_order(self, ticker_or_uuid, state='wait', page=1, limit=100, contain_req=False):
        return ""
    
    def get_individual_order(self, uuid, contain_req=False):
        return ""
    
    def cancel_order(self, uuid, contain_req=False):
        return ""
        
    def buy_limit_order(self, ticker, price, volume, contain_req=False):
        return ""
    
    def sell_limit_order(self, ticker, price, volume, contain_req=False):
        return ""

    def get_api_key_list(self):
        return ""
    

if __name__ == "__main__":
    pass