import pandas as pd

def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Loads and preprocesses data from a file or a Google Sheet URL.
    
    Args:
        file: File object (CSV or Excel).
        google_sheet_url: URL of the Google Sheet.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    try:
        # Load data from file
        if file:
            # Determine file type and load accordingly
            if file.name.endswith('.csv'):
                data = pd.read_csv(file, on_bad_lines='skip', engine="python")
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

        # Load data from Google Sheets
        elif google_sheet_url:
            # Extract the Google Sheets ID and convert to exportable CSV URL
            if "https://docs.google.com/spreadsheets/" in google_sheet_url:
                sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
                data = pd.read_csv(csv_url, on_bad_lines='skip', engine="python")
            else:
                raise ValueError("Invalid Google Sheets URL. Please provide a valid link.")
        else:
            raise ValueError("No data source provided.")

        # Clean column names (strip whitespace, standardize case)
        data.columns = data.columns.str.strip().str.title()

        # Add a Quarter column based on the Month column
        if "Month" in data.columns:
            month_to_quarter = {
                'Jan': 'Q1', 'Feb': 'Q1', 'Mar': 'Q1',
                'Apr': 'Q2', 'May': 'Q2', 'Jun': 'Q2',
                'Jul': 'Q3', 'Aug': 'Q3', 'Sep': 'Q3',
                'Oct': 'Q4', 'Nov': 'Q4', 'Dec': 'Q4'
            }
            data['Quarter'] = data['Month'].str.strip().str.title().map(month_to_quarter)

        # Standardize column names for consistency
        data.rename(columns={
            'Consignee State': 'State',  # Rename to 'State'
            'Quanity': 'Quantity',      # Fix any typos in 'Quantity'
            'Job No.': 'Job_Number'     # Rename Job No. for clarity
        }, inplace=True)

        # Convert Quantity to numeric (if it contains additional characters like " Kgs")
        if "Quantity" in data.columns:
            data['Quantity'] = data['Quantity'].replace(" Kgs", "", regex=True).astype(float)

        return data

    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading or preprocessing data: {e}")
