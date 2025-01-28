import streamlit as st

USER_CREDENTIALS = {
    "admin": "password123",
    "user": "userpass"
}

def authenticate_user():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.sidebar.success("Login successful!")
            return True
        else:
            st.sidebar.error("Invalid username or password.")
            return False

    return st.session_state.get("authenticated", False)

def logout_user():
    st.session_state["authenticated"] = False
    st.sidebar.info("You have been logged out.")
