md5_path = "./data/md5.txt"  # Path to the file where MD5 hashes will be stored

# Chroma vector store configuration
collection_name = "rag"
persist_directory = "./chroma_db"

# Text splitter configuration
chunk_size = 1000  # The maximum size of each chunk of text
chunk_overlap = 100  # The number of characters to overlap between chunks
separators = [
    "\n\n",
    "\n",
    " ",
    "",
    ".",
    "!",
    "?",
    "。",
    "？",
    "！",
]  # The separators to use when splitting the text into chunks

min_spliter_char_size = 1000  # Greater than this size will be split into chunks, otherwise it will not be split
similarity_threshold = (
    1  # The number of similar chunks to retrieve from the vector store when querying
)


embedding_model_name = "text-embedding-v4"
chat_model_name = "deepseek-chat"

chat_message_store_path = "./data/chat_history"

session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}
