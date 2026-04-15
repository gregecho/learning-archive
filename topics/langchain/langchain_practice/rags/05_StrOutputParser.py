from itertools import chain
from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from init_llm import deepseek_llm

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}，刚生了个{child_gender}, 请你给孩子起个名字，简短回答"
)

# StrOutputParser可以将LLM的输出解析为字符串，适用于LLM生成的内容需要被后续工具或链式调用使用的场景
parser = StrOutputParser()
chain = prompt_template | deepseek_llm | parser | deepseek_llm | parser

res = chain.invoke(input={"last_name": "李", "child_gender": "女"})
print(res)
