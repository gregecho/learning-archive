from langchain.agents import create_agent
from pathlib import Path
import sys

from langchain_core.tools import tool

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from init_llm import deepseek_llm


@tool(description="获取天气信息")
def get_weather(location: str) -> str:
    # 这里可以调用一个天气API来获取天气信息
    print(f"获取{location}的天气信息...")
    return f"{location}今天天气晴朗，温度25度。"


agent = create_agent(
    deepseek_llm,
    tools=[get_weather],
    system_prompt="你是一个智能聊天助手，能够回答用户的问题并提供帮助。",
)

res = agent.invoke({"messages": [{"role": "user", "content": "济南今天天气怎么样？"}]})

for message in res["messages"]:
    print(f"{type(message).__name__}: {message.content}")
