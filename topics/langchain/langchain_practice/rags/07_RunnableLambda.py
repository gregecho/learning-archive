from itertools import chain
from pathlib import Path
import sys
from typing import cast

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda
from init_llm import deepseek_llm
from langchain_core.messages import AIMessage

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 定义一个RunnableLambda，接收AIMessage并返回一个包含"name"键的字典
json_function = RunnableLambda(lambda ai_msg: {"name": cast(AIMessage, ai_msg).content})

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}，刚生了个{child_gender}, 请你给孩子起个名字，简短回答"
)

second_prompt_template = PromptTemplate.from_template(
    "姓名{name}: 帮我分析这个名字的含义"
)

chain = (
    prompt_template
    | deepseek_llm
    | json_function
    | second_prompt_template
    | deepseek_llm
    | str_parser
)

res = chain.invoke(input={"last_name": "李", "child_gender": "女"})
print(res)
