import pandas as pd

def load_and_preprocess_data(file=None, google_sheet_url=None):
    # Load data from file or Google Sheets
    if file:
        # Check if the file is CSV or Excel
        if file.name.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    elif google_sheet_url:
        # Fetch data from Google Sheets
        sheet_id = google_sheet_url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        data = pd.read_csv(csv_url)
    else:
        raise ValueError("No data source provided.")

    # Add a Quarter column based on the Month column
    month_to_quarter = {
        'Jan': 'Q1', 'Feb': 'Q1', 'Mar': 'Q1',
        'Apr': 'Q2', 'May': 'Q2', 'Jun': 'Q2',
        'Jul': 'Q3', 'Aug': 'Q3', 'Sep': 'Q3',
        'Oct': 'Q4', 'Nov': 'Q4', 'Dec': 'Q4'
    }
    data['Quarter'] = data['Month'].map(month_to_quarter)

    # Rename columns for consistency
    data.rename(columns={
        'Consignee State': 'State',
        'Quanity': 'Quantity',
        'Job No.': 'Job_Number'
    }, inplace=True)

    return data
