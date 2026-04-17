"""
总结服务类：用户提问，搜索参考资料，将用户提问和参考资料发给模型，让模型总结回复
"""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from rag.vector_store import VectorStoreService
from model.factory import chat_model
from utils.prompt_loader import get_rag_prompts


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagSummarizeService(object):
    def __init__(self) -> None:
        self.vector_store = VectorStoreService()
        self.model = chat_model
        self.retriever = self.vector_store.get_retriever()
        self.prompt_template = get_rag_prompts()
        self.prompt_text = PromptTemplate.from_template(self.prompt_template)
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = self.prompt_text | print_prompt | self.model | StrOutputParser()
        return chain

    def retrieve_docs(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retrieve_docs(query)

        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】: 参考资料：{doc.page_content} | 参考元数据：{doc.metadata}\n"

        return self.chain.invoke({"input": query, "context": context})


if __name__ == "__main__":
    rag = RagSummarizeService()
    print(rag.rag_summarize("大户型适合哪些扫地机器人"))
