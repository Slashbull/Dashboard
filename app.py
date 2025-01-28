# importer_dashboard/app.py

import streamlit as st
from core.core import load_and_preprocess_data

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    st.header("Importer Dashboard 360° - Step 2")
    st.subheader("Upload Your Data")

    # Data upload options
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    # If user provides a file or Google Sheet URL
    if file or google_sheet_url:
        try:
            # Load and preprocess data
            df = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded and preprocessed successfully!")

            # Show a preview
            st.subheader("Data Preview")
            st.write(df.head())
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
