import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from submodules.anomaly_detection import detect_anomalies
import plotly.express as px
import datetime
import io

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

    # Data Upload
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # Load and preprocess data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded successfully!")
            st.subheader("Dataset Preview")
            st.write(data.head())

            # Get current quarter and year
            current_month = datetime.datetime.now().month
            current_quarter = f"Q{((current_month - 1) // 3) + 1}"
            current_year = datetime.datetime.now().year

            # Sidebar Filters
            st.sidebar.subheader("Filter Options")
            filters = {}
            for column, default in [
                ("State", "All"),
                ("Quarter", current_quarter),
                ("Month", "All"),
                ("Year", current_year),
                ("Consignee", "All"),
                ("Exporter", "All"),
            ]:
                if column in data.columns:
                    options = ["All"] + sorted(data[column].dropna().unique())
                    filters[column] = st.sidebar.selectbox(
                        f"Select {column}", options, index=options.index(default) if default in options else 0
                    )
                else:
                    filters[column] = "All"

            # Apply Filters
            filtered_data = data.copy()
            for column, value in filters.items():
                if value != "All":
                    filtered_data = filtered_data[filtered_data[column] == value]

            # Display Filtered Data
            if filtered_data.empty:
                st.warning("No data matches the selected filters. Please adjust your filter options.")
            else:
                st.subheader("Filtered Data")
                st.write(filtered_data)

                # KPI Metrics
                total_imports = filtered_data["Quantity"].sum() if "Quantity" in filtered_data.columns else 0
                unique_states = filtered_data["State"].nunique() if "State" in filtered_data.columns else 0

                col1, col2 = st.columns(2)
                col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
                col2.metric("States Involved", unique_states)

                # Anomaly Detection
                st.subheader("Anomaly Detection")
                if st.checkbox("Run Anomaly Detection"):
                    anomalies = detect_anomalies(filtered_data, column="Quantity", method="iqr")
                    st.write(anomalies[anomalies["is_anomaly"]])

                    # Visualization for Anomalies
                    if "State" in anomalies.columns and "Quantity" in anomalies.columns:
                        fig = px.scatter(
                            anomalies,
                            x="State",
                            y="Quantity",
                            color="is_anomaly",
                            title="Quantity by State with Anomalies Highlighted",
                        )
                        st.plotly_chart(fig, use_container_width=True)

                # Quarterly Trends
                st.subheader("Quarterly Trends")
                if "Quarter" in filtered_data.columns and "Quantity" in filtered_data.columns:
                    quarter_sums = filtered_data.groupby("Quarter", as_index=False)["Quantity"].sum()
                    fig_quarter = px.bar(
                        quarter_sums,
                        x="Quarter",
                        y="Quantity",
                        title="Total Imports by Quarter",
                        labels={"Quarter": "Quarter", "Quantity": "Quantity (Kg)"},
                    )
                    st.plotly_chart(fig_quarter, use_container_width=True)

                # Data Export
                st.download_button(
                    label="Download Filtered Data as CSV",
                    data=filtered_data.to_csv(index=False),
                    file_name="filtered_data.csv",
                    mime="text/csv",
                )

                # Export Quarterly Trends
                if "Quarter" in filtered_data.columns:
                    to_excel = io.BytesIO()
                    with pd.ExcelWriter(to_excel, engine="xlsxwriter") as writer:
                        filtered_data.to_excel(writer, index=False, sheet_name="Filtered Data")
                        quarter_sums.to_excel(writer, index=False, sheet_name="Quarterly Trends")
                    to_excel.seek(0)
                    st.download_button(
                        label="Download Data as Excel",
                        data=to_excel,
                        file_name="data_analysis.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link.")

if __name__ == "__main__":
    main()
