import pandas as pd

def load_and_preprocess_data(file=None, google_sheet_url=None):
    try:
        if file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format.")
        else:
            if "docs.google.com/spreadsheets" not in google_sheet_url:
                raise ValueError("Invalid Google Sheets URL.")
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            df = pd.read_csv(csv_url)

        # Data Preprocessing
        df.columns = df.columns.str.strip()
        df.rename(columns={"Consignee State": "State", "Quanity": "Quantity"}, inplace=True)

        if "Quantity" in df.columns:
            df["Quantity"] = pd.to_numeric(df["Quantity"].str.replace('[^0-9.]', '', regex=True))

        month_to_quarter = {
            "Jan": "Q1", "Feb": "Q1", "Mar": "Q1",
            "Apr": "Q2", "May": "Q2", "Jun": "Q2",
            "Jul": "Q3", "Aug": "Q3", "Sep": "Q3",
            "Oct": "Q4", "Nov": "Q4", "Dec": "Q4",
        }
        if "Month" in df.columns:
            df["Quarter"] = df["Month"].map(month_to_quarter)

        return df
    except Exception as e:
        raise ValueError(f"Error during data preprocessing: {e}")
