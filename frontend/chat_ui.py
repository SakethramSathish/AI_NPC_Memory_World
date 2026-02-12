import streamlit as st

def init_chat():
    """
    Initialize chat history in session state.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def render_chat():
    """
    Render the chat history.
    """
    for entry in st.session_state.chat_history:
        role = entry["role"]
        message = entry["message"]

        if role == "player":
            with st.chat_message("user"):
                st.write(message)
        else:
            with st.chat_message("assistant"):
                st.write(message)


def chat_input():
    """
    Render chat input box with submit button.
    Returns player input text when submitted.
    """
    return st.chat_input("Say something to the NPC...")


def append_player_message(message: str):
    st.session_state.chat_history.append(
        {"role": "player", "message": message}
    )


def append_npc_message(message: str):
    st.session_state.chat_history.append(
        {"role": "npc", "message": message}
    )