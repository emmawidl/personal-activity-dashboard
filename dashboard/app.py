import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="ACL Recovery Dashboard", layout="centered")

# --- Title ---
st.title("🏃‍♀️ Personal Activity Tracker + ACL Recovery Dashboard")


# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("mock_data/synthetic_health_data.csv", parse_dates=["date"])
    return df


df = load_data()

# --- Injury Marker ---
injury_date = pd.to_datetime("2025-04-01")

# --- Sidebar Filters ---
st.sidebar.header("📅 Date Range")
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Select range:", [min_date, max_date], min_value=min_date, max_value=max_date
)

filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date))
    & (df["date"] <= pd.to_datetime(end_date))
]

# --- Metric Selection ---
st.sidebar.header("📈 Metric")
metric = st.sidebar.selectbox(
    "Choose a metric to visualize:", ["steps", "heart_rate_avg", "sleep_hours"]
)

# --- Rolling Average Option ---
add_rolling = st.sidebar.checkbox("Show 7-day rolling average")

# --- Plotly Chart ---
fig = px.line(
    filtered_df,
    x="date",
    y=metric,
    title=f"📊 {metric.replace('_', ' ').title()} Over Time",
    markers=True,
)

# Injury date vertical line
fig.add_vline(x=injury_date, line_dash="dash", line_color="red")
fig.add_annotation(
    x=injury_date,
    y=filtered_df[metric].max(),
    text="🩼 Injury",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40,
)

# Optional rolling average
if add_rolling:
    filtered_df["rolling_avg"] = filtered_df[metric].rolling(window=7).mean()
    fig.add_scatter(
        x=filtered_df["date"],
        y=filtered_df["rolling_avg"],
        mode="lines",
        name="7-Day Avg",
        line=dict(dash="dot"),
    )

# Layout tweaks
fig.update_layout(
    xaxis_title="Date",
    yaxis_title=metric.replace("_", " ").title(),
    legend_title="Legend",
    template="simple_white",
    margin=dict(l=40, r=40, t=60, b=40),
)

# --- Render Chart ---
st.plotly_chart(fig, use_container_width=True)

# --- Show Raw Data ---
if st.checkbox("📄 Show Raw Data"):
    st.dataframe(filtered_df)
