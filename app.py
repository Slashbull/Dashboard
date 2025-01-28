# importer_dashboard/app.py

import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    # 1. Authentication
    authenticated = authenticate_user()
    if not authenticated:
        st.stop()  # Stop the app if user is not authenticated

    if st.sidebar.button("Logout"):
        logout_user()
        st.stop()

    # 2. Header & Data Upload
    st.header("Importer Dashboard 360° - Step 3")
    st.subheader("Upload Your Data")

    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # 3. Load & Preprocess Data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded and preprocessed successfully!")

            # 4. Dataset Preview
            st.subheader("Dataset Preview")
            st.write(data.head())  # Show top 5 rows

            # 5. Filters (Sidebar)
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

            # 6. Apply Filters
            filtered_data = data.copy()

            if selected_state != "All" and "State" in data.columns:
                filtered_data = filtered_data[filtered_data["State"] == selected_state]

            if selected_month != "All" and "Month" in data.columns:
                filtered_data = filtered_data[filtered_data["Month"] == selected_month]

            if selected_year != "All" and "Year" in data.columns:
                filtered_data = filtered_data[filtered_data["Year"] == selected_year]

            if selected_consignee != "All" and "Consignee" in data.columns:
                filtered_data = filtered_data[filtered_data["Consignee"] == selected_consignee]

            if selected_exporter != "All" and "Exporter" in data.columns:
                filtered_data = filtered_data[filtered_data["Exporter"] == selected_exporter]

            # 7. Display Filtered Data
            st.subheader("Filtered Data")
            st.write(filtered_data)

            # 8. Summary KPIs
            # Example: total quantity & unique states in the filtered dataset
            if "Quantity" in filtered_data.columns:
                total_imports = filtered_data["Quantity"].sum()
            else:
                total_imports = 0

            if "State" in filtered_data.columns:
                unique_states_count = filtered_data["State"].nunique()
            else:
                unique_states_count = 0

            # Show KPI metrics
            col1, col2 = st.columns(2)
            col1.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
            col2.metric("States Involved", unique_states_count)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
