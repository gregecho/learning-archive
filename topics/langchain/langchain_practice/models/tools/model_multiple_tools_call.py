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
def get_stock_price(stock_symbol: str) -> str:
    """
    获取指定股票的价格信息
    Args:
        stock_symbol (str): 股票代码
    Returns:
        str: 股票价格信息
    """
    # 这里可以调用实际的股票API来获取数据
    return f"{stock_symbol}的当前价格是100美元。"


@tool
def search_news(query: str) -> str:
    """
    搜索与查询相关的新闻信息
    Args:
        query (str): 搜索查询
    Returns:
        str: 新闻信息
    """
    # 这里可以调用实际的新闻API来获取数据
    return f"与'{query}'相关的最新新闻是：APPLE将会与Google展开激烈竞争。"


model_bind_tool = deepseek_llm.bind_tools([get_stock_price, search_news])

messages = []
# Construct the conversation with the human message
human_message = HumanMessage(content="苹果公司的股票价格是多少和最新的新闻是什么？")
messages.append(human_message)

while True:
    response = model_bind_tool.invoke(messages)
    # add the model's response to the conversation history
    messages.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            # tools多了之后这种写法就不太好维护了，所以可以使用agent，参考01_agent_demo1.py
            if tool_call["name"] == "get_stock_price":
                # 3. 根据返回结果手动处理，并将结果告知LLM
                tool_result = get_stock_price.invoke(tool_call)
                # 4. LLM根据工具函数的返回结果继续进行对话或生成内容
                messages.append(tool_result)
            elif tool_call["name"] == "search_news":
                tool_result = search_news.invoke(tool_call)
                messages.append(tool_result)
    else:
        print("No more tool calls, final response:")
        break

print(f"messages:{messages}")
print(response.content)
