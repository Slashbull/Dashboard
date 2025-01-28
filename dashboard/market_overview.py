import streamlit as st
from submodules.key_metrics import calculate_kpis
from submodules.state_visuals import generate_state_heatmap, generate_state_bar_chart
from submodules.anomaly_detection import detect_anomalies
import plotly.express as px

def market_overview(data):
    st.header("Market Overview Dashboard")

    if data.empty:
        st.warning("No data available. Please upload a dataset to continue.")
        return

    # Display KPIs
    st.subheader("Key Performance Indicators (KPIs)")
    total_imports, unique_states, yoy_growth, mom_growth = calculate_kpis(data)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
    col2.metric("States Involved", unique_states)
    col3.metric("YoY Growth (%)", f"{yoy_growth:.2f}")
    col4.metric("MoM Growth (%)", f"{mom_growth:.2f}")

    # Quarterly Trends
    st.subheader("Quarterly Trends")
    quarter_trends = data.groupby("Quarter", as_index=False)["Quantity"].sum()
    fig_quarter = px.bar(
        quarter_trends,
        x="Quarter",
        y="Quantity",
        title="Total Imports by Quarter",
        labels={"Quarter": "Quarter", "Quantity": "Quantity (Kg)"}
    )
    st.plotly_chart(fig_quarter, use_container_width=True)

    # State Visualizations
    st.subheader("State-Level Contributions")
    generate_state_bar_chart(data)
    generate_state_heatmap(data)
