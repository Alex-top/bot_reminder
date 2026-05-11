"""Модель данных напоминания"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Reminder:
    """Напоминание"""
    
    id: Optional[int] = None
    user_id: int = 0
    text: str = ""
    execute_at: datetime = None
    created_at: datetime = None
    is_sent: bool = False
    is_cancelled: bool = False
    
    def to_dict(self) -> dict:
        """Преобразование в словарь для БД"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "text": self.text,
            "execute_at": int(self.execute_at.timestamp()) if self.execute_at else 0,
            "created_at": int(self.created_at.timestamp()) if self.created_at else 0,
            "is_sent": 1 if self.is_sent else 0,
            "is_cancelled": 1 if self.is_cancelled else 0,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Reminder":
        """Создание из словаря БД"""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id", 0),
            text=data.get("text", ""),
            execute_at=datetime.fromtimestamp(data.get("execute_at", 0)),
            created_at=datetime.fromtimestamp(data.get("created_at", 0)),
            is_sent=bool(data.get("is_sent", 0)),
            is_cancelled=bool(data.get("is_cancelled", 0)),
        )