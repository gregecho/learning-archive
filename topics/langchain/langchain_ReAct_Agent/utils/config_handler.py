import yaml
from utils.path_tool import get_absolute_path


def get_rag_config(
    config_path: str = "config/rag.yaml", encoding: str = "utf-8"
) -> dict:
    """从yaml文件读取RAG配置"""
    with open(get_absolute_path(config_path), "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_chroma_config(
    config_path: str = "config/chroma.yaml", encoding: str = "utf-8"
) -> dict:
    """从yaml文件读取Chroma配置"""
    with open(get_absolute_path(config_path), "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_agent_config(
    config_path: str = "config/agent.yaml", encoding: str = "utf-8"
) -> dict:
    """从yaml文件读取Agent配置"""
    with open(get_absolute_path(config_path), "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_prompts_config(
    config_path: str = "config/prompts.yaml", encoding: str = "utf-8"
) -> dict:
    """从yaml文件读取prompt配置"""
    with open(get_absolute_path(config_path), "r", encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


# 全局配置实例
rag_conf = get_rag_config()
chroma_conf = get_chroma_config()
agent_conf = get_agent_config()
prompts_conf = get_prompts_config()

if __name__ == "__main__":
    print(agent_conf["chat_model_name"])
