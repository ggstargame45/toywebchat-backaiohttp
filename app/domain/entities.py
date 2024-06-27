from dataclasses import dataclass
from datetime import datetime

@dataclass
class ChatMessage:
    username: str
    message: str
    sent_at: datetime

    def to_dict(self):
        return {
            "username": self.username,
            "message": self.message,
            "sentAt": self.sent_at.isoformat()
        }

    @staticmethod
    def from_dict(data : dict):
        return ChatMessage(
            username=data['username'],
            message=data['message'],
            sent_at=datetime.fromisoformat(data['sentAt'])
        )
