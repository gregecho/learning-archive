"""
jsonschema: 模型结构化输出
"""

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from init_llm import deepseek_llm

json_schema = {
    "title": "Movie",
    "description": "电影信息",
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "电影标题",
        },
        "year": {
            "type": "integer",
            "description": "上映年份",
        },
        "director": {
            "type": "string",
            "description": "导演",
        },
        "rating": {
            "type": "number",
            "description": "评分",
        },
    },
    "required": ["title", "year", "director", "rating"],
}

structured_llm = deepseek_llm.with_structured_output(json_schema)

messages = [
    # SystemMessage("以JSON格式返回，字段必须包含：title（电影标题）、year（上映年份，整数）、director（导演）、rating（评分）"),
    HumanMessage("给我介绍下电影《肖申克的救赎》"),
]

response = structured_llm.invoke(messages)
print(type(response))
print(response)
