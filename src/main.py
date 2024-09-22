import streamlit as st

from authenticator import main as show_login_page
from chat_prompt import main as show_chat_page


def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        show_login_page()
    else:
        show_chat_page()


if __name__ == "__main__":
    main()
