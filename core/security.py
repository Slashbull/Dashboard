# importer_dashboard/core/security.py

import streamlit as st

# Example credentials (In production, store securely!)
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "userpass"
}

def authenticate_user():
    """Display a login form and authenticate the user."""
    st.sidebar.title("Login")

    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", type="password", key="password")

    if st.sidebar.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.sidebar.success("Login successful!")
            return True
        else:
            st.sidebar.error("Invalid username or password.")
            return False
    
    # If the user already logged in this session
    if "authenticated" in st.session_state and st.session_state["authenticated"]:
        return True
    
    return False

def logout_user():
    """Log out the current user."""
    st.session_state["authenticated"] = False
    st.sidebar.info("You have been logged out.")
