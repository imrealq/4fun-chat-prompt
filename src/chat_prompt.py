import os

import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

TITLE = "💬 Welcome to chat prompt"
API_KEY = os.getenv("API_KEY")
CLIENT_TYPE = os.getenv("CLIENT_TYPE", "anthropic")
MODEL = os.getenv("MODEL", "claude-3-sonnet-20240320")


def get_client(api_key=None, client_type="anthropic"):
    if not api_key:
        st.info("Please add your API key to continue.")
        st.stop()

    if client_type.lower() == "anthropic":
        return Anthropic(api_key=api_key)
    elif client_type.lower() == "openai":
        return OpenAI(api_key=api_key)
    else:
        raise ValueError("Invalid client_type. Choose 'openai' or 'anthropic'.")


def create_chat_completion(client, messages):
    if isinstance(client, Anthropic):
        try:
            response = client.messages.create(
                model=MODEL,
                messages=messages,
                max_tokens=300,
            )
            return response.content[0].text
        except Exception as e:
            st.error(f"Error with Anthropic API: {str(e)}")
            return None
    elif isinstance(client, OpenAI):
        try:
            response = client.chat.completions.create(model=MODEL, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error with OpenAI API: {str(e)}")
            return None
    else:
        st.error("Invalid client type")
        return None


def chat_prompt():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = create_chat_completion(st.session_state.client, st.session_state.messages)
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)


def main():
    st.title(TITLE)
    st.session_state.client = get_client(API_KEY, CLIENT_TYPE)
    if st.session_state.client:
        chat_prompt()


if __name__ == "__main__":
    main()
