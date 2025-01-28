import streamlit as st
import pandas as pd
import chardet
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user

# Function to handle file loading, preprocessing and data transformations
def load_and_preprocess_data(file=None, google_sheet_url=None):
    try:
        # If file is uploaded
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
        # If Google Sheets link is provided
        elif google_sheet_url:
            if not google_sheet_url.startswith("https://docs.google.com/spreadsheets/"):
                raise ValueError("Invalid Google Sheet URL. Please provide a valid link.")
            csv_export_url = google_sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            data = pd.read_csv(csv_export_url, on_bad_lines='skip', engine="python")
        else:
            raise ValueError("No file or link provided.")

        # Print out columns for debugging
        st.write("Columns in the dataset:", data.columns.tolist())

        # Clean the column names (strip spaces, handle case inconsistencies)
        data.columns = data.columns.str.strip()  # Strip any leading/trailing spaces
        data.columns = data.columns.str.title()  # Convert column names to title case (e.g., "Month" instead of "month")

        # Check the columns after cleaning
        st.write("Cleaned columns:", data.columns.tolist())

        # Preprocessing data (cleaning and formatting)
        data["Month"] = data["Month"].str.strip().str.title()  # Standardizing month format
        data["Quarter"] = data["Month"].map({
            "Jan": "Q1", "Feb": "Q1", "Mar": "Q1",
            "Apr": "Q2", "May": "Q2", "Jun": "Q2",
            "Jul": "Q3", "Aug": "Q3", "Sep": "Q3",
            "Oct": "Q4", "Nov": "Q4", "Dec": "Q4"
        })  # Add Quarter column

        data["Quantity"] = data["Quantity"].replace(" Kgs", "", regex=True).astype(float)  # Clean Quantity column

        return data
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing data: {e}")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")


def main():
    # Authentication
    authenticated = authenticate_user()
    if not authenticated:
        return  # Stop app if not authenticated

    # Logout button
    if st.sidebar.button("Logout"):
        logout_user()
        return

    # Main app content after authentication
    st.header("Importer Dashboard 360°")
    st.subheader("Upload Your Data")

    # Data upload options
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xls", "xlsx"])
    google_sheet_url = st.text_input("Or provide a Google Sheet link:")

    if file or google_sheet_url:
        try:
            # Load and preprocess data
            data = load_and_preprocess_data(file=file, google_sheet_url=google_sheet_url)
            st.success("Data loaded successfully!")

            # Display dataset preview
            st.subheader("Dataset Preview")
            st.write(data.head())

            # Filter options (State, Consignee, Month, Year)
            st.sidebar.subheader("Filter Options")
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

            # Summary KPIs
            total_imports = filtered_data['Quantity'].sum()
            unique_states = filtered_data['Consignee State'].nunique()

            st.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
            st.metric("States Involved", unique_states)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
