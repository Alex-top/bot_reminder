"""Парсинг времени через библиотеку hors (сложный уровень)"""

from datetime import datetime
from typing import Optional

try:
    import hors
    HORS_AVAILABLE = True
except ImportError:
    HORS_AVAILABLE = False
    print("⚠️ Библиотека hors не установлена. Установите: pip install hors")


class HorsTimeParser:
    """Парсинг времени с помощью hors (поддержка русского языка)"""
    
    @staticmethod
    def parse(text: str) -> Optional[datetime]:
        """
        Пытается распознать время с помощью библиотеки hors.
        Возвращает datetime или None.
        """
        if not HORS_AVAILABLE:
            return None
        
        try:
            result = hors.process_phrase(text.lower())
            
            if result.dates:
                # Берем первую найденную дату
                for date_obj in result.dates:
                    # type 1 = FIXED (конкретная дата)
                    if hasattr(date_obj, 'type') and date_obj.type == 1:
                        if hasattr(date_obj, 'date_from') and date_obj.date_from:
                            dt = date_obj.date_from
                            if isinstance(dt, datetime):
                                # Проверяем, что дата не в прошлом
                                if dt > datetime.now():
                                    return dt
                            # Если это date (без времени) — дополняем временем
                            elif hasattr(dt, 'year'):
                                from datetime import timedelta
                                default_time = datetime.now().replace(
                                    hour=9, minute=0, second=0, microsecond=0
                                )
                                combined = datetime(
                                    dt.year, dt.month, dt.day,
                                    default_time.hour, default_time.minute
                                )
                                if combined > datetime.now():
                                    return combined
            
            return None
            
        except Exception as e:
            print(f"Ошибка hors: {e}")
            return None