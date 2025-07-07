import streamlit as st
import uuid
from engine.document_loader import load_documents
from engine.query_engine import build_query_engine
from utils.session import reset_chat
from utils.pdf_display import display_pdf
import os

st.set_page_config(page_title="Chat My Docs", layout="wide")

if "id" not in st.session_state:
    st.session_state.id = str(uuid.uuid4())
    st.session_state.file_cache ={}

if "messages" not in st.session_state:
    reset_chat()

with st.sidebar:
    st.header("Upload Your PDF Documents!")
    uploaded_files = st.file_uploader("Choose PDF file(s)", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        st.write("Indexing documents...")
        docs, display_previews = load_documents(uploaded_files, st.session_state.id)

        query_engine = build_query_engine(docs)
        st.session_state.query_engine = query_engine
        st.success("Documents ready. Start chatting!")

        for preview in display_previews:
            display_pdf(preview)

col1, col2 = st.columns([6, 1])

with col1:
    st.header("Chat with your documents")
with col2:
    st.button("Clear ↻", on_click=reset_chat)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything about the documents"):
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        if "query_engine" not in st.session_state:
            st.error("Please upload documents first")
            st.stop()

        response = st.session_state.query_engine.query(prompt)

        for chunk in response.response_gen:
            full_response += chunk
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

        if response.source_nodes:
            source = set(node.node.extra_info.get("source", "") for node in response.source_nodes)
            st.markdown("**Sources:** " + ", ".join(sorted(source)))

    st.session_state.messages.append({"role":"assistant", "content":full_response})