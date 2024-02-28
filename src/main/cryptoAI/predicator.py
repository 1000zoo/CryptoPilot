import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(root_path)

import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler

TEMPORARY_MODEL_PATH = "model/RNN_initial_model.h5"



"""
model_predict: 모델로부터 가격을 예측받는다.

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


"""
mock_scaler: 가짜 스케일러 생성

모델 학습 당시 y_scaler를 구할 수 없으므로
임시적인 가짜 스케일러를 최소값, 최대값 만으로 구성
"""
def mock_scaler():
    MIN = 3_730_000
    MAX = 82_700_000
    scaler = MinMaxScaler()
    scaler.fit([[MIN], [MAX]])
    return scaler



if __name__ == "__main__":
    pass
