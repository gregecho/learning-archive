from collections.abc import Sequence
import json
import os
from langchain_core.messages import messages_from_dict, message_to_dict
from langchain_core.messages import BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
import config_data as config


def get_history(session_id: str):
    return FileChatMessageHistory(
        session_id=session_id, storage_path=config.chat_message_store_path
    )


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str) -> None:
        self.session_id = session_id
        self.storage_path = storage_path
        # 完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    # 重写父类的属性，实现读取逻辑
    @property
    def messages(self) -> list[BaseMessage]:  # type: ignore
        """重写父类的属性，实现读取逻辑"""
        file_path = os.path.join(self.storage_path, self.session_id)
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)
            return messages_from_dict(messages_data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # Existing messages
        all_messages.extend(messages)  # Add new messages

        # 将消息列表转换为字典列表并保存到文件中
        new_messages = [message_to_dict(message) for message in all_messages]
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    def clear(self) -> None:
        file_path = os.path.join(self.storage_path, self.session_id)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
