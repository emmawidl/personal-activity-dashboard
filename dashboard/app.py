import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Recovery Dashboard", layout="centered")

# Title
st.title("🏃‍♀️ Personal Activity Tracker + ACL Recovery Dashboard")


# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("mock_data/synthetic_health_data.csv", parse_dates=["date"])
    return df


df = load_data()

# Injury marker
injury_date = pd.to_datetime("2025-04-01")

# Sidebar filters
st.sidebar.header("📅 Date Range")
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Select range:", [min_date, max_date], min_value=min_date, max_value=max_date
)

# Filtered data
filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date))
    & (df["date"] <= pd.to_datetime(end_date))
]

# Line chart: Steps over time
fig = px.line(filtered_df, x="date", y="steps", title="🦶 Daily Steps Over Time")
fig.add_vline(x=injury_date, line_dash="dash", line_color="red")
fig.update_layout(xaxis_title="Date", yaxis_title="Steps", showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# Optional: Add note
st.markdown(f"**Red dashed line** indicates injury date: `{injury_date.date()}`")

# Show raw data (optional toggle)
if st.checkbox("Show raw data"):
    st.dataframe(filtered_df)
