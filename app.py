import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from core.filters import apply_filters, generate_filter_options, get_active_filters
from submodules.key_metrics import calculate_kpis
import plotly.express as px
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
            st.subheader("Dataset Preview")
            st.write(data.head())

            # Sidebar Filters
            st.sidebar.subheader("Filter Options")

            # Generate Filter Options
            columns = ["Quarter", "Month", "Year", "State", "Consignee", "Exporter"]
            filter_options = generate_filter_options(data, columns)

            # Filter Selection
            filters = {}
            for column in columns:
                if column in ["State", "Consignee", "Exporter"]:  # Multi-select filters
                    filters[column] = st.sidebar.multiselect(f"Select {column}", filter_options[column])
                else:  # Single-select filters
                    filters[column] = st.sidebar.selectbox(f"Select {column}", filter_options[column])

            # Apply Filters
            filtered_data = apply_filters(data, filters)

            # Active Filters Summary
            active_filters = get_active_filters(filters)
            st.sidebar.write("**Active Filters**:")
            for key, value in active_filters.items():
                st.sidebar.write(f"{key}: {', '.join(value) if isinstance(value, list) else value}")

            # Display Filtered Data
            if filtered_data.empty:
                st.warning("No data matches the selected filters. Please adjust your filter options.")
            else:
                st.subheader("Filtered Data")
                st.write(filtered_data)

                # KPI Metrics
                total_imports, unique_states, yoy_growth, mom_growth = calculate_kpis(filtered_data)

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
                col2.metric("States Involved", unique_states)
                col3.metric("YoY Growth (%)", f"{yoy_growth:.2f}")
                col4.metric("MoM Growth (%)", f"{mom_growth:.2f}")

                # Visualization: Quarterly Trends
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

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link.")

if __name__ == "__main__":
    main()
