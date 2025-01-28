import streamlit as st
import pandas as pd
import chardet
from io import StringIO
import requests

# Function to load and preprocess data
def load_and_preprocess_data(file=None, google_sheet_url=None):
    """
    Load and preprocess the uploaded data file or Google Sheet.
    Handles irregular CSV formats and missing data gracefully.
    """
    try:
        # Detect encoding and load the file
        if file:
            raw_data = file.read()  # Read the file content as raw bytes
            detected_encoding = chardet.detect(raw_data)["encoding"]
            file.seek(0)  # Reset file pointer

            if file.name.endswith(".csv"):
                data = pd.read_csv(file, encoding=detected_encoding, on_bad_lines='skip', engine="python")
            elif file.name.endswith(".xls") or file.name.endswith(".xlsx"):
                data = pd.read_excel(file)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
        elif google_sheet_url:
            # Process Google Sheet link
            if not google_sheet_url.startswith("https://docs.google.com/spreadsheets/"):
                raise ValueError("Invalid Google Sheet URL. Please provide a valid link.")
            csv_export_url = google_sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            data = pd.read_csv(csv_export_url, on_bad_lines='skip', engine="python")
        else:
            raise ValueError("No file or link provided.")

        # Debugging: Show column names
        st.write("Columns found in the file:", data.columns.tolist())

        # Ensure required columns exist
        required_columns = ["Month", "Year", "Consignee", "Exporter", "Consignee State", "Quanity"]
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

        data["Quanity"] = data["Quanity"].replace(" Kgs", "", regex=True).astype(float)  # Clean Quantity column

        return data
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing data: {e}")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

# Streamlit app UI
st.title("Importer Dashboard 360°")
st.sidebar.title("Upload Data")

# File Upload or Google Sheet URL Input
file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
google_sheet_url = st.sidebar.text_input("Or provide a Google Sheets link")

# Handle file uploads or Google Sheet link
if file or google_sheet_url:
    try:
        # Load and preprocess data
        data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
        st.success("Data loaded successfully!")
        st.subheader("Dataset Preview")
        st.write(data.head())

        # Data Filtering Options
        st.sidebar.subheader("Filters")
        states = data["Consignee State"].unique()
        selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))

        consignees = data["Consignee"].unique()
        selected_consignee = st.sidebar.selectbox("Select Consignee", ["All"] + list(consignees))

        months = data["Month"].unique()
        selected_month = st.sidebar.selectbox("Select Month", ["All"] + list(months))

        years = data["Year"].unique()
        selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(years))

        # Apply filters based on user selection
        filtered_data = data
        if selected_state != "All":
            filtered_data = filtered_data[filtered_data["Consignee State"] == selected_state]
        if selected_consignee != "All":
            filtered_data = filtered_data[filtered_data["Consignee"] == selected_consignee]
        if selected_month != "All":
            filtered_data = filtered_data[filtered_data["Month"] == selected_month]
        if selected_year != "All":
            filtered_data = filtered_data[filtered_data["Year"] == selected_year]

        st.subheader("Filtered Data")
        st.write(filtered_data)

    except pd.errors.ParserError:
        st.error("There was an issue parsing the file. Please check the file's formatting.")
    except KeyError as e:
        st.error(f"Missing required columns: {e}")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload a file or provide a Google Sheet link to proceed.")
