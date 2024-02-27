import pyupbit as pu
from pandas.core.frame import DataFrame


"""
predicate: 모델로부터 가격을 예측받는다.

파라미터
- pyupbit와 독립시키기 위해, 모델의 입력값이 될 sequence를 따로 받아온다.
- sequence는 {모델의 input 개수} 만큼의 OHLCV 값들이 DataFrame으로 들어온다.
"""
def predicate(sequence: DataFrame):
    pass


if __name__ == "__main__":
    pass
