"""Обработчик нажатий на кнопки (callback'ов)"""

from typing import Dict, Any
from services.reminder_service import reminder_service
from utils.formatters import format_reminder_list
from utils.logger import BotLogger

logger = BotLogger.get_logger(__name__)


class CallbackHandler:
    """Обработчик callback-событий от кнопок"""
    
    def __init__(self, vk):
        self.vk = vk
    
    def handle(self, user_id: int, payload: Dict[str, Any]) -> str:
        """
        Обрабатывает callback и возвращает текст ответа.
        
        Args:
            user_id: ID пользователя
            payload: Словарь с данными из кнопки
        
        Returns:
            str: Текст ответа для пользователя
        """
        action = payload.get('action')
        
        logger.debug(f"Callback от {user_id}: action={action}, payload={payload}")
        
        if action == 'cancel_reminder':
            reminder_id = payload.get('reminder_id')
            return self._cancel_reminder(user_id, reminder_id)
        
        elif action == 'confirm_cancel_all':
            return self._cancel_all_reminders(user_id)
        
        elif action == 'confirm_cancel_one':
            reminder_id = payload.get('reminder_id')
            return self._confirm_cancel_one(user_id, reminder_id)
        
        elif action == 'cancel_confirm':
            return "✅ Действие отменено."
        
        elif action == 'quick_reminder':
            delay_minutes = payload.get('delay_minutes')
            return self._create_quick_reminder(user_id, delay_minutes)
        
        else:
            logger.warning(f"Неизвестное действие callback: {action}")
            return "❌ Неизвестное действие."
    
    def _cancel_reminder(self, user_id: int, reminder_id: int) -> str:
        """Отмена одного напоминания"""
        success = reminder_service.cancel_reminder(user_id, reminder_id)
        
        if success:
            return f"✅ Напоминание #{reminder_id} отменено."
        else:
            return f"❌ Напоминание #{reminder_id} не найдено или уже отправлено."
    
    def _cancel_all_reminders(self, user_id: int) -> str:
        """Отмена всех напоминаний"""
        reminders = reminder_service.get_user_reminders(user_id)
        
        if not reminders:
            return "📭 У вас нет активных напоминаний."
        
        cancelled_count = 0
        for reminder in reminders:
            if reminder_service.cancel_reminder(user_id, reminder.id):
                cancelled_count += 1
        
        return f"✅ Отменено напоминаний: {cancelled_count} из {len(reminders)}."
    
    def _confirm_cancel_one(self, user_id: int, reminder_id: int) -> str:
        """Подтверждение отмены одного напоминания через кнопку"""
        return self._cancel_reminder(user_id, reminder_id)
    
    def _create_quick_reminder(self, user_id: int, delay_minutes: int) -> str:
        """Быстрое создание напоминания через кнопку"""
        from datetime import datetime, timedelta
        from models.reminder import Reminder
        from storage.reminder_repository import reminder_repo
        
        # Проверка лимита
        count = reminder_repo.count_by_user(user_id)
        if count >= 50:  # config.MAX_REMINDERS_PER_USER
            return "❌ Превышен лимит активных напоминаний (50). Отмените ненужные."
        
        execute_at = datetime.now() + timedelta(minutes=delay_minutes)
        reminder_text = f"напоминание через {delay_minutes} минут"
        
        reminder = Reminder(
            user_id=user_id,
            text=reminder_text,
            execute_at=execute_at,
            created_at=datetime.now()
        )
        
        reminder_id = reminder_repo.create(reminder)
        reminder.id = reminder_id
        
        return f"✅ Напомню через {delay_minutes} минут (ID: {reminder_id})"
    
    def format_reminder_list_with_buttons(self, user_id: int) -> tuple:
        """
        Форматирует список напоминаний с кнопками для отмены.
        Возвращает (текст_сообщения, клавиатура)
        """
        from handlers.keyboards import BotKeyboards
        
        reminders = reminder_service.get_user_reminders(user_id)
        
        if not reminders:
            return "📭 У вас нет активных напоминаний.", None
        
        lines = ["📋 *Ваши напоминания:*"]
        
        for i, reminder in enumerate(reminders, 1):
            from parsers.time_parser import format_reminder_time
            time_str = format_reminder_time(reminder.execute_at)
            lines.append(f"{i}. {time_str}: \"{reminder.text}\" (ID: {reminder.id})")
        
        lines.append("\n💡 Нажмите на кнопку под напоминанием, чтобы отменить его.")
        
        return "\n".join(lines), BotKeyboards.get_reminder_actions_keyboard(reminders[0].id)