import unittest
import pyupbit
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

from src.main.cryptoAI.preprocess import *


class PreprocessTest(unittest.TestCase):

    def print_preprocessing(self):
        print(preprocessing(pyupbit.get_ohlcv("KRW-BTC", "minute1", 5)))


def test_dataframe_results():
    data = preprocessing(pyupbit.get_ohlcv("KRW-BTC", "minute1", 5))
    print(data.shape)
    print(type(data))
    print(data)

if __name__ == "__main__":
    test_dataframe_results()

