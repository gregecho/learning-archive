from langchain.agents import create_agent
from pathlib import Path
import sys

from langchain_core.tools import tool
from requests import get

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from init_llm import deepseek_llm


@tool(description="获取股票价格")
def get_stock_price(stock_symbol: str) -> str:
    # 这里可以调用一个股票API来获取股票价格
    print(f"获取{stock_symbol}的股票价格...")
    return f"{stock_symbol}当前价格为100美元。"


@tool(description="获取股票信息")
def get_stock_info(stock_symbol: str) -> str:
    # 这里可以调用一个股票API来获取股票信息
    print(f"获取{stock_symbol}的股票信息...")
    return f"{stock_symbol}是一家科技公司，市值1000亿美元。"


agent = create_agent(
    deepseek_llm,
    tools=[get_stock_price, get_stock_info],
    system_prompt="你是一个智能聊天助手，可以回答股票相关问题，请告知我你的思考过程，让我知道你为什么调用某个工具。",
)

chunks = agent.stream(
    {"messages": [{"role": "user", "content": "请告诉我苹果公司的股票价格和信息。"}]},
    stream_mode="values",
)

for chunk in chunks:
    lastest_msg = chunk["messages"][-1]
    if lastest_msg.content:
        print(f"{type(lastest_msg).__name__}: {lastest_msg.content}")

    try:
        if lastest_msg.tool_calls:
            print(
                f"工具调用: {[tool_call['name'] for tool_call in lastest_msg.tool_calls]}"
            )
    except AttributeError as e:
        print(f"Error occurred: {e}")
        pass
