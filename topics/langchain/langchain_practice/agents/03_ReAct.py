from langchain.agents import create_agent
from pathlib import Path
import sys

from langchain_core.tools import tool
from requests import get

# Add the workspace root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
from init_llm import deepseek_llm


@tool(description="获取体重,单位为kg")
def get_weight() -> int:
    return 90


@tool(description="获取身高,单位为cm")
def get_height() -> int:
    return 180


agent = create_agent(
    deepseek_llm,
    tools=[get_weight, get_height],
    system_prompt="""你是严格遵守ReAct原则的智能助手，必须按照[思考->行动->观察->再思考]的流程解决问题，
     并告知我你的思考过程，工具调用的原因，按照思考行动观察三个结构告知我。""",
)

chunks = agent.stream(
    {"messages": [{"role": "user", "content": "计算我的BMI指数。"}]},
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
