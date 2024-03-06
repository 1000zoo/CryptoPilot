import pyupbit as pu
import datetime
import time
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.predicator import predict
from src.main.runner.investor import *
from src.main.tradeEngine.ema_equation import discriminant
from src.test.mockUpbit.mockUpbit import *
from src.main.tradeEngine.trade_engine import main

upbit=MockUpbit(100_000,0)
logger=Logger('test_log_20240305')

investor=Investor(upbit,logger)

main(investor)