"""Функции форматирования сообщений для пользователя"""

from datetime import datetime
from typing import List
from models.reminder import Reminder
from parsers.time_parser import format_reminder_time


def format_reminder_created(reminder: Reminder) -> str:
    """
    Форматирует сообщение об успешном создании напоминания.
    Пример: ✅ Напоминание создано! Напомню сегодня в 15:30: "встреча с клиентом"
    """
    time_str = format_reminder_time(reminder.execute_at)
    return f"✅ Напомню {time_str}: \"{reminder.text}\""


def format_reminder_list(reminders: List[Reminder]) -> str:
    """
    Форматирует список напоминаний.
    Пример:
    📋 *Ваши напоминания:*
    1. сегодня в 15:30: "встреча"
    2. завтра в 10:00: "купить хлеб"
    """
    if not reminders:
        return "📭 У вас нет активных напоминаний"
    
    lines = ["📋 *Ваши напоминания:*"]
    
    for i, reminder in enumerate(reminders, 1):
        time_str = format_reminder_time(reminder.execute_at)
        lines.append(f"{i}. {time_str}: \"{reminder.text}\" (ID: {reminder.id})")
    
    lines.append("\n💡 Чтобы отменить: `/cancel ID`")
    
    return "\n".join(lines)


def format_error(message: str) -> str:
    """Форматирует сообщение об ошибке"""
    return f"❌ {message}"