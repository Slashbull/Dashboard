import streamlit as st
import hashlib

USER_CREDENTIALS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest(),
    "user": hashlib.sha256("userpass".encode()).hexdigest()
}

def authenticate_user():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", type="password", key="password")

    if st.sidebar.button("Login"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == hashed_password:
            st.session_state["authenticated"] = True
            st.sidebar.success("Login successful!")
            return True
        else:
            st.sidebar.error("Invalid credentials.")
            return False

    return st.session_state.get("authenticated", False)

def logout_user():
    st.session_state["authenticated"] = False
    st.sidebar.info("You have been logged out.")
