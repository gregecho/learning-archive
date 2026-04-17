from abc import ABC, abstractmethod
from typing import Optional

from dashscope import api_key
from langchain.chat_models import BaseChatModel, init_chat_model
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from pydantic import SecretStr
from utils.config_handler import rag_conf
from utils.env_utils import DASHSCOPE_API_KEY, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> BaseChatModel:
        return init_chat_model(
            model=rag_conf["chat_model_name"],
            model_provider=rag_conf["model_provider"],
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )


class EmbeddingsModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings]:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
        )


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsModelFactory().generator()
