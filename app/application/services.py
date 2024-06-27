from datetime import datetime
from app.domain.entities import ChatMessage
from app.infrastructure.redis_repository import RedisRepository


class ChatService:
    def __init__(self, repository : RedisRepository):
        self.repository = repository

    def save_message(self, username : str, message : str):
        chat_message = ChatMessage(username=username, message=message, sent_at=datetime.now())
        self.repository.save_message(chat_message)
        return chat_message

    def get_messages(self):
        return self.repository.get_messages()

    def delete_all_messages(self):
        self.repository.delete_all_messages()