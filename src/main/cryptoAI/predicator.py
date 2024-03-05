import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

import keras
import numpy as np
import pyupbit as pu

from src.main.cryptoAI.preprocess import preprocessing

TEMPORARY_MODEL_PATH = "model/datasize2000000-sequence64-epochs500-batchsize2048-ckpt0005.h5"

TICKER = "KRW-BTC"
INTERVAL = "minute1"
SEQUENCE_LENGTH = 64

TRADING_THRESHOLD = 0.01

"""
predict(): 실제로 호출되는 부분 (외부로부터 호출받는 부분)

return
연속된 두 ohlcv를 통해 가격의 추세를 예측한다.
상승 => 1 / 횡보 => 0 / 하락 => -1
"""
def predict() -> int:
    ohlcv = pu.get_ohlcv(TICKER, INTERVAL, SEQUENCE_LENGTH + 1)
    result = model_predict(preprocessing(ohlcv, SEQUENCE_LENGTH))
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
    pass
