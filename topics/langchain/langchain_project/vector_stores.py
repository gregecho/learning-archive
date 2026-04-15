"""
实现了一个向量存储服务类，用于管理向量存储，包括创建、检索和删除向量存储。该服务使用Chroma作为向量存储，并提供了一个方法来获取检索器，以便根据查询检索相关的知识。
"""

from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    """
    用于管理向量存储的服务类，包括创建、检索和删除向量存储。该服务使用Chroma作为向量存储，并提供了一个方法来获取检索器，以便根据查询检索相关的知识。
     - embedding: 用于生成向量的嵌入函数
     - vector_store: Chroma向量存储实例，用于存储和管理向量数据
     - get_retriever: 获取一个检索器，用于根据查询从向量存储中检索相关的知识
    """

    def __init__(self, embedding) -> None:
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        """
        Get a retriever for the vector store to retrieve relevant knowledge based on a query.
        """
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold}
        )


if __name__ == "__main__":
    # Example usage of the VectorStoreService
    from langchain_community.embeddings import DashScopeEmbeddings

    retriever = VectorStoreService(
        embedding=DashScopeEmbeddings(model="text-embedding-v4")
    ).get_retriever()

    res = retriever.invoke("我体重180斤，身高1米8，体脂率20%，请帮我推荐")
    print(res)
