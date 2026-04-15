"""
typedDict: 模型结构化输出
"""

from typing import Annotated, TypedDict

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from init_llm import deepseek_llm

class Movie(TypedDict):
    title: Annotated[str, "电影标题"]
    year: Annotated[int, "电影上映年份"]
    director: Annotated[str, "电影导演"]
    rating: Annotated[float, "电影评分"]

structured_llm = deepseek_llm.with_structured_output(Movie, method="json_mode")

messages = [
    SystemMessage("以JSON格式返回，字段必须包含：title（电影标题）、year（上映年份，整数）、director（导演）、rating（评分）"),
    HumanMessage("给我介绍下电影《肖申克的救赎》"),
]

response = structured_llm.invoke(messages)
print(type(response))
print(response)