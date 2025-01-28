import pandas as pd

def detect_anomalies(data: pd.DataFrame, column: str = "Quantity", method: str = "zscore", threshold: float = 3.0, multiplier: float = 1.5):
    """
    Detect anomalies using Z-Score or IQR methods.
    Args:
        data (pd.DataFrame): Input data.
        column (str): Column to analyze for anomalies.
        method (str): "zscore" or "iqr".
        threshold (float): Z-Score threshold (if method="zscore").
        multiplier (float): IQR multiplier (if method="iqr").
    """
    if data.empty or column not in data.columns:
        data["is_anomaly"] = False
        return data

    if method == "zscore":
        data["z_score"] = (data[column] - data[column].mean()) / data[column].std()
        data["is_anomaly"] = data["z_score"].abs() > threshold
        return data.drop(columns=["z_score"])

    elif method == "iqr":
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (multiplier * IQR)
        upper_bound = Q3 + (multiplier * IQR)
        data["is_anomaly"] = (data[column] < lower_bound) | (data[column] > upper_bound)
        return data
