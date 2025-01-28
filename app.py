# importer_dashboard/app.py

import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from submodules.anomaly_detection import detect_anomalies
import plotly.express as px

import sys

st.write("Python executable being used:", sys.executable)
st.write("Python version:", sys.version)

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    # 1. Authentication
    authenticated = authenticate_user()
    if not authenticated:
        st.stop()

    if st.sidebar.button("Logout"):
        logout_user()
        st.stop()

    st.header("Importer Dashboard 360°")
    st.subheader("Upload Your Data")

    # 2. Data Upload
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # 3. Load and Preprocess Data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded successfully!")
            st.subheader("Dataset Preview")
            st.write(data.head())

            # 4. Sidebar Filters
            st.sidebar.subheader("Filter Options")
            filters = {}
            for column in ["State", "Month", "Year", "Consignee", "Exporter"]:
                if column in data.columns:
                    options = ["All"] + sorted(data[column].unique())
                    filters[column] = st.sidebar.selectbox(f"Select {column}", options)
                else:
                    filters[column] = "All"

            # Apply Filters
            filtered_data = data.copy()
            for column, value in filters.items():
                if value != "All":
                    filtered_data = filtered_data[filtered_data[column] == value]

            # 5. Display Filtered Data
            st.subheader("Filtered Data")
            st.write(filtered_data)

            # 6. KPI Metrics
            total_imports = filtered_data["Quantity"].sum() if "Quantity" in filtered_data.columns else 0
            unique_states = filtered_data["State"].nunique() if "State" in filtered_data.columns else 0

            col1, col2 = st.columns(2)
            col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
            col2.metric("States Involved", unique_states)

            # 7. Optional: Anomaly Detection
            st.subheader("Anomaly Detection")
            if st.checkbox("Run Anomaly Detection"):
                anomalies = detect_anomalies(filtered_data)
                st.write(anomalies[anomalies["is_anomaly"]])

                # Anomaly Chart
                if "Month" in anomalies.columns and "Quantity" in anomalies.columns:
                    fig = px.scatter(
                        anomalies, 
                        x="Month", 
                        y="Quantity", 
                        color="is_anomaly", 
                        title="Quantity by Month with Anomalies Highlighted"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # 8. Visualization: Bar Chart
            st.subheader("Total Imports by State")
            if "State" in filtered_data.columns and "Quantity" in filtered_data.columns:
                state_sums = filtered_data.groupby("State", as_index=False)["Quantity"].sum()
                fig_bar = px.bar(
                    state_sums, 
                    x="State", 
                    y="Quantity", 
                    title="Total Imports by State",
                    labels={"State": "State", "Quantity": "Quantity (Kg)"}
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link.")

if __name__ == "__main__":
    main()
