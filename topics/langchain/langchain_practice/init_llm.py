from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from env_utils import (
    ALI_API_KEY,
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    ANTHROPIC_BASE_URL,
    ANTHROPIC_API_KEY,
)

# 2. 通过统一方式调用

ali_llm = init_chat_model(
    model="qwen3-max",
    model_provider="openai",
    api_key=ALI_API_KEY,
    base_url=ALI_API_KEY,
)

anthropic_llm = init_chat_model(
    model="claude-3-5-sonnet-20241022",
    model_provider="anthropic",
    api_key=ANTHROPIC_API_KEY,
    base_url=ANTHROPIC_BASE_URL,
)

deepseek_llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

deepseek_embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    base_url=DEEPSEEK_BASE_URL,
)
