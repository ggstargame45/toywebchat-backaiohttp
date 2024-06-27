import redis
import json
from app.domain.entities import ChatMessage


class RedisRepository:
    def __init__(self, redis_url: str):
        self.redis = redis.Redis.from_url(redis_url)

    def save_message(self, chat_message: ChatMessage):
        self.redis.rpush('chat_messages', json.dumps(chat_message.to_dict()))

    def get_messages(self):
        messages = self.redis.lrange('chat_messages', 0, -1)
        return [ChatMessage.from_dict(json.loads(msg.decode('utf-8'))) for msg in messages]

    def delete_all_messages(self):
        self.redis.delete('chat_messages')
