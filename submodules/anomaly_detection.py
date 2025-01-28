# importer_dashboard/submodules/anomaly_detection.py

import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(data: pd.DataFrame, contamination: float = 0.05):
    if data.empty or "Quantity" not in data.columns:
        data["is_anomaly"] = False
        return data

    model = IsolationForest(contamination=contamination, random_state=42)
    data["is_anomaly"] = model.fit_predict(data[["Quantity"]]) == -1
    return data
