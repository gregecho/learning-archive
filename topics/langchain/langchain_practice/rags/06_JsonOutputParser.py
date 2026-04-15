from itertools import chain
from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from init_llm import deepseek_llm

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

prompt_template = PromptTemplate.from_template(
    '我的邻居姓{last_name}，刚生了个{child_gender}, 请你给孩子起个名字，简短回答。并用json格式返回，格式如下：{{"name": "名字"}}'
)

second_prompt_template = PromptTemplate.from_template(
    "姓名{name}: 帮我分析这个名字的含义"
)

chain = (
    prompt_template
    | deepseek_llm
    | json_parser
    | second_prompt_template
    | deepseek_llm
    | str_parser
)

res = chain.invoke(input={"last_name": "李", "child_gender": "女"})
print(res)
