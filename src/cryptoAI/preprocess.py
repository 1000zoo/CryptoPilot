from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame
import numpy as np

def preprocessing(sequence: DataFrame):
    x_cols = [0, 1, 2, 4]

    x = sequence.iloc[:, x_cols].values
    x = MinMaxScaler().fit_transform(x)

    X = []
    for i in range(len(x) - 5 + 1):
        X.append(x[i : i + 5, :])

    return np.array(X).reshape(-1, 5, 4)

