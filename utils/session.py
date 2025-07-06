import streamlit as st

def reset_chat():
    st.session_state.messages = []
    st.session_state.context = None