"""
Implementation of the file uploader component based on streamlit for the app.
"""

import time
from turtle import up

from huggingface_hub import upload_file
import streamlit as st
from knowledge_base import KnowledgeBaseService

# Define the title of the file uploader
st.title("Knowledge File Uploader")

# Create a file uploader component that allows users to upload their knowledge files
uploaded_file = st.file_uploader(
    "Upload your knowledge file(.txt) here",
    type=["txt"],  # Allow only specific file types to be uploaded
    accept_multiple_files=False,  # Allow only one file to be uploaded at a time
)

if "service" not in st.session_state:
    # Initialize the KnowledgeBaseService and store it in the session state
    st.session_state.service = KnowledgeBaseService()

if uploaded_file is not None:
    # Read the content of the uploaded file
    file_name = uploaded_file.name
    file_size = uploaded_file.size
    file_type = uploaded_file.type

    # Display the information of the uploaded file
    st.subheader("Uploaded File Information:")
    st.write(f"Name: {file_name} | Size: {file_size} bytes | Type: {file_type}")

    # Get the content of the uploaded file as a string
    file_content = uploaded_file.getvalue().decode("utf-8")
    st.subheader("File Content:")
    st.text(file_content)  # Display the content of the uploaded file

    with st.spinner("Uploading knowledge..."):
        time.sleep(1)
        # Upload the content of the file to the knowledge base using the upload_by_str method of the KnowledgeBaseService
        result = st.session_state.service.upload_by_str(file_content, file_name)
        st.write(result)
