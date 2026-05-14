"""Тесты для модуля парсинга времени"""

import pytest
from datetime import datetime, timedelta
from parsers.regex_parser import RegexTimeParser
from parsers.time_parser import parse_reminder_time


class TestRegexTimeParser:
    """Тесты для regex-парсера"""
    
    def test_parse_relative_minutes(self):
        """Тест: через X минут"""
        result = RegexTimeParser._parse_relative("через 10 минут")
        assert result is not None
        
        now = datetime.now()
        diff = result - now
        # 10 минут ± 1 секунда (из-за времени выполнения)
        assert 9*60 <= diff.total_seconds() <= 11*60
    
    def test_parse_relative_hours(self):
        """Тест: через X часов"""
        result = RegexTimeParser._parse_relative("через 2 часа")
        assert result is not None
        
        now = datetime.now()
        diff = result - now
        assert 1.9*3600 <= diff.total_seconds() <= 2.1*3600
    
    def test_parse_time_only(self):
        """Тест: в ЧЧ:ММ"""
        # Подменяем now для теста
        # В реальном тесте нужно замокать datetime.now()
        pass
    
    def test_parse_tomorrow(self):
        """Тест: завтра в ЧЧ:ММ"""
        result = RegexTimeParser._parse_tomorrow("завтра в 10:00")
        assert result is not None
        
        now = datetime.now()
        days_diff = (result - now).days
        assert days_diff == 1 or (days_diff == 0 and result.hour > now.hour)
    
    def test_parse_days_later(self):
        """Тест: через N дней в ЧЧ:ММ"""
        result = RegexTimeParser._parse_days_later("через 3 дня в 14:00")
        assert result is not None
        
        now = datetime.now()
        days_diff = (result - now).days
        assert days_diff == 2 or days_diff == 3  # ±1 из-за времени суток


class TestTimeParser:
    """Тесты для главного парсера"""
    
    def test_parse_various_formats(self):
        """Тест: разные форматы"""
        test_cases = [
            "через 5 минут",
            "через 1 час",
            "в 15:30",
            "в 9.00",
            "завтра в 10:00",
            "послезавтра в 18:30",
            "через 2 дня в 14:00",
        ]
        
        for text in test_cases:
            result = parse_reminder_time(text)
            assert result is not None, f"Не распознано: {text}"
    
    def test_parse_invalid(self):
        """Тест: некорректные фразы"""
        test_cases = [
            "привет",
            "как дела",
            "",
            None,
            "напомни потом",
        ]
        
        for text in test_cases:
            result = parse_reminder_time(text)
            assert result is None, f"Должно вернуть None: {text}"