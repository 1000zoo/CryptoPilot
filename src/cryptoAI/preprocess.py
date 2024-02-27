from sklearn.preprocessing import MinMaxScaler
from pandas.core.frame import DataFrame

def preprocessing(sequence: DataFrame):
    x_cols = [0, 1, 2, 4]

    x = sequence.iloc[:, x_cols].values
    x = MinMaxScaler().fit_transform(x)

    return x

