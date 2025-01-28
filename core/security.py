import streamlit as st

def authenticate_user():
    st.sidebar.header("Authentication")
    username = st.sidebar.text_input("Username", key="username")
    password = st.sidebar.text_input("Password", key="password", type="password")

    if username == "admin" and password == "1234":
        return True
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
        return False
