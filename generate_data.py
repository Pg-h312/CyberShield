import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)
random.seed(42)

threat_types = [
    "Malware",
    "Phishing",
    "Ransomware",
    "DDoS",
    "Unauthorized Access",
    "Brute Force"
]

regions = [
    "North America",
    "Europe",
    "Asia",
    "South America",
    "Africa",
    "Oceania"
]

devices = [
    "Server",
    "Laptop",
    "Desktop",
    "Router",
    "Firewall"
]

rows = []

start_time = datetime.now() - timedelta(days=30)

for i in range(5000):

    timestamp = start_time + timedelta(
        minutes=i * 8
    )

    failed_logins = np.random.poisson(3)
    network_packets = np.random.randint(100, 1000)
    connections = np.random.randint(5, 100)
    port_scans = np.random.choice([0, 1], p=[0.95, 0.05])
    data_transfer = np.random.randint(10, 500)

    # Create some abnormal events
    if random.random() < 0.05:
        failed_logins = np.random.randint(30, 150)
        network_packets = np.random.randint(5000, 15000)
        connections = np.random.randint(300, 1000)
        port_scans = 1
        data_transfer = np.random.randint(700, 2000)

    rows.append({
        "event_id": f"EVT{i+1:06d}",
        "timestamp": timestamp,
        "threat_type": random.choice(threat_types),
        "region": random.choice(regions),
        "device_type": random.choice(devices),
        "failed_logins": failed_logins,
        "network_packets": network_packets,
        "connections": connections,
        "port_scans": port_scans,
        "data_transfer": data_transfer
    })

df = pd.DataFrame(rows)

df.to_csv(
    "data/security_events.csv",
    index=False
)

print("Security dataset created successfully.")
print(df.head())