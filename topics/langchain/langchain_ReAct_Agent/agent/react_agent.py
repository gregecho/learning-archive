from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from model.factory import chat_model
from utils.prompt_loader import get_system_prompts
from agent.tools.agent_tools import (
    rag_summarize,
    get_weather,
    get_user_location,
    get_user_id,
    get_current_month,
    fetch_external_data,
    fill_context_for_report,
)
from agent.tools.middleware import monitor_tool, log_before_model, report_prompt_switch


class ReactAgent:
    def __init__(self) -> None:
        self.agent = create_agent(
            model=chat_model,
            system_prompt=get_system_prompts(),
            tools=[
                rag_summarize,
                get_weather,
                get_user_location,
                get_user_id,
                get_current_month,
                fetch_external_data,
                fill_context_for_report,
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch],
        )

    def execute_stream(self, query: str):
        input_message = {
            "role": "user",
            "content": query,
        }
        config: RunnableConfig = {"configurable": {"thread_id": "some_id"}}

        for chunk in self.agent.stream(
            {"messages": [input_message]}, stream_mode="values", config=config
        ):
            latest_msg = chunk["messages"][-1]
            if latest_msg.content:
                yield f"{latest_msg.content}\n"


if __name__ == "__main__":
    agent = ReactAgent()

    # for chunk in agent.execute_stream("扫地机器人在我所在地区气温下如何保养"):
    for chunk in agent.execute_stream("生成我的使用报告"):

        print(chunk, end="", flush=True)
