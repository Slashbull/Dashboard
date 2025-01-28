import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user
from core.filters import apply_filters, generate_filter_options, get_active_filters
from dashboards.market_overview import market_overview

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

            # Sidebar: Dashboard Navigation
            st.sidebar.title("Dashboard Navigation")
            dashboard = st.sidebar.radio(
                "Select Dashboard",
                ("Market Overview",)
            )

            # Dashboard Routing
            if dashboard == "Market Overview":
                market_overview(data)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link.")

if __name__ == "__main__":
    main()
