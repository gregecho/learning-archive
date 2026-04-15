from itertools import chain
from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import PromptTemplate
from init_llm import deepseek_llm

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}，刚生了个{child_gender}, 请你给孩子起个名字，简短回答"
)

# 1. 使用PromptTemplate生成输入，并调用LLM
# formatted_prompt = prompt_template.format(last_name="张", child_gender="男")
# print(formatted_prompt)
# res = deepseek_llm.invoke(input=formatted_prompt)
# print(res.content)

# 2. 也可以直接将PromptTemplate和LLM组合成一个链式调用
chain = prompt_template | deepseek_llm
res = chain.invoke(input={"last_name": "李", "child_gender": "女"})
print(res.content)
