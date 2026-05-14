"""Парсинг времени через регулярные выражения (простой уровень)"""

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple


class RegexTimeParser:
    """Парсинг времени с помощью регулярных выражений"""
    
    @staticmethod
    def parse(text: str) -> Optional[datetime]:
        """
        Пытается распознать время в тексте с помощью regex.
        Возвращает datetime или None.
        """
        text = text.lower().strip()
        
        # Порядок важен: от более специфичных к общим
        patterns = [
            # "через 10 минут" / "через 1 час"
            RegexTimeParser._parse_relative,
            # "завтра в 10:00" / "послезавтра в 18:30"
            RegexTimeParser._parse_tomorrow,
            # "через 2 дня в 14:00"
            RegexTimeParser._parse_days_later,
            # "в 15:30" / "в 9.00"
            RegexTimeParser._parse_time_only,
        ]
        
        for parse_func in patterns:
            result = parse_func(text)
            if result:
                return result
        
        return None
    
    @staticmethod
    def _parse_relative(text: str) -> Optional[datetime]:
        """Парсинг: через 10 минут, через 2 часа"""
        
        # Паттерн для минут
        match_minutes = re.search(r'через\s+(\d+)\s*(?:минут|мин|минуты|минуту)', text)
        if match_minutes:
            minutes = int(match_minutes.group(1))
            return datetime.now() + timedelta(minutes=minutes)
        
        # Паттерн для часов
        match_hours = re.search(r'через\s+(\d+)\s*(?:час|часов|часа)', text)
        if match_hours:
            hours = int(match_hours.group(1))
            return datetime.now() + timedelta(hours=hours)
        
        return None
    
    @staticmethod
    def _parse_time_only(text: str) -> Optional[datetime]:
        """Парсинг: в 15:30, в 9.00"""
        
        # "в 15:30" или "в 15.30"
        match = re.search(r'в\s+(\d{1,2})[:.](\d{2})', text)
        if not match:
            return None
        
        hour = int(match.group(1))
        minute = int(match.group(2))
        
        if hour > 23 or minute > 59:
            return None
        
        now = datetime.now()
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Если время уже прошло сегодня — переносим на завтра
        if reminder_time <= now:
            reminder_time += timedelta(days=1)
        
        return reminder_time
    
    @staticmethod
    def _parse_tomorrow(text: str) -> Optional[datetime]:
        """Парсинг: завтра в 10:00, послезавтра в 18:30"""
        
        # Завтра
        match = re.search(r'завтра\s+в\s+(\d{1,2})[:.](\d{2})', text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if hour <= 23 and minute <= 59:
                target_date = datetime.now() + timedelta(days=1)
                return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Послезавтра
        match = re.search(r'послезавтра\s+в\s+(\d{1,2})[:.](\d{2})', text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if hour <= 23 and minute <= 59:
                target_date = datetime.now() + timedelta(days=2)
                return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        return None
    
    @staticmethod
    def _parse_days_later(text: str) -> Optional[datetime]:
        """Парсинг: через 2 дня в 14:00"""
        
        match = re.search(r'через\s+(\d+)\s+день|дня|дней\s+в\s+(\d{1,2})[:.](\d{2})', text)
        if not match:
            return None
        
        days = int(match.group(1))
        hour = int(match.group(2))
        minute = int(match.group(3))
        
        if hour > 23 or minute > 59:
            return None
        
        target_date = datetime.now() + timedelta(days=days)
        return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)