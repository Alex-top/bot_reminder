"""Обработчик текстовых сообщений"""

from services.reminder_service import reminder_service
from utils.formatters import format_reminder_created, format_reminder_list
from utils.validators import is_reminder_command


class MessageHandler:
    """Обработчик входящих сообщений"""
    
    def __init__(self, vk_api_instance):
        self.vk = vk_api_instance
    
    def handle(self, user_id: int, message_text: str) -> str:
        """
        Обработать сообщение и вернуть ответ
        """
        # Сначала проверяем, является ли сообщение попыткой создать напоминание
        reminder = reminder_service.create_reminder(user_id, message_text)
        
        if reminder:
            return format_reminder_created(reminder)
        
        # Если не удалось распознать — даём подсказку
        return self._get_help_message()
    
    def _get_help_message(self) -> str:
        return """
🤖 *Бот-напоминание*

Чтобы создать напоминание, напишите:

• `через 10 минут позвонить`
• `в 15:30 встреча`
• `завтра в 10:00 купить хлеб`
• `через 2 дня в 14:00 важное дело`

📋 Команды:
`/list` — список напоминаний
`/cancel [номер]` — отменить напоминание
`/cancel_all` — отменить всё
`/help` — эта справка
"""