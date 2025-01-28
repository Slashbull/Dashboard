# importer_dashboard/app.py

import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from submodules.anomaly_detection import detect_anomalies

import plotly.express as px

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    # 1. Authentication
    authenticated = authenticate_user()
    if not authenticated:
        st.stop()  # Stop the app if user is not authenticated

    # 2. Logout button
    if st.sidebar.button("Logout"):
        logout_user()
        st.stop()

    # 3. Page Header
    st.header("Importer Dashboard 360°")
    st.write("Upload your data (CSV/Excel or Google Sheet link). Then apply filters and explore the dashboard.")

    # 4. Data Upload
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # 5. Load & Preprocess Data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded and preprocessed successfully!")

            # 6. Preview Data
            st.subheader("Data Preview")
            st.write(data.head())

            # 7. Sidebar Filters
            st.sidebar.subheader("Filter Options")

            # State filter
            if "State" in data.columns:
                unique_states = ["All"] + sorted(data["State"].unique())
                selected_state = st.sidebar.selectbox("Select State", unique_states)
            else:
                selected_state = "All"

            # Month filter
            if "Month" in data.columns:
                unique_months = ["All"] + sorted(data["Month"].unique())
                selected_month = st.sidebar.selectbox("Select Month", unique_months)
            else:
                selected_month = "All"

            # Year filter
            if "Year" in data.columns:
                unique_years = ["All"] + sorted(data["Year"].unique())
                selected_year = st.sidebar.selectbox("Select Year", unique_years)
            else:
                selected_year = "All"

            # Consignee filter
            if "Consignee" in data.columns:
                unique_consignees = ["All"] + sorted(data["Consignee"].unique())
                selected_consignee = st.sidebar.selectbox("Select Consignee", unique_consignees)
            else:
                selected_consignee = "All"

            # Exporter filter
            if "Exporter" in data.columns:
                unique_exporters = ["All"] + sorted(data["Exporter"].unique())
                selected_exporter = st.sidebar.selectbox("Select Exporter", unique_exporters)
            else:
                selected_exporter = "All"

            # 8. Apply Filters
            filtered_data = data.copy()

            if selected_state != "All" and "State" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["State"] == selected_state]

            if selected_month != "All" and "Month" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["Month"] == selected_month]

            if selected_year != "All" and "Year" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["Year"] == selected_year]

            if selected_consignee != "All" and "Consignee" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["Consignee"] == selected_consignee]

            if selected_exporter != "All" and "Exporter" in filtered_data.columns:
                filtered_data = filtered_data[filtered_data["Exporter"] == selected_exporter]

            # 9. Display Filtered Data
            st.subheader("Filtered Data")
            st.write(filtered_data)

            # 10. KPI Metrics
            if "Quantity" in filtered_data.columns:
                total_imports = filtered_data["Quantity"].sum()
            else:
                total_imports = 0

            if "State" in filtered_data.columns:
                unique_states_count = filtered_data["State"].nunique()
            else:
                unique_states_count = 0

            col1, col2 = st.columns(2)
            col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
            col2.metric("States Involved", unique_states_count)

            # 11. Optional: Anomaly Detection
            st.subheader("Anomaly Detection (Optional)")
            run_anomaly = st.checkbox("Run Anomaly Detection on Quantity")
            if run_anomaly:
                data_with_anomalies = detect_anomalies(filtered_data.copy())
                anomalies = data_with_anomalies[data_with_anomalies["is_anomaly"] == True]
                if not anomalies.empty:
                    st.warning(f"Detected {len(anomalies)} anomalies!")
                    st.write(anomalies)
                else:
                    st.success("No anomalies detected.")

                # 12. Example Plot with anomalies highlighted
                if "Month" in data_with_anomalies.columns and "Quantity" in data_with_anomalies.columns:
                    # Convert Month to numeric for plotting
                    month_map = {
                        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                        "Jul": 7, "Aug": 8, "Sep": 9, "Sept": 9, "Oct": 10, "Nov": 11, "Dec": 12
                    }
                    data_with_anomalies["Month_Num"] = data_with_anomalies["Month"].map(month_map)
                    data_with_anomalies.sort_values(by="Month_Num", inplace=True)

                    fig_anomaly = px.scatter(
                        data_with_anomalies,
                        x="Month_Num",
                        y="Quantity",
                        color="is_anomaly",
                        title="Month vs. Quantity (Anomalies Highlighted)",
                        labels={"Month_Num": "Month (Numeric)", "Quantity": "Quantity (Kg)"},
                    )
                    st.plotly_chart(fig_anomaly, use_container_width=True)

            # 13. Example Chart: Bar of State vs. Quantity
            if "State" in filtered_data.columns and "Quantity" in filtered_data.columns:
                st.subheader("Bar Chart: Total Imports by State (Filtered)")
                state_sums = filtered_data.groupby("State", as_index=False)["Quantity"].sum()
                fig_bar = px.bar(
                    state_sums,
                    x="State",
                    y="Quantity",
                    title="Total Imports by State (Filtered Data)"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
