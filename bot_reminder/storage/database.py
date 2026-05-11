"""Инициализация и подключение к SQLite"""

import sqlite3
from contextlib import contextmanager
from config import config


class Database:
    """Менеджер подключения к БД"""
    
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Создание таблиц при первом запуске"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    text TEXT NOT NULL,
                    execute_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL,
                    is_sent INTEGER DEFAULT 0,
                    is_cancelled INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_execute_at 
                ON reminders(execute_at)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id 
                ON reminders(user_id)
            """)
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для соединения с БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()


database = Database()