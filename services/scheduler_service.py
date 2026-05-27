"""Планировщик — фоновый поток для отправки напоминаний"""

import time
import threading
from datetime import datetime
from typing import Callable
from storage.reminder_repository import reminder_repo
from config import config


class SchedulerService:
    """Сервис для фоновой отправки напоминаний"""
    
    def __init__(self, vk, send_callback: Callable):
        """
        send_callback: функция, которая отправляет сообщение пользователю
        """
        self.vk = vk
        self.send_callback = send_callback
        self.running = False
        self.thread = None
    
    def start(self):
        """Запустить планировщик в фоновом потоке"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("🕐 Планировщик запущен")
    
    def stop(self):
        """Остановить планировщик"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🕐 Планировщик остановлен")
    
    def _run(self):
        """Основной цикл планировщика"""
        while self.running:
            try:
                current_timestamp = int(datetime.now().timestamp())
                due_reminders = reminder_repo.get_due(current_timestamp)
                
                for reminder in due_reminders:
                    # Отправляем напоминание
                    success = self.send_callback(self.vk,
                        user_id=reminder.user_id,
                        text=f"🔔 Напоминание: {reminder.text}"
                    )
                    
                    # Если отправили успешно — помечаем как отправленное
                    if success:
                        reminder_repo.mark_as_sent(reminder.id)
                
            except Exception as e:
                print(f"Ошибка в планировщике: {e}")
            
            time.sleep(config.SCHEDULER_INTERVAL)