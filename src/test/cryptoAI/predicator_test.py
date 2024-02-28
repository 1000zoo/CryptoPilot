import unittest
import pyupbit
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.preprocess import *
from src.main.cryptoAI.predicator import *



class PredicatorTest(unittest.TestCase):
    pass


def test_model_predict():
    data = preprocessing(pyupbit.get_ohlcv("KRW-BTC", "minute1", 6))
    result = model_predict(data)
    import datetime
    print(datetime.datetime.now())
    print(result)

if __name__ == "__main__":
    test_model_predict()

