import pandas as pd
import numpy as np
import os

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

os.makedirs("models", exist_ok=True)

df = pd.read_csv("data/security_events.csv")

features = [
    "failed_logins",
    "network_packets",
    "connections",
    "port_scans",
    "data_transfer"
]

X = df[features]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    n_estimators=200,
    contamination=0.05,
    random_state=42
)

model.fit(X_scaled)

df["prediction"] = model.predict(X_scaled)

df["anomaly_score"] = -model.decision_function(X_scaled)

# Convert anomaly score into risk score
minimum = df["anomaly_score"].min()
maximum = df["anomaly_score"].max()

df["risk_score"] = (
    (df["anomaly_score"] - minimum)
    / (maximum - minimum)
    * 100
)

df["risk_score"] = df["risk_score"].clip(0, 100)

def severity(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"

df["severity"] = df["risk_score"].apply(severity)

df["threat_detected"] = np.where(
    df["prediction"] == -1,
    "Suspicious",
    "Normal"
)

joblib.dump(
    model,
    "models/anomaly_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

df.to_csv(
    "data/predicted_security_events.csv",
    index=False
)

print("Machine Learning model trained successfully.")
print(df["severity"].value_counts())