from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame
import numpy as np
import pickle

SCALER_PATH = "scaler/2024-03-01 22-33.pkl"

def preprocessing(sequence: DataFrame, sequence_length: int):
    x_cols = [0, 1, 2, 3, 4]

    x = sequence.iloc[:, x_cols].values
    scaler = __load_scaler()
    x = scaler.fit_transform(x)

    X = []
    for i in range(len(x) - sequence_length + 1):
        X.append(x[i : i + sequence_length, :])

    return np.array(X).reshape(-1, sequence_length, len(x_cols))


def __load_scaler():
    with open(SCALER_PATH, "rb") as file:
        loaded_scaler = pickle.load(file)

    return loaded_scaler
