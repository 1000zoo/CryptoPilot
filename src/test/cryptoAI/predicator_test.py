import unittest
import pyupbit
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.cryptoAI.preprocess import *
from src.cryptoAI.predicator import *



class PredicatorTest(unittest.TestCase):
    pass


def test_predicate():
    data = preprocessing(pyupbit.get_ohlcv("KRW-BTC", "minute1", 5))
    result = predicate(data)
    import datetime
    print(datetime.datetime.now())
    print(result)

if __name__ == "__main__":
    test_predicate()

