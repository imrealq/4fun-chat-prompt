import os

import streamlit as st
from openai import OpenAI

TITLE = "💬 Welcome to chat prompt"
API_KEY = os.getenv("API_KEY")


def st_sidebar():
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

        return openai_api_key


def get_client(api_key=None):
    if not api_key:
        st.info("Please add your API key to continue.")
        st.stop()

    client = OpenAI(api_key=api_key)
    return client


def chat_prompt(client):
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)


def main():
    st.title(TITLE)
    # api_key = st_sidebar()
    client = get_client(API_KEY)
    if client:
        chat_prompt(client)


if __name__ == "__main__":
    main()
