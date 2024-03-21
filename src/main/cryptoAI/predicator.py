import os
import sys
import datetime

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

import keras
import numpy as np
import pyupbit as pu

from src.main.cryptoAI.preprocess import preprocessing, time_embedding_preprocessing

TEMPORARY_MODEL_PATH = "model/lstm-time-embedding-sequence20-batchsize64-best-0033.h5"

TICKER = "KRW-BTC"
INTERVAL = "minute1"
SEQUENCE_LENGTH = 20

TRADING_THRESHOLD = 0.01

def time_embedding_predict() -> int:
    ohlcv = pu.get_ohlcv(TICKER, INTERVAL, SEQUENCE_LENGTH + 2)
    data = time_embedding_preprocessing(ohlcv, SEQUENCE_LENGTH)
    result = model_predict(data)
    print(result)
    return _encode(result)

"""
predict(): 실제로 호출되는 부분 (외부로부터 호출받는 부분)

return
연속된 두 ohlcv를 통해 가격의 추세를 예측한다.
상승 => 1 / 횡보 => 0 / 하락 => -1
"""
def predict() -> int:
    ohlcv = pu.get_ohlcv(TICKER, INTERVAL, SEQUENCE_LENGTH + 2)
    data = preprocessing(ohlcv, SEQUENCE_LENGTH)
    print(data.shape)
    result = model_predict(data)
    print(result)
    return _encode(result)

    
"""
model_predict: 모델로부터 가격을 예측받는다. 외부에서 호출해야하는 메서드는 아님

파라미터
- sequence는 {모델의 input 개수} 만큼의 OHLCV 값들이 전처리 되어 ndarray로 들어온다.
"""
def model_predict(sequence : np.ndarray):
    model = load_model()
    result = model.predict(sequence)
    result = np.mean(result, axis=1)

    return result

"""
load_model: 저장된 모델 불러오기

모델 선택 방식 (고정 모델 or 파인튜닝 모델)에 따라
추후에 분리될 수 있음
"""
def load_model():
    return keras.models.load_model(TEMPORARY_MODEL_PATH)


def _encode(result : np.ndarray):
    d = result[1] - result[0]
    absolute = abs(d)
    
    if absolute < TRADING_THRESHOLD:
        return 0
    
    return 1 if d > 0 else -1


if __name__ == "__main__":
    result = time_embedding_predict()
    print(result)

