
import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user

def main():
    # Authentication
    authenticated = authenticate_user()
    if not authenticated:
        return

    # Header
    st.header("Importer Dashboard")
    st.subheader("Upload Your Data")

    # Data upload options
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # Load and preprocess data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded successfully!")

            # Display dataset preview
            st.subheader("Dataset Preview")
            st.write(data.head())

            # Summary KPIs
            total_imports = data['Quantity'].sum()
            unique_states = data['State'].nunique()
            st.metric("Total Imports (Kg)", f"{total_imports:,}")
            st.metric("States Involved", unique_states)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
