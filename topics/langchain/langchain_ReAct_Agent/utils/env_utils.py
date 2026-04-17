import os
from dotenv import load_dotenv

load_dotenv(override=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

ALI_API_KEY = os.getenv("ALI_API_KEY")
ALI_BASE_URL = os.getenv("ALI_BASE_URL")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
