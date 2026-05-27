"""CRUD операции с напоминаниями"""

from datetime import datetime
from typing import List, Optional
from storage.database import database
from models.reminder import Reminder


class ReminderRepository:
    """Репозиторий для работы с напоминаниями в БД"""
    
    def create(self, reminder: Reminder) -> int:
        """Создать новое напоминание, вернуть ID"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reminders (user_id, text, execute_at, created_at, is_sent, is_cancelled)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                reminder.user_id,
                reminder.text,
                int(reminder.execute_at.timestamp()),
                int(reminder.created_at.timestamp()),
                0, 0
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_pending(self) -> List[Reminder]:
        """Получить все неотправленные и неотменённые напоминания"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE is_sent = 0 AND is_cancelled = 0
                ORDER BY execute_at ASC
            """)
            return [Reminder.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def get_due(self, current_timestamp: int) -> List[Reminder]:
        """Получить напоминания, которые пора отправлять"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE execute_at <= ? 
                AND is_sent = 0 
                AND is_cancelled = 0
                ORDER BY execute_at ASC
            """, (current_timestamp,))
            return [Reminder.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def mark_as_sent(self, reminder_id: int):
        """Пометить напоминание как отправленное"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reminders SET is_sent = 1 
                WHERE id = ?
            """, (reminder_id,))
            conn.commit()
    
    def cancel(self, reminder_id: int, user_id: int) -> bool:
        """Отменить напоминание (только своё)"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reminders SET is_cancelled = 1 
                WHERE id = ? AND user_id = ? AND is_sent = 0
            """, (reminder_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_by_user(self, user_id: int) -> List[Reminder]:
        """Получить активные напоминания пользователя"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM reminders 
                WHERE user_id = ? AND is_sent = 0 AND is_cancelled = 0
                ORDER BY execute_at ASC
            """, (user_id,))
            return [Reminder.from_dict(dict(row)) for row in cursor.fetchall()]
    
    def count_by_user(self, user_id: int) -> int:
        """Подсчитать активные напоминания пользователя"""
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count FROM reminders 
                WHERE user_id = ? AND is_sent = 0 AND is_cancelled = 0
            """, (user_id,))
            return cursor.fetchone()["count"]


reminder_repo = ReminderRepository()