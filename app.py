import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from submodules.anomaly_detection import detect_anomalies
import plotly.express as px
import pandas as pd
import datetime

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    # Authentication
    authenticated = authenticate_user()
    if not authenticated:
        st.stop()

    if st.sidebar.button("Logout"):
        logout_user()
        st.stop()

    st.header("Importer Dashboard 360°")
    st.subheader("Upload Your Data")

    # File Upload
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # Load and preprocess data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded successfully!")
            st.write(data.head())

            # Filters
            st.sidebar.subheader("Filter Options")
            filtered_data = data.copy()

            # Multi-select Filters
            selected_states = st.sidebar.multiselect("Select States", ["All"] + sorted(data["State"].dropna().unique()))
            selected_exporters = st.sidebar.multiselect("Select Exporters", ["All"] + sorted(data["Exporter"].dropna().unique()))
            selected_consignees = st.sidebar.multiselect("Select Consignees", ["All"] + sorted(data["Consignee"].dropna().unique()))

            # Apply Filters
            if selected_states and "All" not in selected_states:
                filtered_data = filtered_data[filtered_data["State"].isin(selected_states)]
            if selected_exporters and "All" not in selected_exporters:
                filtered_data = filtered_data[filtered_data["Exporter"].isin(selected_exporters)]
            if selected_consignees and "All" not in selected_consignees:
                filtered_data = filtered_data[filtered_data["Consignee"].isin(selected_consignees)]

            # Display Filtered Data
            if filtered_data.empty:
                st.warning("No data matches the selected filters. Please adjust your filter options.")
            else:
                st.subheader("Filtered Data")
                st.write(filtered_data)

                # KPIs
                total_imports = filtered_data["Quantity"].sum() if "Quantity" in filtered_data.columns else 0
                unique_states = filtered_data["State"].nunique() if "State" in filtered_data.columns else 0

                col1, col2 = st.columns(2)
                col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
                col2.metric("States Involved", unique_states)

                # Quarterly Trends
                st.subheader("Quarterly Trends")
                if "Quarter" in filtered_data.columns and "Quantity" in filtered_data.columns:
                    quarter_trends = filtered_data.groupby("Quarter", as_index=False)["Quantity"].sum()
                    fig_quarter = px.bar(
                        quarter_trends,
                        x="Quarter",
                        y="Quantity",
                        title="Total Imports by Quarter",
                        labels={"Quarter": "Quarter", "Quantity": "Quantity (Kg)"}
                    )
                    st.plotly_chart(fig_quarter, use_container_width=True)

                # Anomaly Detection
                st.subheader("Anomaly Detection")
                anomalies = detect_anomalies(filtered_data, column="Quantity", method="iqr")
                st.write(anomalies[anomalies["is_anomaly"]])

                # Exporter Contributions
                exporter_contributions = filtered_data.groupby("Exporter", as_index=False)["Quantity"].sum()
                fig_exporter = px.bar(
                    exporter_contributions,
                    x="Exporter",
                    y="Quantity",
                    title="Exporter Contributions",
                    labels={"Quantity": "Total Imports (Kg)", "Exporter": "Exporter"},
                )
                st.plotly_chart(fig_exporter, use_container_width=True)

                # Consignee Contributions
                consignee_contributions = filtered_data.groupby("Consignee", as_index=False)["Quantity"].sum()
                fig_consignee = px.bar(
                    consignee_contributions,
                    x="Consignee",
                    y="Quantity",
                    title="Consignee Contributions",
                    labels={"Quantity": "Total Imports (Kg)", "Consignee": "Consignee"},
                )
                st.plotly_chart(fig_consignee, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link.")

if __name__ == "__main__":
    main()
