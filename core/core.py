def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess data from a file or Google Sheet.
    
    Args:
        file: Uploaded file (CSV or Excel).
        google_sheet_url: URL to a Google Sheet.

    Returns:
        pd.DataFrame: Preprocessed DataFrame.
    """
    try:
        # Load data from file or Google Sheets
        if file:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith(('.xls', '.xlsx')):
                data = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        elif google_sheet_url:
            # Convert Google Sheets link to exportable CSV URL
            if "https://docs.google.com/spreadsheets/" not in google_sheet_url:
                raise ValueError("Invalid Google Sheets URL.")
            sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            data = pd.read_csv(csv_url)
        else:
            raise ValueError("No data source provided.")

        # Clean column names (case-insensitive)
        data.columns = data.columns.str.strip().str.title()  # Normalize column names
        data.rename(columns={
            'Consignee State': 'State',
            'Quanity': 'Quantity',
            'Job No.': 'Job_Number'
        }, inplace=True)

        # Add a Quarter column if 'Month' exists
        if 'Month' in data.columns:
            month_to_quarter = {
                'Jan': 'Q1', 'Feb': 'Q1', 'Mar': 'Q1',
                'Apr': 'Q2', 'May': 'Q2', 'Jun': 'Q2',
                'Jul': 'Q3', 'Aug': 'Q3', 'Sep': 'Q3',
                'Oct': 'Q4', 'Nov': 'Q4', 'Dec': 'Q4'
            }
            data['Quarter'] = (
                data['Month']
                .str.strip()  # Remove leading/trailing spaces
                .str.title()  # Normalize month names (e.g., 'jan' -> 'Jan')
                .map(month_to_quarter)  # Map to quarters
            )
        else:
            st.warning("No 'Month' column found. Skipping quarter calculation.")

        # Clean the Quantity column
        if 'Quantity' in data.columns:
            # Remove non-numeric characters (e.g., '-', ',', ' Kgs')
            data['Quantity'] = (
                data['Quantity']
                .astype(str)  # Ensure it's a string
                .str.replace('[^0-9.]', '', regex=True)  # Remove all non-numeric characters
                .replace('', '0')  # Replace empty strings with '0'
                .astype(float)  # Convert to float
            )
        else:
            st.warning("No 'Quantity' column found. Skipping quantity cleaning.")

        return data

    except Exception as e:
        raise ValueError(f"Error loading and preprocessing data: {e}")
