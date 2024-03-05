import pyupbit as pu
import os
import sys
import csv
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

def _csv_title(title):
    if not ".csv" in title:
        return title + ".csv"
    return title

def _get_path(title):
    log_path = os.path.join(root_path, "log")
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return os.path.join(log_path, _csv_title(title))

class Logger:
    def __init__(self, title) -> None:
        self.path = _get_path(title)
        try:
            with open(self.path, 'x', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                header = ["Time Stamp", "Ticker", "Trade Type", "Trade Price", "Price", "Volume", "Profit"]
                writer.writerow(header)
        except FileExistsError:
            pass

    def write_trade_log(self,
                         ticker : str, trade_type : str,
                         trade_price : float, price : float, volume : float,
                         profit=0.0):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 데이터 기록
        with open(self.path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            data = [timestamp, ticker, trade_type, trade_price, price, volume, profit]
            writer.writerow(data)

class Investor:
    def __init__(self, upbit : pu.Upbit, logger : Logger) -> None:
        self.upbit = upbit
        self.logger = logger
        self.__init_krw = upbit.get_balance("KRW")

    def buy_market_order(self, ticker : str, price):
        response = self.upbit.buy_market_order(ticker, price)
        if response:
            self.logger.write_trade_log(
                ticker=ticker, trade_type="buy", trade_price=self.get_trade_price(response),
                price=self.get_price(response), volume=self.get_volume(response)
            )

    def sell_market_order(self, ticker, volume):
        response = self.upbit.sell_market_order(ticker, volume)
        if response:
            trade_price = self.get_trade_price(response)
            v = self.get_volume(response)
            self.logger.write_trade_log(
                ticker=ticker, trade_type="sell", trade_price=trade_price,
                price=trade_price*v, volume=v
            )

    def get_balance(self, ticker="KRW"):
        return self.upbit.get_balance(ticker)
    
    def get_amount(self, ticker="KRW"):
        return self.upbit.get_amount(ticker)

    def get_trade_price(self, trade_log : dict):
        if not "uuid" in trade_log:
            return -1
        try:
            return float(self.upbit.get_individual_order(trade_log["uuid"])["trades"][0]["price"])
        except KeyError as e:
            print(e)
            return -1
        
    def get_volume(self, trade_log : dict):
        if not "uuid" in trade_log:
            return -1
        try:
            return float(self.upbit.get_individual_order(trade_log["uuid"])["trades"][0]["volume"])
        except KeyError as e:
            print(e)
            return -1
        
    def get_price(self, trade_log : dict):
        if not "uuid" in trade_log:
            return -1
        try:
            return float(trade_log["price"])
        except KeyError as e:
            print(e)
            return -1



if __name__ == "__main__":
    from ___key___ import ACCESS_KEY, SECRET_KEY
    upbit = pu.Upbit(ACCESS_KEY, SECRET_KEY)
    logger = Logger("real upbit test 0440")
    inv = Investor(upbit, logger)
    # inv.buy_market_order("KRW-BTC", 8000)
    inv.sell_market_order("KRW-BTC", 0.00009263)

