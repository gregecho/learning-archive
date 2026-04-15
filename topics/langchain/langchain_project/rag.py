from file_history_store import get_history
from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from env_utils import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
from langchain_core.runnables import (
    RunnableConfig,
    RunnableLambda,
    RunnablePassthrough,
    RunnableWithMessageHistory,
)
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser


class RagService(object):
    """
    该服务

    Args:
        object (_type_): _description_
    """

    def __init__(self) -> None:
        self.vector_store_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "以我提供的已知材料为主，简介和专业的回答用户问题。参考资料: {context}",
                ),
                ("system", "用户的对话记录如下："),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问：{input}"),
            ]
        )
        self.chat_model = init_chat_model(
            model=config.chat_model_name,
            model_provider="deepseek",
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_store_service.get_retriever()

        def format_document(docs: list[Document]):
            if not docs:
                return "No relevant knowledge found."
            formatted_docs = []
            for doc in docs:
                formatted_docs.append(
                    f"Source: {doc.metadata.get('source', 'Unknown')}\nContent: {doc.page_content}\n\n"
                )
            return formatted_docs

        def format_for_retriever(value: dict) -> str:
            """从输入中提取用户问题，传递给检索器进行检索"""
            return value["input"]

        def format_for_prompt_template(value):
            """将检索到的文档和用户输入格式化为适合 prompt template 的输入格式"""
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                # 步骤 1: 准备数据
                "input": RunnablePassthrough(),  # 原样传递用户的问题
                "context": RunnableLambda(format_for_retriever)
                | retriever
                | format_document,  # 检索并【通过 format_document】格式化为字符串
            }
            | RunnableLambda(format_for_prompt_template)
            | self.prompt_template  # 步骤 2: 将 input 和 context 填入模板
            | self.chat_model  # 步骤 3: 传给 AI 进行推理
            | StrOutputParser()  # 步骤 4: 把 AI 的响应解析为纯字符串
        )

        # 使用 RunnableWithMessageHistory 包装 chain，使其能够访问和更新对话历史
        conversational_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversational_chain


if __name__ == "__main__":
    session_config: RunnableConfig = {"configurable": {"session_id": "user_001"}}

    res = RagService().chain.invoke({"input": "羽绒服怎么保养"}, config=session_config)

    print(res)
