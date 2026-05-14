"""Загрузка конфигурации из переменных окружения"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""
    
    # VK
    VK_TOKEN = os.getenv("VK_TOKEN")
    VK_GROUP_ID = int(os.getenv("VK_GROUP_ID", 0))
    
    # Бот
    BOT_NAME = os.getenv("BOT_NAME", "ReminderBot")
    
    # База данных
    DATABASE_PATH = os.getenv("DATABASE_PATH", "reminders.db")
    
    # Планировщик
    SCHEDULER_INTERVAL = int(os.getenv("SCHEDULER_INTERVAL", 5))  # секунды
    
    # Лимиты
    MAX_REMINDERS_PER_USER = int(os.getenv("MAX_REMINDERS_PER_USER", 50))


config = Config()