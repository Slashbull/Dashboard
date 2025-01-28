import pandas as pd
import streamlit as st

def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess data from a file or Google Sheet.
    """
    if not file and not google_sheet_url:
        raise ValueError("No data source provided (file or Google Sheet URL).")

    try:
        if file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload CSV or Excel.")
        else:
            if "docs.google.com/spreadsheets" not in google_sheet_url:
                raise ValueError("Invalid Google Sheets URL.")
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            df = pd.read_csv(csv_url)

        df.columns = df.columns.str.strip()
        if "Consignee State" in df.columns:
            df.rename(columns={"Consignee State": "State"}, inplace=True)
        if "Quanity" in df.columns:
            df.rename(columns={"Quanity": "Quantity"}, inplace=True)
        if "Quantity" in df.columns:
            df["Quantity"] = df["Quantity"].str.replace('[^0-9.]', '', regex=True).astype(float)

        return df
    except Exception as e:
        raise ValueError(f"Error loading/preprocessing data: {e}")
