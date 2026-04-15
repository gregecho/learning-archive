from pathlib import Path
import sys

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from langchain_core.tools import tool
from init_llm import deepseek_llm
from langchain_core.messages import HumanMessage

# LLM使用工具返回结果的步骤
# 1. 定义工具函数，并使用@tool装饰器进行装饰
# 2. 与LLM进行对话，LLM会根据对话内容判断是否需要调用工具函数
# 3. 根据返回结果手动处理，并将结果告知LLM
# 4. LLM根据工具函数的返回结果继续进行对话或生成内容


@tool
def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息
    Args:
        city (str): 城市名称
    Returns:
        str: 天气信息
    """
    # 这里可以调用实际的天气API来获取数据
    return f"{city}的天气是晴朗，温度25摄氏度。"


model_bind_tool = deepseek_llm.bind_tools([get_weather])

messages = []
# Construct the conversation with the human message
human_message = HumanMessage(content="请告诉我北京的天气")
messages.append(human_message)

response = model_bind_tool.invoke(messages)
# add the model's response to the conversation history
messages.append(response)

for tool_call in response.tool_calls:
    if tool_call["name"] == "get_weather":
        # 3. 根据返回结果手动处理，并将结果告知LLM
        tool_result = get_weather.invoke(tool_call)
        # print(type(tool_result))  # langchain_core.messages.tool.ToolMessage
        # 4. LLM根据工具函数的返回结果继续进行对话或生成内容
        messages.append(tool_result)
response = model_bind_tool.invoke(messages)

print(type(response))
print(response)
