# importer_dashboard/core/core.py

import pandas as pd
import streamlit as st
import re

def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess data from a file or Google Sheet.
    
    Args:
        file (UploadedFile): A CSV or Excel file uploaded via Streamlit.
        google_sheet_url (str): Publicly accessible Google Sheet link.

    Returns:
        pd.DataFrame: Cleaned DataFrame ready for filtering and analysis.
    """
    if not file and not google_sheet_url:
        raise ValueError("No data source provided (file or Google Sheet URL).")

    try:
        # Load from local file
        if file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel.")
        else:
            # Convert Google Sheets link to CSV export URL
            if "docs.google.com/spreadsheets" not in google_sheet_url:
                raise ValueError("Invalid Google Sheets URL.")
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            df = pd.read_csv(csv_url)

        # Clean column names (remove extra spaces, make them consistent)
        df.columns = [col.strip() for col in df.columns]

        # Example: rename columns if they exist
        if "Consignee State" in df.columns:
            df.rename(columns={"Consignee State": "State"}, inplace=True)
        if "Quanity" in df.columns:
            df.rename(columns={"Quanity": "Quantity"}, inplace=True)

        # Clean Quantity column (remove non-numerics, convert to float)
        if "Quantity" in df.columns:
            df["Quantity"] = (
                df["Quantity"]
                .astype(str)
                .str.replace('[^0-9.]', '', regex=True)  # remove anything not digit/decimal
                .replace('', '0')  # empty => 0
                .astype(float)
            )
        else:
            st.warning("No 'Quantity' column found. Some analyses may be unavailable.")

        # Normalize "Month" values if they exist (e.g., 'Sept' -> 'Sep')
        if "Month" in df.columns:
            df["Month"] = df["Month"].str.strip().str.title()
            df["Month"] = df["Month"].replace({"Sept": "Sep"})

        # If you have a "Year" column and it's string, convert to numeric
        if "Year" in df.columns:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

        return df

    except Exception as e:
        raise ValueError(f"Error loading/preprocessing data: {e}")
