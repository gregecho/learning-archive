from unittest import loader

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

# 创建一个InMemoryVectorStore实例
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="opinion_on_programming",
)
documents = loader.load()

# 将文档添加到向量存储中
vector_store.add_documents(
    documents=documents, ids=["id" + str(i) for i in range(1, len(documents) + 1)]
)

vector_store.delete(ids=["id1", "id2"])

# 进行相似度搜索
query = "编程是不是很难"
similar_docs = vector_store.similarity_search(query=query, k=3)
print(similar_docs)
