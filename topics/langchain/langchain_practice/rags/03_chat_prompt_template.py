from itertools import chain
from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from init_llm import deepseek_llm

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位边塞诗人"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "请你根据前面的对话内容，创作一首七言律诗，题目是《边塞》"),
    ]
)

history_data = [
    ("human", "你能否描述一下边塞的景色吗？"),
    (
        "ai",
        "边塞的景色壮丽而辽阔，黄沙漫天，戈壁无垠。",
    ),
    ("human", "边塞的士兵们在这样的环境中是如何生活的？"),
    (
        "ai",
        "边塞的士兵们生活艰苦，他们常常要面对恶劣的天气和环境。",
    ),
]

# Return StringPromptValue
prompt_text = chat_prompt_template.invoke(input={"history": history_data}).to_string()
res = deepseek_llm.invoke(input=prompt_text)
print(res.content)
