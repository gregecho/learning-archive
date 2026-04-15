"""
Knowledge Base Service for managing and storing knowledge data using Chroma vector store.
"""

import hashlib
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from numpy import save
import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from datetime import datetime


def check_md5(md5_str: str) -> bool:
    """
    Check the MD5 hash of the uploaded file to ensure data integrity.

    Args:
        md5_str (str): md5 string

    Returns:
        bool: True if the MD5 hash exists, False otherwise
    """
    if not os.path.exists(config.md5_path):
        open(
            config.md5_path, "w", encoding="utf-8"
        ).close()  # Create the MD5 file if it does not exist
        return False  # If the file does not exist, return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()  # Remove leading and trailing whitespace characters
            if line == md5_str:
                return True  # If the MD5 hash matches, return True
        return False  # If the MD5 hash does not match, return False


def save_md5(md5_str: str):
    """
    Save the MD5 hash of the uploaded file for future reference.
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")  # Append the MD5 hash to the file


def get_str_md5(input_str: str) -> str:
    """
    Get the MD5 hash of a string input.

    Args:
        input_str (str): input string

    Returns:
        str: md5 string
    """
    str_bytes = input_str.encode("utf-8")  # Encode the string to bytes
    md5_obj = hashlib.md5()  # Create an MD5 hash object
    md5_obj.update(str_bytes)  # Update the hash object with the bytes
    return md5_obj.hexdigest()  # Return the hexadecimal representation of the hash


class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model=config.embedding_model_name),
            persist_directory=config.persist_directory,
        )  # Initialize the Chroma vector store for storing and retrieving knowledge

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
        )  # Initialize the text splitter for splitting the knowledge into smaller chunks

    def upload_by_str(self, data, filename):
        """
        Upload knowledge data as a string and save it to the Chroma vector store.
        """
        md5_hex = get_str_md5(data)
        if check_md5(md5_hex):
            return "Data already exists, skipping upload"

        if len(data) > config.min_spliter_char_size:
            # Split the knowledge into smaller chunks if it exceeds the minimum size
            knowledge_chunks = self.spliter.split_text(data)
        else:
            # Knowledge is smaller than the minimum size, do not split it
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "admin",
        }  # Metadata for the knowledge, including source and creation time

        # Save the MD5 hash of the knowledge to ensure data integrity
        self.chroma.add_texts(
            knowledge_chunks, metadatas=[metadata] * len(knowledge_chunks)
        )
        print([metadata] * len(knowledge_chunks))
        save_md5(md5_hex)  # Save the MD5 hash of the knowledge for future reference
        return "Knowledge uploaded successfully"


if __name__ == "__main__":
    knowledge_service = KnowledgeBaseService()
    res = knowledge_service.upload_by_str(
        "This is a test knowledge string.", "test.txt"
    )
    print([{"test": "test"}] * 3)
