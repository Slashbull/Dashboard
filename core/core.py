import pandas as pd
import streamlit as st

def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess the uploaded data file or Google Sheet.
    """
    try:
        # Check if file is uploaded
        if file:
            if file.name.endswith(".csv"):
                data = pd.read_csv(file)
            elif file.name.endswith(".xls") or file.name.endswith(".xlsx"):
                data = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        elif google_sheet_url:
            # Process Google Sheet link
            if not google_sheet_url.startswith("https://docs.google.com/spreadsheets/"):
                raise ValueError("Invalid Google Sheet URL. Please provide a valid link.")
            csv_export_url = google_sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            data = pd.read_csv(csv_export_url)
        else:
            raise ValueError("No file or link provided.")

        # Debug: Display column names
        st.write("Columns found in the file:", data.columns.tolist())

        # Ensure required columns exist
        required_columns = ["Month", "Year", "Consignee", "Exporter", "State", "Quantity"]
        for col in required_columns:
            if col not in data.columns:
                raise KeyError(f"Required column '{col}' is missing from the uploaded data.")

        # Preprocessing
        data["Month"] = data["Month"].str.strip().str.title()  # Standardize month format
        data["Quarter"] = data["Month"].map({
            "Jan": "Q1", "Feb": "Q1", "Mar": "Q1",
            "Apr": "Q2", "May": "Q2", "Jun": "Q2",
            "Jul": "Q3", "Aug": "Q3", "Sep": "Q3",
            "Oct": "Q4", "Nov": "Q4", "Dec": "Q4"
        })  # Add Quarter column

        data["Quantity"] = data["Quantity"].replace(" Kgs", "", regex=True).astype(float)  # Clean Quantity column

        return data
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")
