"""Главный парсер времени — координирует regex и hors"""

from datetime import datetime
from typing import Optional
from parsers.regex_parser import RegexTimeParser
from parsers.hors_parser import HorsTimeParser


def parse_reminder_time(text: str) -> Optional[datetime]:
    """
    Главная функция парсинга времени из текста.
    Стратегия: сначала regex (быстро, контролируемо), потом hors (для сложных случаев).
    
    Примеры:
        "через 10 минут позвонить" -> datetime (сейчас + 10 минут)
        "в 15:30 встреча" -> datetime (сегодня в 15:30)
        "завтра в 10:00 купить хлеб" -> datetime (завтра в 10:00)
        "в пятницу в 14:00" -> datetime (ближайшая пятница в 14:00) — через hors
    """
    if not text or not isinstance(text, str):
        return None
    
    # Уровень 1: регулярные выражения (быстро и предсказуемо)
    dt = RegexTimeParser.parse(text)
    if dt:
        return dt
    
    # Уровень 2: hors (для сложных случаев)
    dt = HorsTimeParser.parse(text)
    if dt:
        return dt
    
    # Ничего не распознали
    return None


def format_reminder_time(dt: datetime) -> str:
    """Форматирует datetime для отображения пользователю"""
    now = datetime.now()
    
    if dt.date() == now.date():
        return f"сегодня в {dt.strftime('%H:%M')}"
    elif dt.date() == now.date() + timedelta(days=1):
        return f"завтра в {dt.strftime('%H:%M')}"
    elif dt.date() == now.date() + timedelta(days=2):
        return f"послезавтра в {dt.strftime('%H:%M')}"
    else:
        return dt.strftime("%d.%m.%Y в %H:%M")


# Импорт нужен для format_reminder_time
from datetime import timedelta