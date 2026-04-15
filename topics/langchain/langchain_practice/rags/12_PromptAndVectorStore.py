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
# 从向量存储中检索相关文档
similar_docs = vector_store.similarity_search(query=input_text, k=2)
print(similar_docs)
# 将检索到的相关文档与用户提问一起构建增强的提示词
enhanced_prompt = prompt.format(input=input_text, docs=similar_docs)

chain = prompt | deepseek_llm | StrOutputParser()
# 使用增强的提示词生成回答
response = chain.invoke({"input": input_text, "docs": similar_docs})
print(response)
