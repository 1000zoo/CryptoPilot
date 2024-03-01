import unittest
import pyupbit
import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.preprocess import *
from src.main.cryptoAI.predicator import *


class PredicatorTest(unittest.TestCase):
    def test_encode(self):
        from src.main.cryptoAI.predicator import _encode, TRADING_THRESHOLD
        self.assertEqual(_encode(np.array([0.3, 0.3 + TRADING_THRESHOLD * 1.1])), 1)
        self.assertEqual(_encode(np.array([0.3, 0.3 + TRADING_THRESHOLD / 10])), 0)
        self.assertEqual(_encode(np.array([0.3, 0.3 - TRADING_THRESHOLD * 1.1])), -1)



def test_model_predict():
    data = preprocessing(pyupbit.get_ohlcv("KRW-BTC", "minute1", 6))
    result = model_predict(data)
    print(datetime.datetime.now())
    print(result)

def test_predict():
    print(datetime.datetime.now())
    p = predict()
    print(p)


if __name__ == "__main__":
    # test_model_predict()
    test_predict()
    # unittest.main()

