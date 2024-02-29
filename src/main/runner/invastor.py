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

class Invastor:
    def __init__(self, upbit : pu.Upbit, logger : Logger) -> None:
        self.upbit = upbit
        self.logger = logger
        self.__init_krw = upbit.get_balance("KRW")

    def buy_market_order(self, ticker : str, price):
        self.upbit.buy_market_order(ticker, price)
        trade_price = price * 0.95 / self.upbit.get_balance(ticker.split("-")[1])
        self.logger.write_trade_log(
            ticker=ticker, trade_type="buy", trade_price=trade_price,
            price=price, volume=price / trade_price
        )

    def sell_market_order(self, ticker, volume):
        self.upbit.sell_market_order(ticker, volume)

    def get_trade_price(self, trade_log : dict):
        if not "uuid" in trade_log:
            return -1
        try:
            return self.upbit.get_individual_order(trade_log["uuid"])["trades"][0]["price"]
        except KeyError as e:
            print(e)
            return -1



if __name__ == "__main__":
    pass

