from ast import In
from itertools import chain
from pathlib import Path
import sys
from turtle import st
from typing import cast

from click import File, prompt
from httpx import get

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashscope import Run
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableConfig, RunnableLambda
from init_llm import deepseek_llm
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from FileChatMessageHistory09 import FileChatMessageHistory

# prompt = PromptTemplate.from_template(
#     "需要根据对话历史来回答问题，对话历史是：{chat_history}，用户当前输入：{input}，请你根据对话历史来回答用户的问题"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "需要根据对话历史来回答问题"),
        MessagesPlaceholder("chat_history"),
        (
            "human",
            "用户当前输入：{input}",
        ),
    ]
)
str_parser = StrOutputParser()


def print_prompt(full_prompt):
    """打印完整的prompt内容，方便我们调试和理解最终传递给LLM的内容是什么样子的"""
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt


base_chain = prompt | print_prompt | deepseek_llm | str_parser

store = {}


def get_history(session_id: str):
    return FileChatMessageHistory(session_id=session_id, storage_path="chat_history")


conversation_chain = RunnableWithMessageHistory(
    base_chain,  # the chain to run with message history
    get_history,  # a function that takes the current messages and returns the history to use for the chain
    input_messages_key="input",  # the key in the input messages that contains the user input
    history_messages_key="chat_history",  # the key to use for the history in the chain's input
)

if __name__ == "__main__":
    session_config: RunnableConfig = {"configurable": {"session_id": "123"}}
    # res = conversation_chain.invoke(
    #     input={"input": "小明有两只猫"}, config=session_config
    # )
    # print("第一次执行", res)

    # res = conversation_chain.invoke(
    #     input={"input": "小刚有1只狗"}, config=session_config
    # )
    # print("第二次执行", res)

    res = conversation_chain.invoke(
        input={"input": "一共几只宠物"}, config=session_config
    )
    print("第三次执行", res)
