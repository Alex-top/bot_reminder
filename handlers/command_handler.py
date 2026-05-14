"""Обработчик команд (/list, /cancel, /cancel_all)"""

from services.reminder_service import reminder_service
from utils.formatters import format_reminder_list


class CommandHandler:
    """Обработчик команд бота"""
    
    def __init__(self, vk_api_instance):
        self.vk = vk_api_instance
    
    def handle(self, user_id: int, command_text: str) -> str:
        """
        Обрабатывает команду и возвращает ответ.
        Команды: /list, /cancel N, /cancel_all, /help, /start
        """
        command_text = command_text.lower().strip()
        
        if command_text == "/start" or command_text == "/help":
            return self._get_help()
        
        elif command_text == "/list":
            return self._list_reminders(user_id)
        
        elif command_text.startswith("/cancel "):
            # /cancel 5
            parts = command_text.split()
            if len(parts) == 2 and parts[1].isdigit():
                reminder_id = int(parts[1])
                return self._cancel_reminder(user_id, reminder_id)
            else:
                return "❌ Использование: `/cancel номер`\nНомер можно посмотреть в `/list`"
        
        elif command_text == "/cancel_all":
            return self._cancel_all_reminders(user_id)
        
        else:
            return f"❌ Неизвестная команда: `{command_text}`\nВведите `/help` для списка команд"
    
    def _get_help(self) -> str:
        return """🤖 *Бот-напоминание*

📝 *Как создать напоминание:*
• `через 10 минут позвонить`
• `в 15:30 встреча`
• `завтра в 10:00 купить хлеб`
• `через 2 дня в 14:00 важное дело`

📋 *Команды:*
`/list` — список активных напоминаний
`/cancel [номер]` — отменить напоминание
`/cancel_all` — отменить все напоминания
`/help` — эта справка

💡 *Пример:* `/cancel 3` — отменит напоминание под номером 3
"""
    
    def _list_reminders(self, user_id: int) -> str:
        """Показать список напоминаний пользователя"""
        reminders = reminder_service.get_user_reminders(user_id)
        
        if not reminders:
            return "📭 У вас нет активных напоминаний.\n\nСоздайте новое: например, `через 10 минут позвонить`"
        
        return format_reminder_list(reminders)
    
    def _cancel_reminder(self, user_id: int, reminder_id: int) -> str:
        """Отменить одно напоминание"""
        success = reminder_service.cancel_reminder(user_id, reminder_id)
        
        if success:
            return f"✅ Напоминание #{reminder_id} отменено"
        else:
            return f"❌ Напоминание #{reminder_id} не найдено или уже было отправлено"
    
    def _cancel_all_reminders(self, user_id: int) -> str:
        """Отменить все напоминания пользователя"""
        reminders = reminder_service.get_user_reminders(user_id)
        
        if not reminders:
            return "📭 У вас нет активных напоминаний"
        
        cancelled_count = 0
        for reminder in reminders:
            if reminder_service.cancel_reminder(user_id, reminder.id):
                cancelled_count += 1
        
        return f"✅ Отменено напоминаний: {cancelled_count} из {len(reminders)}"