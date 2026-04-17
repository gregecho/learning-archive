from typing import Callable

from langchain.agents.middleware import (
    AgentState,
    ModelRequest,
    Runtime,
    before_model,
    dynamic_prompt,
    wrap_tool_call,
)
from langchain.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.types import Command
from utils.logger_handler import logger
from utils.prompt_loader import get_report_prompts, get_system_prompts


@wrap_tool_call
def monitor_tool(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    """工具执行的监控

    Args:
        request (ToolCallRequest): 请求数据的封装
        handler (Callable[[ToolCallRequest], ToolMessage  |  Command]): 执行的函数本身

    Returns:
        ToolMessage | Command: _description_
    """
    logger.info(f"[Tool Monitor]执行工具: {request.tool_call['name']}")
    logger.info(f"[Tool Monitor]执行参数: {request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[Tool Monitor]工具: {request.tool_call['name']}调用成功")

        tool_name = request.tool_call["name"] if request.tool_call else None
        if tool_name == "fill_context_for_report":
            context = getattr(request.runtime, "context", {}) or {}
            context["report"] = True

        return result
    except Exception as e:
        logger.error(
            f"[Tool Monitor]工具{request.tool_call['name']}调用失败，原因: {str(e)}"
        )
        raise e


@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    """模型执行前输出日志

    Args:
        state (AgentState): 整个Agent智能体中的状态记录
        runtime (Runtime): 整个执行过程中的上下文信息
    """
    logger.info(f"[log_before_model]即将调用模型: 带有{len(state['messages'])}条信息")
    content_preview = str(state["messages"][-1].content).strip()
    logger.debug(
        f"[log_before_model]{type(state['messages'][-1]).__name__} | {content_preview}"
    )

    return None


@dynamic_prompt  # 在每一次生成提示此之前，会调用带有该装饰器的方法
def report_prompt_switch(request: ModelRequest):
    """动态切换提示词

    Args:
        request (ModelRequest): Agent的模型请求信息
    """
    is_report = (request.runtime.context or {}).get("report", False)
    if is_report:
        return get_report_prompts()

    return get_system_prompts()
