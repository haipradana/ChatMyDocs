import streamlit as st
import base64

def display_pdf(file_bytes):
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)