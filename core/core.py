# importer_dashboard/core/core.py

import pandas as pd
import streamlit as st
import re

def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess data from a file or Google Sheet.
    
    Args:
        file: Uploaded file (CSV or Excel).
        google_sheet_url: URL to a Google Sheet.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    if not file and not google_sheet_url:
        raise ValueError("No data source provided (file or Google Sheet URL).")

    try:
        # 1. Read the data
        if file:
            # Handle local CSV or Excel upload
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        else:
            # Convert Google Sheets link to a CSV export link
            if "https://docs.google.com/spreadsheets" not in google_sheet_url:
                raise ValueError("Invalid Google Sheets URL.")
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            df = pd.read_csv(csv_url)

        # 2. Basic Column Cleaning
        df.columns = [col.strip() for col in df.columns]  # Remove extra spaces
        
        # Example: rename columns if needed
        # If your column is "Consignee State", rename to "State"
        if "Consignee State" in df.columns:
            df.rename(columns={"Consignee State": "State"}, inplace=True)
        
        # If you have "Quanity" or "Quantity"
        if "Quanity" in df.columns:
            df.rename(columns={"Quanity": "Quantity"}, inplace=True)
        
        # 3. Clean up "Quantity" column (remove non-numeric characters, convert to float)
        if "Quantity" in df.columns:
            df["Quantity"] = (
                df["Quantity"]
                .astype(str)
                .str.replace('[^0-9.]', '', regex=True)
                .replace('', '0')  # replace empty with '0'
                .astype(float)
            )
        else:
            st.warning("No 'Quantity' column found in the data.")
        
        # Optional: unify "Month" format, convert "Sept" → "Sep", etc.
        if "Month" in df.columns:
            df["Month"] = df["Month"].str.strip().str.title()
            # Convert "Sept" to "Sep" if needed
            df["Month"] = df["Month"].replace({"Sept": "Sep", "Septy": "Sep"})

        # Return the cleaned DataFrame
        return df
    
    except Exception as e:
        raise ValueError(f"Error loading/preprocessing data: {e}")
