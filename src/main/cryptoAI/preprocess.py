from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame

import pandas as pd
import numpy as np
import pickle

SCALER_PATH = "scaler/2024-03-01 22-33.pkl"

def preprocessing(sequence: DataFrame, sequence_length: int):
    x_cols = [0, 1, 2, 3, 4]

    x = sequence.iloc[:, x_cols].values
    scaler = __load_scaler()
    x = scaler.fit_transform(x)

    X = []
    for i in range(len(x) - sequence_length):
        X.append(x[i : i + sequence_length, :])

    return np.array(X).reshape(-1, sequence_length, len(x_cols))

def time_embedding_preprocessing(sequence: DataFrame, sequence_length: int):
    timestamps = sequence.index.values
    int_times = [pd.Timestamp(t).hour * 60 + pd.Timestamp(t).minute for t in timestamps]
    sin_times, cos_times = get_cyclical_seires(int_times)
    ohlcv_data = scaling_price_and_volume(sequence)

    time_embedded_data = np.concatenate([ohlcv_data, sin_times[:, None], cos_times[:, None]], axis=-1)
    print(time_embedded_data.shape)

    X = []
    for i in range(len(time_embedded_data) - sequence_length):
        X.append(time_embedded_data[i : i + sequence_length, :])

    return np.array(X).reshape(-1, sequence_length, 7)

def scaling_price_and_volume(sequence: DataFrame):
    price_scaler = __load_scaler_by_path("scaler/2024-03-14 18-00_price.pkl")
    volume_scaler = __load_scaler_by_path("scaler/2024-03-14 18-00_volume.pkl")

    prices = sequence.iloc[:, [0,1,2,3]]
    volumes = sequence.iloc[:, [4]]

    scaled_prices = price_scaler.transform(prices)
    scaled_volumes = volume_scaler.transform(volumes)
    
    return np.concatenate([scaled_prices, scaled_volumes], axis=-1)

def get_cyclical_seires(int_times):
    sins = []
    coss = []

    for time in int_times:
        sin, cos = encode_cyclical_time(time)
        sins.append(sin)
        coss.append(cos)
    
    return np.array(sins), np.array(coss)

def encode_cyclical_time(time, max_time = 1440):
    PI = np.pi
    sin = np.sin(2 * PI * time / max_time)
    cos = np.cos(2 * PI * time / max_time)
    return sin, cos

def __load_scaler_by_path(path):
    with open(path, "rb") as file:
        scaler = pickle.load(file)

    return scaler

def __load_scaler():
    with open(SCALER_PATH, "rb") as file:
        loaded_scaler = pickle.load(file)

    return loaded_scaler
