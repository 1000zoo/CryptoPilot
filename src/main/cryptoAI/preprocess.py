from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame
import numpy as np

def preprocessing(sequence: DataFrame, sequence_length: int):
    x_cols = [0, 1, 2, 4]

    x = sequence.iloc[:, x_cols].values
    x = MinMaxScaler().fit_transform(x)

    X = []
    for i in range(len(x) - sequence_length + 1):
        X.append(x[i : i + sequence_length, :])

    return np.array(X).reshape(-1, sequence_length, len(x_cols))

