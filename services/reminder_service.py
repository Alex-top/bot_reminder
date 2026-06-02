"""Бизнес-логика работы с напоминаниями"""

from datetime import datetime
from typing import Optional, List
from models.reminder import Reminder
from storage.reminder_repository import reminder_repo
from parsers.time_parser import parse_reminder_time
from config import config
from utils.logger import BotLogger

logger = BotLogger.get_logger(__name__)


class ReminderService:
    """Сервис для управления напоминаниями"""
    
    def create_reminder(self, user_id: int, text: str) -> Optional[Reminder]:
        """
        Создать напоминание из текста.
        Возвращает Reminder или None, если время не распознано.
        """
        # Проверка лимита
        count = reminder_repo.count_by_user(user_id)
        if count >= config.MAX_REMINDERS_PER_USER:
            logger.warning(f"Пользователь {user_id} превысил лимит напоминаний ({count}/{config.MAX_REMINDERS_PER_USER})")
            return None  # или raise исключение
        
        # Парсим время из текста
        execute_at = parse_reminder_time(text)
        if not execute_at:
            logger.debug(f"Не удалось распознать время в сообщении: {text}")
            return None
        
        # Извлекаем сам текст напоминания (без временной части)
        reminder_text = self._extract_reminder_text(text)
        
        reminder = Reminder(
            user_id=user_id,
            text=reminder_text,
            execute_at=execute_at,
            created_at=datetime.now(),
            is_sent=False,
            is_cancelled=False
        )
        
        reminder_id = reminder_repo.create(reminder)
        reminder.id = reminder_id
        
        logger.info(f"Создано напоминание #{reminder_id} для {user_id} на {execute_at}")
        return reminder
    
    def cancel_reminder(self, user_id: int, reminder_id: int) -> bool:
        """Отменить напоминание"""
        return reminder_repo.cancel(reminder_id, user_id)
    
    def get_user_reminders(self, user_id: int) -> List[Reminder]:
        """Получить все активные напоминания пользователя"""
        return reminder_repo.get_by_user(user_id)
    
    def _extract_reminder_text(self, full_text: str) -> str:
        """Извлечь текст напоминания, убрав временную часть"""
        # Упрощённая версия. Можно улучшить.
        # Удаляем слова "напомни", "через", "в" и т.д.
        # Для MVP можно просто вернуть full_text
        return full_text


reminder_service = ReminderService()