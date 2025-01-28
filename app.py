import streamlit as st
from core.core import load_and_preprocess_data
from core.security import authenticate_user, logout_user

def main():
    # Authentication
    authenticated = authenticate_user()
    if not authenticated:
        st.stop()  # Stop the app if not authenticated

    # Logout button
    if st.sidebar.button("Logout"):
        logout_user()
        st.stop()

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
            st.success("Data loaded and preprocessed successfully!")

            # Display dataset preview
            st.subheader("Dataset Preview")
            st.write(data.head())

            # Sidebar filters
            st.sidebar.subheader("Filter Options")
            states = data["State"].unique()
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
                filtered_data = filtered_data[filtered_data["State"] == selected_state]
            if selected_consignee != "All":
                filtered_data = filtered_data[filtered_data["Consignee"] == selected_consignee]
            if selected_month != "All":
                filtered_data = filtered_data[filtered_data["Month"] == selected_month]
            if selected_year != "All":
                filtered_data = filtered_data[filtered_data["Year"] == selected_year]

            st.subheader("Filtered Data")
            st.write(filtered_data)

            # Summary KPIs
            total_imports = filtered_data["Quantity"].sum() if not filtered_data.empty else 0
            unique_states = filtered_data["State"].nunique() if not filtered_data.empty else 0

            st.metric("Total Imports (Kg)", f"{total_imports:,.2f}")
            st.metric("States Involved", unique_states)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload a file or provide a Google Sheet link to proceed.")

if __name__ == "__main__":
    main()
