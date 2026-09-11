# ============================================================
# CYBERSHIELD THREAT ANALYTICS
# Interactive ML Cybersecurity Monitoring Dashboard
# Streamlit + Pandas + NumPy + Scikit-learn + Plotly
# No Spark / No Databricks
# ============================================================

import os
import time
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CyberShield Threat Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# IMPORTANT:
# CSS is inside <style> and is NOT displayed as dashboard code.
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN APPLICATION ---------- */

    .stApp {
        background: #06111f;
        color: #eaf4ff;
    }

    .main .block-container {
        padding-top: 1.2rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 1700px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #071522;
        border-right: 1px solid #12365a;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.2rem;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #eaf4ff !important;
    }

    /* ---------- TEXT ---------- */

    h1, h2, h3, h4 {
        color: #f5f9ff !important;
    }

    p {
        color: #b9cce0;
    }

    /* ---------- SELECTBOX ---------- */

    div[data-baseweb="select"] > div {
        background: #081a2c !important;
        border: 1px solid #164d78 !important;
        border-radius: 8px !important;
        color: white !important;
    }

    div[data-baseweb="select"] span {
        color: #eaf4ff !important;
    }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        background: #0b74c9;
        color: white;
        border: 1px solid #178fe9;
        border-radius: 8px;
        min-height: 42px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: #108ee8;
        border-color: #2ba5ff;
    }

    /* ---------- DOWNLOAD BUTTON ---------- */

    .stDownloadButton > button {
        background: #087f72;
        color: white;
        border: 1px solid #10bca7;
        border-radius: 8px;
        font-weight: 600;
    }

    /* ---------- HEADER ---------- */

    .brand-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: white;
    }

    .brand-title span {
        color: #00d9ff;
    }

    .brand-subtitle {
        color: #86a7c7;
        font-size: 14px;
        margin-top: -5px;
    }

    .shield-icon {
        font-size: 38px;
        vertical-align: middle;
    }

    /* ---------- SECTION TITLE ---------- */

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #edf7ff;
        margin-bottom: 8px;
    }

    /* ---------- STATUS ---------- */

    .live-status {
        background: #0a2945;
        border: 1px solid #145787;
        border-radius: 9px;
        padding: 10px 16px;
        color: #27d9ff;
        font-weight: 600;
        text-align: center;
    }

    .live-dot {
        color: #00e5b0;
        font-size: 17px;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: linear-gradient(
            145deg,
            #0b2033,
            #071725
        );
        border: 1px solid #16486d;
        border-radius: 13px;
        padding: 18px;
        min-height: 145px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .kpi-label {
        color: #8eb1d1;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .kpi-value {
        color: white;
        font-size: 31px;
        font-weight: 800;
        margin-top: 8px;
    }

    .kpi-info {
        color: #00e5ad;
        font-size: 12px;
        margin-top: 5px;
    }

    .kpi-red {
        border-color: #8f244e;
    }

    .kpi-orange {
        border-color: #91551b;
    }

    .kpi-yellow {
        border-color: #826d18;
    }

    .kpi-green {
        border-color: #137c72;
    }

    .kpi-blue {
        border-color: #176aa3;
    }

    /* ---------- ALERT ---------- */

    .risk-alert {
        background: linear-gradient(
            90deg,
            #251522,
            #171421
        );
        border: 1px solid #9d3152;
        border-radius: 12px;
        padding: 16px 20px;
        color: #f7eaf0;
        margin-top: 8px;
        margin-bottom: 18px;
    }

    .risk-title {
        font-weight: 800;
        font-size: 17px;
        color: #ffcedc;
    }

    /* ---------- PAGE CARD ---------- */

    .page-card {
        background: #081827;
        border: 1px solid #153b5c;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
    }

    /* ---------- BADGES ---------- */

    .badge-high {
        background: #a51e3d;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }

    .badge-medium {
        background: #a36a15;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }

    .badge-low {
        background: #087d70;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
    }

    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: #081827;
        border: 1px solid #153b5c;
        padding: 14px;
        border-radius: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: #8eb1d1 !important;
    }

    [data-testid="stMetricValue"] {
        color: white !important;
    }

    /* ---------- DATAFRAME ---------- */

    [data-testid="stDataFrame"] {
        border: 1px solid #153b5c;
        border-radius: 10px;
    }

    /* ---------- DIVIDER ---------- */

    hr {
        border-color: #173a58 !important;
    }

    /* ---------- SIDEBAR RADIO ---------- */

    div[role="radiogroup"] label {
        background: transparent;
        border-radius: 7px;
        padding: 5px 7px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #6685a2;
        font-size: 12px;
        padding: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = os.path.join("data", "security_events.csv")
PREDICTED_FILE = os.path.join("data", "predicted_security_events.csv")

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "anomaly_model.pkl")
SCALER_FILE = os.path.join(MODEL_DIR, "scaler.pkl")

FEATURES = [
    "failed_logins",
    "network_packets",
    "connections",
    "port_scans",
    "data_transfer"
]

THREAT_TYPES = [
    "Malware",
    "Phishing",
    "Ransomware",
    "DDoS",
    "Unauthorized Access",
    "Brute Force"
]

REGIONS = [
    "North America",
    "Europe",
    "Asia",
    "South America",
    "Africa",
    "Oceania"
]

DEVICE_TYPES = [
    "Server",
    "Laptop",
    "Desktop",
    "Router",
    "Firewall"
]


# ============================================================
# GENERATE FALLBACK DATA
# ============================================================

def generate_demo_data(rows=5000):

    np.random.seed(42)

    now = datetime.now()

    timestamps = [
        now - timedelta(
            minutes=int(np.random.randint(0, 30 * 24 * 60))
        )
        for _ in range(rows)
    ]

    threat_type = np.random.choice(
        THREAT_TYPES,
        rows,
        p=[0.22, 0.18, 0.13, 0.12, 0.18, 0.17]
    )

    region = np.random.choice(
        REGIONS,
        rows,
        p=[0.38, 0.26, 0.20, 0.08, 0.05, 0.03]
    )

    device = np.random.choice(
        DEVICE_TYPES,
        rows,
        p=[0.28, 0.28, 0.18, 0.14, 0.12]
    )

    df = pd.DataFrame({
        "event_id": range(1, rows + 1),
        "timestamp": timestamps,
        "threat_type": threat_type,
        "region": region,
        "device_type": device,
        "source_ip": [
            f"{np.random.randint(10, 224)}."
            f"{np.random.randint(0, 255)}."
            f"{np.random.randint(0, 255)}."
            f"{np.random.randint(1, 254)}"
            for _ in range(rows)
        ],
        "failed_logins": np.random.poisson(4, rows),
        "network_packets": np.random.gamma(4, 850, rows),
        "connections": np.random.poisson(45, rows),
        "port_scans": np.random.poisson(3, rows),
        "data_transfer": np.random.gamma(3, 180, rows)
    })

    # Add abnormal events
    abnormal_count = int(rows * 0.06)

    abnormal_indices = np.random.choice(
        df.index,
        abnormal_count,
        replace=False
    )

    df.loc[abnormal_indices, "failed_logins"] = np.random.randint(
        30, 120, abnormal_count
    )

    df.loc[abnormal_indices, "network_packets"] = np.random.randint(
        5000, 25000, abnormal_count
    )

    df.loc[abnormal_indices, "connections"] = np.random.randint(
        150, 600, abnormal_count
    )

    df.loc[abnormal_indices, "port_scans"] = np.random.randint(
        20, 100, abnormal_count
    )

    df.loc[abnormal_indices, "data_transfer"] = np.random.randint(
        1000, 8000, abnormal_count
    )

    return df


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=60)
def load_data():

    os.makedirs("data", exist_ok=True)

    if os.path.exists(PREDICTED_FILE):

        try:
            df = pd.read_csv(PREDICTED_FILE)

            if len(df) > 0:
                return df

        except Exception:
            pass

    if os.path.exists(DATA_FILE):

        try:
            df = pd.read_csv(DATA_FILE)

            if len(df) > 0:
                return df

        except Exception:
            pass

    return generate_demo_data(5000)


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    df = df.copy()

    # Required columns
    defaults = {
        "event_id": range(1, len(df) + 1),
        "timestamp": datetime.now(),
        "threat_type": "Malware",
        "region": "North America",
        "device_type": "Server",
        "source_ip": "192.168.1.1",
        "failed_logins": 0,
        "network_packets": 0,
        "connections": 0,
        "port_scans": 0,
        "data_transfer": 0
    }

    for column, default in defaults.items():

        if column not in df.columns:

            if isinstance(default, range):

                df[column] = list(default)

            else:

                df[column] = default

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    df["timestamp"] = df["timestamp"].fillna(
        pd.Timestamp.now()
    )

    for feature in FEATURES:

        df[feature] = pd.to_numeric(
            df[feature],
            errors="coerce"
        ).fillna(0)

    return df


# ============================================================
# MACHINE LEARNING
# ============================================================

def train_model(df):

    os.makedirs(MODEL_DIR, exist_ok=True)

    scaler = StandardScaler()

    X = df[FEATURES].astype(float)

    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=200,
        contamination=0.05,
        random_state=42
    )

    model.fit(X_scaled)

    joblib.dump(model, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)

    return model, scaler


@st.cache_resource
def get_model():

    base_df = prepare_data(load_data())

    if os.path.exists(MODEL_FILE) and os.path.exists(SCALER_FILE):

        try:

            model = joblib.load(MODEL_FILE)
            scaler = joblib.load(SCALER_FILE)

            return model, scaler

        except Exception:
            pass

    return train_model(base_df)


def apply_ml(df):

    df = df.copy()

    model, scaler = get_model()

    X = df[FEATURES].astype(float)

    X_scaled = scaler.transform(X)

    predictions = model.predict(X_scaled)

    anomaly_values = model.decision_function(X_scaled)

    df["prediction"] = predictions

    # Convert anomaly score to 0-100 risk score
    minimum = anomaly_values.min()
    maximum = anomaly_values.max()

    if maximum - minimum == 0:

        df["risk_score"] = 50

    else:

        df["risk_score"] = (
            (maximum - anomaly_values)
            / (maximum - minimum)
            * 100
        )

    df["risk_score"] = df["risk_score"].clip(0, 100)

    def severity(score):

        if score >= 75:
            return "High"

        elif score >= 50:
            return "Medium"

        return "Low"

    df["severity"] = df["risk_score"].apply(severity)

    df["threat_detected"] = np.where(
        (predictions == -1) | (df["risk_score"] >= 50),
        "Detected",
        "Normal"
    )

    # Status
    if "status" not in df.columns:

        status_values = []

        for score in df["risk_score"]:

            if score >= 80:
                status_values.append(
                    np.random.choice(
                        ["Investigating", "Blocked"]
                    )
                )

            elif score >= 50:
                status_values.append(
                    np.random.choice(
                        ["Investigating", "Resolved"]
                    )
                )

            else:
                status_values.append(
                    np.random.choice(
                        ["Resolved", "Blocked"]
                    )
                )

        df["status"] = status_values

    return df


# ============================================================
# HEADER
# ============================================================

def show_header():

    col1, col2, col3 = st.columns(
        [5.5, 2, 2.5]
    )

    with col1:

        st.markdown(
            """
            <div class="brand-title">
                🛡️ Cyber<span>Shield</span>
            </div>
            <div class="brand-subtitle">
                ML Threat Analytics & Security Monitoring
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="live-status">
                <span class="live-dot">●</span>
                Live Monitoring
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div style="text-align:right;">
                <div style="color:#7896b3;font-size:12px;">
                    Last Updated
                </div>
                <div style="color:white;font-weight:600;">
                    {datetime.now().strftime("%b %d, %Y %H:%M:%S")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding:12px 0 18px;">
                <div style="font-size:46px;">🛡️</div>
                <div class="brand-title" style="font-size:25px;">
                    Cyber<span>Shield</span>
                </div>
                <div class="brand-subtitle">
                    ML Threat Analytics
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        st.markdown(
            "### NAVIGATION"
        )

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "🛡️ Threats",
                "⚠️ Incidents",
                "🖥️ Devices",
                "👤 Users",
                "🌐 Network",
                "📊 Reports",
                "⚙️ Settings"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            "### QUICK FILTERS"
        )

        quick_time = st.selectbox(
            "Time Range",
            [
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days",
                "Last 90 Days"
            ],
            index=2
        )

        quick_threat = st.selectbox(
            "Threat Type",
            ["All"] + THREAT_TYPES
        )

        quick_severity = st.selectbox(
            "Severity",
            ["All", "High", "Medium", "Low"]
        )

        quick_region = st.selectbox(
            "Region",
            ["All"] + REGIONS
        )

        quick_device = st.selectbox(
            "Device Type",
            ["All"] + DEVICE_TYPES
        )

        st.divider()

        live = st.toggle(
            "Live Monitoring",
            value=False
        )

        if live:

            refresh = st.slider(
                "Refresh seconds",
                min_value=5,
                max_value=60,
                value=15
            )

        else:

            refresh = 15

        st.divider()

        st.caption(
            "CyberShield v1.0"
        )

        st.caption(
            "Stay Safe. Stay Ahead."
        )

    return (
        page,
        quick_time,
        quick_threat,
        quick_severity,
        quick_region,
        quick_device,
        live,
        refresh
    )


# ============================================================
# FILTER DATA
# ============================================================

def filter_data(
    df,
    time_range,
    threat_type,
    severity,
    region,
    device_type
):

    filtered = df.copy()

    now = filtered["timestamp"].max()

    if time_range == "Last 24 Hours":

        start = now - pd.Timedelta(hours=24)

    elif time_range == "Last 7 Days":

        start = now - pd.Timedelta(days=7)

    elif time_range == "Last 30 Days":

        start = now - pd.Timedelta(days=30)

    else:

        start = now - pd.Timedelta(days=90)

    filtered = filtered[
        filtered["timestamp"] >= start
    ]

    if threat_type != "All":

        filtered = filtered[
            filtered["threat_type"] == threat_type
        ]

    if severity != "All":

        filtered = filtered[
            filtered["severity"] == severity
        ]

    if region != "All":

        filtered = filtered[
            filtered["region"] == region
        ]

    if device_type != "All":

        filtered = filtered[
            filtered["device_type"] == device_type
        ]

    return filtered


# ============================================================
# KPI CARD
# ============================================================

def kpi_card(
    label,
    value,
    info,
    css_class
):

    st.markdown(
        f"""
        <div class="kpi-card {css_class}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value:,}</div>
            <div class="kpi-info">{info}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD PAGE
# ============================================================

def dashboard_page(df):

    st.markdown(
        "## Security Dashboard"
    )

    st.caption(
        "Machine learning powered cybersecurity monitoring"
    )

    # ---------------------------------------------
    # GLOBAL FILTERS
    # ---------------------------------------------

    st.markdown(
        "### Global Filters"
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:

        time_range = st.selectbox(
            "📅 Time Range",
            [
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days",
                "Last 90 Days"
            ],
            index=2,
            key="dashboard_time"
        )

    with f2:

        threat_type = st.selectbox(
            "🛡️ Threat Type",
            ["All"] + THREAT_TYPES,
            key="dashboard_threat"
        )

    with f3:

        severity = st.selectbox(
            "⚠️ Severity",
            ["All", "High", "Medium", "Low"],
            key="dashboard_severity"
        )

    with f4:

        region = st.selectbox(
            "🌐 Region",
            ["All"] + REGIONS,
            key="dashboard_region"
        )

    with f5:

        device = st.selectbox(
            "🖥️ Device Type",
            ["All"] + DEVICE_TYPES,
            key="dashboard_device"
        )

    filtered = filter_data(
        df,
        time_range,
        threat_type,
        severity,
        region,
        device
    )

    # ---------------------------------------------
    # KPIs
    # ---------------------------------------------

    total = len(filtered)

    high = len(
        filtered[
            filtered["severity"] == "High"
        ]
    )

    medium = len(
        filtered[
            filtered["severity"] == "Medium"
        ]
    )

    low = len(
        filtered[
            filtered["severity"] == "Low"
        ]
    )

    resolved = len(
        filtered[
            filtered["status"].isin(
                ["Resolved", "Blocked"]
            )
        ]
    )

    st.markdown("### Security Overview")

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        kpi_card(
            "Total Threats",
            total,
            "ML analyzed",
            "kpi-red"
        )

    with k2:
        kpi_card(
            "High Severity",
            high,
            "Requires attention",
            "kpi-orange"
        )

    with k3:
        kpi_card(
            "Medium Severity",
            medium,
            "Under monitoring",
            "kpi-yellow"
        )

    with k4:
        kpi_card(
            "Low Severity",
            low,
            "Low risk events",
            "kpi-green"
        )

    with k5:
        kpi_card(
            "Resolved Threats",
            resolved,
            "Protected",
            "kpi-blue"
        )

    st.write("")

    # ---------------------------------------------
    # HIGH RISK ALERT
    # ---------------------------------------------

    if len(filtered) > 0:

        highest = filtered.sort_values(
            "risk_score",
            ascending=False
        ).iloc[0]

        st.markdown(
            f"""
            <div class="risk-alert">
                <div class="risk-title">
                    🚨 HIGH RISK THREAT DETECTED
                </div>
                <br>
                Threat:
                <b>{highest["threat_type"]}</b>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Region:
                <b>{highest["region"]}</b>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Device:
                <b>{highest["device_type"]}</b>
                &nbsp;&nbsp;|&nbsp;&nbsp;
                Risk Score:
                <b>{highest["risk_score"]:.0f}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------
    # CHART ROW 1
    # ---------------------------------------------

    c1, c2 = st.columns([1.25, 1])

    with c1:

        st.markdown(
            "### 📈 Threat Trends"
        )

        trend = (
            filtered
            .assign(
                date=filtered["timestamp"].dt.date
            )
            .groupby(
                ["date", "severity"]
            )
            .size()
            .reset_index(name="count")
        )

        if len(trend) > 0:

            fig = px.line(
                trend,
                x="date",
                y="count",
                color="severity",
                markers=True,
                color_discrete_map={
                    "High": "#ff426d",
                    "Medium": "#ffb42b",
                    "Low": "#10d7b1"
                }
            )

            fig.update_layout(
                height=350,
                template="plotly_dark",
                paper_bgcolor="#081827",
                plot_bgcolor="#081827",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),
                legend_title_text=""
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No data available for the selected filters."
            )

    with c2:

        st.markdown(
            "### 🍩 Threats by Type"
        )

        type_data = (
            filtered["threat_type"]
            .value_counts()
            .reset_index()
        )

        type_data.columns = [
            "Threat Type",
            "Count"
        ]

        if len(type_data) > 0:

            fig = px.pie(
                type_data,
                names="Threat Type",
                values="Count",
                hole=0.62
            )

            fig.update_layout(
                height=350,
                template="plotly_dark",
                paper_bgcolor="#081827",
                plot_bgcolor="#081827",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),
                legend_title_text=""
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No threat type data available."
            )

    # ---------------------------------------------
    # CHART ROW 2
    # ---------------------------------------------

    c3, c4 = st.columns([1, 1])

    with c3:

        st.markdown(
            "### 🌍 Threats by Region"
        )

        region_data = (
            filtered["region"]
            .value_counts()
            .reset_index()
        )

        region_data.columns = [
            "Region",
            "Count"
        ]

        if len(region_data) > 0:

            region_data = region_data.sort_values(
                "Count",
                ascending=True
            )

            fig = px.bar(
                region_data,
                x="Count",
                y="Region",
                orientation="h",
                text="Count"
            )

            fig.update_traces(
                marker_color="#168de2"
            )

            fig.update_layout(
                height=350,
                template="plotly_dark",
                paper_bgcolor="#081827",
                plot_bgcolor="#081827",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with c4:

        st.markdown(
            "### 🎯 Top Attack Sources"
        )

        source_data = (
            filtered["source_ip"]
            .value_counts()
            .head(8)
            .reset_index()
        )

        source_data.columns = [
            "Source IP",
            "Events"
        ]

        if len(source_data) > 0:

            fig = px.bar(
                source_data.sort_values(
                    "Events",
                    ascending=True
                ),
                x="Events",
                y="Source IP",
                orientation="h",
                text="Events"
            )

            fig.update_traces(
                marker_color="#7b5cff"
            )

            fig.update_layout(
                height=350,
                template="plotly_dark",
                paper_bgcolor="#081827",
                plot_bgcolor="#081827",
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # ---------------------------------------------
    # RECENT EVENTS + SECURITY POSTURE
    # ---------------------------------------------

    c5, c6 = st.columns([1.65, 1])

    with c5:

        st.markdown(
            "### 🛡️ Recent Security Events"
        )

        recent = (
            filtered
            .sort_values(
                "timestamp",
                ascending=False
            )
            .head(10)
            .copy()
        )

        if len(recent) > 0:

            display = recent[
                [
                    "timestamp",
                    "threat_type",
                    "severity",
                    "source_ip",
                    "region",
                    "status"
                ]
            ].copy()

            display["timestamp"] = display[
                "timestamp"
            ].dt.strftime(
                "%b %d, %H:%M:%S"
            )

            display.columns = [
                "Time",
                "Threat Type",
                "Severity",
                "Source",
                "Region",
                "Status"
            ]

            st.dataframe(
                display,
                use_container_width=True,
                hide_index=True
            )

    with c6:

        st.markdown(
            "### 🛡️ Security Posture"
        )

        if len(filtered) > 0:

            posture = int(
                max(
                    0,
                    min(
                        100,
                        100 - (
                            filtered["risk_score"]
                            .mean() * 0.35
                        )
                    )
                )
            )

        else:

            posture = 0

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=posture,
                number={
                    "suffix": "%",
                    "font": {
                        "size": 38,
                        "color": "white"
                    }
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#16d7c3"
                    },
                    "bgcolor": "#10283f",
                    "borderwidth": 0,
                    "steps": [
                        {
                            "range": [0, 40],
                            "color": "#3b1d2b"
                        },
                        {
                            "range": [40, 70],
                            "color": "#3c3219"
                        },
                        {
                            "range": [70, 100],
                            "color": "#123b3a"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            height=280,
            template="plotly_dark",
            paper_bgcolor="#081827",
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        checks = [
            "Firewall Protection",
            "Endpoint Security",
            "Email Security",
            "Data Encryption",
            "Access Control"
        ]

        for check in checks:

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:4px 0;
                    color:#bcd1e4;
                ">
                    <span>✓ {check}</span>
                    <span style="color:#00e5ad;">
                        Active
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# THREATS PAGE
# ============================================================

def threats_page(df):

    st.title("🛡️ Threat Intelligence")

    st.caption(
        "Machine learning detected and analyzed security threats."
    )

    high = df[
        df["severity"] == "High"
    ]

    medium = df[
        df["severity"] == "Medium"
    ]

    low = df[
        df["severity"] == "Low"
    ]

    a, b, c, d = st.columns(4)

    with a:
        st.metric(
            "Total Events",
            f"{len(df):,}"
        )

    with b:
        st.metric(
            "High Risk",
            f"{len(high):,}"
        )

    with c:
        st.metric(
            "Medium Risk",
            f"{len(medium):,}"
        )

    with d:
        st.metric(
            "Low Risk",
            f"{len(low):,}"
        )

    st.divider()

    search = st.text_input(
        "🔎 Search Threats",
        placeholder="Search threat type, IP, region..."
    )

    display = df.copy()

    if search:

        search_lower = search.lower()

        mask = (
            display["threat_type"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
            |
            display["source_ip"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
            |
            display["region"]
            .astype(str)
            .str.lower()
            .str.contains(search_lower)
        )

        display = display[mask]

    display = display.sort_values(
        "risk_score",
        ascending=False
    )

    columns = [
        "timestamp",
        "threat_type",
        "severity",
        "risk_score",
        "source_ip",
        "region",
        "device_type",
        "threat_detected",
        "status"
    ]

    st.dataframe(
        display[columns].head(200),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# INCIDENTS PAGE
# ============================================================

def incidents_page(df):

    st.title("⚠️ Security Incidents")

    st.caption(
        "Investigate and manage high-risk security incidents."
    )

    incidents = df[
        df["risk_score"] >= 50
    ].copy()

    i1, i2, i3 = st.columns(3)

    with i1:

        st.metric(
            "Open Incidents",
            len(
                incidents[
                    incidents["status"]
                    == "Investigating"
                ]
            )
        )

    with i2:

        st.metric(
            "Blocked",
            len(
                incidents[
                    incidents["status"]
                    == "Blocked"
                ]
            )
        )

    with i3:

        st.metric(
            "Resolved",
            len(
                incidents[
                    incidents["status"]
                    == "Resolved"
                ]
            )
        )

    st.divider()

    incident_view = incidents[
        [
            "event_id",
            "timestamp",
            "threat_type",
            "severity",
            "risk_score",
            "region",
            "device_type",
            "source_ip",
            "status"
        ]
    ].sort_values(
        "risk_score",
        ascending=False
    )

    st.dataframe(
        incident_view.head(200),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# DEVICES PAGE
# ============================================================

def devices_page(df):

    st.title("🖥️ Device Security")

    st.caption(
        "Monitor devices and identify abnormal activity."
    )

    device_summary = (
        df.groupby("device_type")
        .agg(
            Events=("event_id", "count"),
            Average_Risk=("risk_score", "mean"),
            High_Risk=(
                "severity",
                lambda x: (x == "High").sum()
            )
        )
        .reset_index()
    )

    device_summary["Average_Risk"] = (
        device_summary["Average_Risk"]
        .round(1)
    )

    st.dataframe(
        device_summary,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    fig = px.bar(
        device_summary,
        x="device_type",
        y="Events",
        color="Average_Risk",
        text="Events"
    )

    fig.update_layout(
        height=420,
        template="plotly_dark",
        paper_bgcolor="#081827",
        plot_bgcolor="#081827"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# USERS PAGE
# ============================================================

def users_page(df):

    st.title("👤 User Security")

    st.caption(
        "User activity and authentication threat monitoring."
    )

    total_logins = int(
        df["failed_logins"].sum()
    )

    suspicious = len(
        df[
            df["failed_logins"] >= 20
        ]
    )

    avg_login_failures = round(
        df["failed_logins"].mean(),
        2
    )

    a, b, c = st.columns(3)

    with a:
        st.metric(
            "Authentication Events",
            f"{total_logins:,}"
        )

    with b:
        st.metric(
            "Suspicious Users",
            f"{suspicious:,}"
        )

    with c:
        st.metric(
            "Avg Failed Logins",
            avg_login_failures
        )

    st.divider()

    user_activity = (
        df.groupby("source_ip")
        .agg(
            Failed_Logins=(
                "failed_logins",
                "sum"
            ),
            Connections=(
                "connections",
                "sum"
            ),
            Events=(
                "event_id",
                "count"
            )
        )
        .reset_index()
        .sort_values(
            "Failed_Logins",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        user_activity,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# NETWORK PAGE
# ============================================================

def network_page(df):

    st.title("🌐 Network Monitoring")

    st.caption(
        "Network traffic, connections and port scanning analytics."
    )

    a, b, c, d = st.columns(4)

    with a:

        st.metric(
            "Network Packets",
            f"{int(df['network_packets'].sum()):,}"
        )

    with b:

        st.metric(
            "Connections",
            f"{int(df['connections'].sum()):,}"
        )

    with c:

        st.metric(
            "Port Scans",
            f"{int(df['port_scans'].sum()):,}"
        )

    with d:

        st.metric(
            "Data Transfer",
            f"{int(df['data_transfer'].sum()):,}"
        )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        network_daily = (
            df.assign(
                date=df["timestamp"].dt.date
            )
            .groupby("date")
            .agg(
                packets=(
                    "network_packets",
                    "sum"
                ),
                connections=(
                    "connections",
                    "sum"
                )
            )
            .reset_index()
        )

        fig = px.line(
            network_daily,
            x="date",
            y=["packets", "connections"],
            markers=True
        )

        fig.update_layout(
            title="Network Traffic Trend",
            template="plotly_dark",
            paper_bgcolor="#081827",
            plot_bgcolor="#081827",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        port_data = (
            df.groupby("threat_type")
            ["port_scans"]
            .sum()
            .reset_index()
            .sort_values(
                "port_scans",
                ascending=False
            )
        )

        fig = px.bar(
            port_data,
            x="threat_type",
            y="port_scans",
            text="port_scans"
        )

        fig.update_layout(
            title="Port Scans by Threat",
            template="plotly_dark",
            paper_bgcolor="#081827",
            plot_bgcolor="#081827",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# REPORTS PAGE
# ============================================================

def reports_page(df):

    st.title("📊 Security Reports")

    st.caption(
        "Generate and download cybersecurity analytics reports."
    )

    report_type = st.selectbox(
        "Report Type",
        [
            "Complete Security Report",
            "High Risk Threats",
            "Incident Report",
            "Network Report"
        ]
    )

    if report_type == "Complete Security Report":

        report = df.copy()

    elif report_type == "High Risk Threats":

        report = df[
            df["severity"] == "High"
        ].copy()

    elif report_type == "Incident Report":

        report = df[
            df["risk_score"] >= 50
        ].copy()

    else:

        report = df[
            [
                "timestamp",
                "source_ip",
                "network_packets",
                "connections",
                "port_scans",
                "data_transfer",
                "threat_type",
                "risk_score"
            ]
        ].copy()

    st.metric(
        "Records in Report",
        f"{len(report):,}"
    )

    st.dataframe(
        report.head(100),
        use_container_width=True,
        hide_index=True
    )

    csv_data = report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download CSV Report",
        data=csv_data,
        file_name=(
            "cybershield_security_report.csv"
        ),
        mime="text/csv"
    )


# ============================================================
# SETTINGS PAGE
# ============================================================

def settings_page(df):

    st.title("⚙️ CyberShield Settings")

    st.caption(
        "Configure monitoring and machine learning options."
    )

    st.subheader(
        "Machine Learning Engine"
    )

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            "ML Engine: Isolation Forest"
        )

        st.write(
            "Algorithm: Isolation Forest"
        )

        st.write(
            "Features:"
        )

        for feature in FEATURES:

            st.write(
                f"• {feature}"
            )

    with c2:

        sensitivity = st.slider(
            "Threat Sensitivity",
            min_value=1,
            max_value=100,
            value=75
        )

        st.write(
            f"Current sensitivity: {sensitivity}%"
        )

        notifications = st.toggle(
            "Enable Security Notifications",
            value=True
        )

        auto_block = st.toggle(
            "Automatic High-Risk Blocking",
            value=False
        )

        if notifications:

            st.success(
                "Security notifications are enabled."
            )

        if auto_block:

            st.warning(
                "Automatic blocking is enabled."
            )

    st.divider()

    st.subheader(
        "System Information"
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        st.metric(
            "Events Loaded",
            f"{len(df):,}"
        )

    with s2:

        st.metric(
            "ML Features",
            len(FEATURES)
        )

    with s3:

        st.metric(
            "Threat Categories",
            len(THREAT_TYPES)
        )

    st.divider()

    if st.button(
        "🔄 Retrain ML Model"
    ):

        with st.spinner(
            "Training Isolation Forest model..."
        ):

            train_model(df)

            get_model.clear()

        st.success(
            "ML model retrained successfully."
        )

        st.rerun()


# ============================================================
# APPLICATION
# ============================================================

def main():

    # Load data
    raw_df = load_data()

    # Prepare
    raw_df = prepare_data(raw_df)

    # ML
    df = apply_ml(raw_df)

    # Sidebar
    (
        page,
        quick_time,
        quick_threat,
        quick_severity,
        quick_region,
        quick_device,
        live,
        refresh
    ) = sidebar()

    # Header
    show_header()

    # --------------------------------------------------------
    # PAGE ROUTING
    # --------------------------------------------------------

    if page == "🏠 Dashboard":

        dashboard_page(df)

    elif page == "🛡️ Threats":

        threats_page(df)

    elif page == "⚠️ Incidents":

        incidents_page(df)

    elif page == "🖥️ Devices":

        devices_page(df)

    elif page == "👤 Users":

        users_page(df)

    elif page == "🌐 Network":

        network_page(df)

    elif page == "📊 Reports":

        reports_page(df)

    elif page == "⚙️ Settings":

        settings_page(df)

    # Footer
    st.markdown(
        """
        <div class="footer">
            CyberShield Threat Analytics |
            Machine Learning Security Monitoring |
            Protected by Intelligent Threat Detection
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # OPTIONAL LIVE REFRESH
    # --------------------------------------------------------

    if live:

        time.sleep(refresh)

        st.rerun()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    main()