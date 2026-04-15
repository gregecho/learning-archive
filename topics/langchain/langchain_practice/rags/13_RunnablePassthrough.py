"""
提示词：用户的提问 + 相关文档（从向量存储中检索）= 增强的提示词 -> LLM生成回答
"""

from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from init_llm import deepseek_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的相关文档为基础，回答用户的问题。参考资料:{docs}"),
        ("human", "用户提问:{input}"),
    ]
)

# 创建一个InMemoryVectorStore实例
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings())


# 将文档添加到向量存储中
vector_store.add_texts(
    [
        "Python是一种流行的编程语言，适用于各种应用领域。",
        "Python具有简单易学的语法，适合初学者。",
        "Python在数据科学和人工智能领域有广泛的应用。",
    ],
)

input_text = "Python适合初学者吗？"

# retriever类型的向量存储可以直接与提示词和LLM连接起来，形成一个完整的链条
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


def print_prompt(full_prompt):
    """打印完整的prompt内容，方便我们调试和理解最终传递给LLM的内容是什么样子的"""
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt


def fromat_func(docs: list[Document]) -> str:
    if not docs:
        return "没有找到相关文档。"
    formatted_docs = "\n".join(
        [f"{i+1}. {doc.page_content}" for i, doc in enumerate(docs)]
    )
    print("formatted_docs:", formatted_docs)
    return formatted_docs


# 将retriever与提示词和LLM连接起来，形成一个完整的链条
# RunnablePassthrough()的作用是将输入直接传递给下一个组件，不进行任何处理
chain = (
    {"input": RunnablePassthrough(), "docs": retriever | fromat_func}
    | prompt
    | print_prompt
    | deepseek_llm
    | StrOutputParser()
)

res = chain.invoke(input_text)
print(res)
"""
retriever:
    - 输入：用户提问                 str
    - 输出：相关文档（从向量存储中检索） list[Document]
prompt:
    - 输入：用户提问 + 相关文档 dict
    - 输出：增强的提示词       promptvalue
"""
