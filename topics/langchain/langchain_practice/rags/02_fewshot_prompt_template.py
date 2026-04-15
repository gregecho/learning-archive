from itertools import chain
from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from init_llm import deepseek_llm

# 定义示例模板和示例数据
example_template = PromptTemplate.from_template("单词: {word}，反义词:{antonym}")
examples_data = [{"word": "大", "antonym": "小"}, {"word": "高", "antonym": "低"}]

fewshot_prompt_template = FewShotPromptTemplate(
    example_prompt=example_template,  # 示例模板,`PromptTemplate` used to format an individual example.
    examples=examples_data,  # 示例数据
    prefix="根据我提供的示例，告知我反义词：",  # 前缀
    suffix="基于前面的示例，告知我{input_word}的反义词是？",  # 后缀
    input_variables=["input_word"],  # 输入变量
)


chain = fewshot_prompt_template | deepseek_llm
res = chain.invoke(input={"input_word": "快"})
print(res.content)
