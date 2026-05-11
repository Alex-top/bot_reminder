"""Тесты для репозитория напоминаний"""

import pytest
import tempfile
import os
from datetime import datetime, timedelta
from storage.database import Database
from storage.reminder_repository import ReminderRepository
from models.reminder import Reminder


@pytest.fixture
def temp_db():
    """Фикстура: временная БД для тестов"""
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    # Подменяем путь к БД
    original_path = Database.db_path
    Database.db_path = path
    Database._init_db()
    
    yield path
    
    Database.db_path = original_path
    os.unlink(path)


@pytest.fixture
def repo(temp_db):
    """Фикстура: репозиторий с временной БД"""
    return ReminderRepository()


class TestReminderRepository:
    """Тесты для репозитория"""
    
    def test_create_and_get(self, repo):
        """Тест: создание и получение напоминания"""
        reminder = Reminder(
            user_id=123456,
            text="Тестовое напоминание",
            execute_at=datetime.now() + timedelta(minutes=30),
            created_at=datetime.now()
        )
        
        reminder_id = repo.create(reminder)
        assert reminder_id is not None
        assert reminder_id > 0
        
        # Проверяем, что добавилось
        pending = repo.get_pending()
        assert len(pending) == 1
        assert pending[0].user_id == 123456
        assert pending[0].text == "Тестовое напоминание"
    
    def test_mark_as_sent(self, repo):
        """Тест: пометка отправленного"""
        reminder = Reminder(
            user_id=123456,
            text="Тест",
            execute_at=datetime.now() + timedelta(minutes=30),
            created_at=datetime.now()
        )
        reminder_id = repo.create(reminder)
        
        repo.mark_as_sent(reminder_id)
        
        pending = repo.get_pending()
        assert len(pending) == 0
    
    def test_get_due(self, repo):
        """Тест: получение просроченных напоминаний"""
        # Создаем напоминание в прошлом
        reminder = Reminder(
            user_id=123456,
            text="Просроченное",
            execute_at=datetime.now() - timedelta(minutes=10),
            created_at=datetime.now()
        )
        repo.create(reminder)
        
        due = repo.get_due(int(datetime.now().timestamp()))
        assert len(due) == 1
        assert due[0].text == "Просроченное"
    
    def test_cancel(self, repo):
        """Тест: отмена напоминания"""
        reminder = Reminder(
            user_id=123456,
            text="Отменяемое",
            execute_at=datetime.now() + timedelta(minutes=30),
            created_at=datetime.now()
        )
        reminder_id = repo.create(reminder)
        
        # Отмена своим пользователем
        success = repo.cancel(reminder_id, 123456)
        assert success is True
        
        # Проверяем, что не в pending
        pending = repo.get_pending()
        assert len(pending) == 0
        
        # Чужой пользователь не может отменить
        reminder = Reminder(
            user_id=123456,
            text="Другое",
            execute_at=datetime.now() + timedelta(minutes=30),
            created_at=datetime.now()
        )
        reminder_id = repo.create(reminder)
        
        success = repo.cancel(reminder_id, 999999)  # чужой ID
        assert success is False
    
    def test_count_by_user(self, repo):
        """Тест: подсчет напоминаний пользователя"""
        for i in range(3):
            reminder = Reminder(
                user_id=123456,
                text=f"Тест {i}",
                execute_at=datetime.now() + timedelta(minutes=30),
                created_at=datetime.now()
            )
            repo.create(reminder)
        
        count = repo.count_by_user(123456)
        assert count == 3
        
        count_other = repo.count_by_user(999999)
        assert count_other == 0