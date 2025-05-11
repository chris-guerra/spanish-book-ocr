import streamlit as st
import requests
from pathlib import Path
import os
from ..core.config import settings

st.set_page_config(
    page_title="Spanish Book OCR",
    page_icon="📚",
    layout="wide"
)

st.title("Spanish Book OCR")
st.write("Convert scanned PDF books into text files")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file
    file_path = settings.INPUT_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File {uploaded_file.name} uploaded successfully!")

# Language selection
st.subheader("OCR Language")
available_languages = ["spa", "eng", "fra", "deu", "ita"]  # TODO: Get from API
selected_language = st.selectbox(
    "Select OCR language",
    available_languages,
    index=0
)

# Process button
if st.button("Process PDF"):
    if uploaded_file is None:
        st.error("Please upload a PDF file first")
    else:
        with st.spinner("Processing..."):
            # TODO: Call API to process the file
            st.info("Processing started...")

# Download section
st.subheader("Download Results")
# TODO: Add download functionality for processed files 