# importer_dashboard/app.py

import streamlit as st

# COMMENTED OUT for Step 1:
# from core.core import load_and_preprocess_data
# from core.security import authenticate_user, logout_user

def main():
    st.set_page_config(page_title="Importer Dashboard 360°", layout="wide")

    # COMMENTED OUT for Step 1:
    # authenticated = authenticate_user()
    # if not authenticated:
    #     st.stop()

    # if st.sidebar.button("Logout"):
    #     logout_user()
    #     st.stop()

    st.header("Importer Dashboard 360° - Step 1")
    st.write("This is our minimal starting point. We'll add data uploads, filters, and authentication in the next steps.")

if __name__ == "__main__":
    main()
