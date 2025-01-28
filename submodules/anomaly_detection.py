# importer_dashboard/submodules/anomaly_detection.py

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies(data: pd.DataFrame, quantity_col: str = "Quantity", contamination: float = 0.05):
    """
    Use IsolationForest to detect anomalies in the Quantity column.
    Returns a DataFrame with an additional boolean column 'is_anomaly'.
    """
    if data.empty or quantity_col not in data.columns:
        data["is_anomaly"] = False
        return data

    # Prepare the data for the model
    X = data[[quantity_col]].values

    # Create and fit the model
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X)

    # Predict: -1 = outlier, 1 = inlier
    preds = model.predict(X)

    data["is_anomaly"] = [True if p == -1 else False for p in preds]
    return data
