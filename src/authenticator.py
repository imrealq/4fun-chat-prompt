import streamlit as st

import db


def sign_in():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if db.authenticate_user(email, password):
            st.success("Success!")
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect email or password!")


def main():
    db.init_db()
    st.title("Sign In")
    sign_in()
