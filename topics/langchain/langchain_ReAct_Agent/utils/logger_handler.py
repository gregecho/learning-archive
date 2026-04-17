from datetime import datetime
import logging
from math import log
from os import makedirs
import os
from venv import logger
from utils.path_tool import get_absolute_path

LOG_ROOT = get_absolute_path("logs")
makedirs(LOG_ROOT, exist_ok=True)

DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)


def get_logger(
    name: str = "agent",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file=None,
) -> logging.Logger:
    """获取日志记录器，默认日志级别为INFO，文件日志级别为DEBUG"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置最低日志级别为DEBUG

    if logger.handlers:
        return logger  # 如果已经有处理器，直接返回

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    # 创建文件处理器
    if not log_file:
        log_file = os.path.join(
            LOG_ROOT, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 全局日志记录器实例
logger = get_logger()

if __name__ == "__main__":
    # 测试日志记录器
    logger.debug("这是一个调试日志")
    logger.info("这是一个信息日志")
    logger.warning("这是一个警告日志")
    logger.error("这是一个错误日志")
    logger.critical("这是一个严重错误日志")
