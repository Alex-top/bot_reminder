"""Модуль для логирования событий бота"""

import logging
import os
from datetime import datetime
from typing import Optional


class BotLogger:
    """
    Класс для логирования работы бота.
    Поддерживает вывод в консоль и запись в файл.
    
    Уровни логирования:
    - DEBUG: детальная отладка (парсинг времени, состояния)
    - INFO: обычные события (бот запущен, получено сообщение)
    - WARNING: не критичные проблемы (не распознано время)
    - ERROR: ошибки (не отправилось сообщение)
    """
    
    def __init__(self, name: str = "bot", log_file: Optional[str] = "bot.log"):
        """
        Инициализация логгера.
        
        Args:
            name: Имя логгера (обычно имя модуля)
            log_file: Путь к файлу лога (None = не писать в файл)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Формат сообщения: [ВРЕМЯ] [УРОВЕНЬ] ИМЯ - СООБЩЕНИЕ
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Вывод в консоль (всегда)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Вывод в файл (опционально)
        if log_file:
            # Создаём папку для логов, если её нет
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)  # В файл пишем только INFO и выше
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Для отладки (не пишет в файл по умолчанию)"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Для обычных событий"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Для предупреждений"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Для ошибок"""
        self.logger.error(message)
    
    @staticmethod
    def get_logger(name: str, log_file: Optional[str] = "bot.log") -> 'BotLogger':
        """
        Удобный метод для получения логгера.
        Используется как альтернатива прямому созданию.
        
        Пример:
            logger = BotLogger.get_logger(__name__)
            logger.info("Сообщение")
        """
        return BotLogger(name, log_file)