"""Создание клавиатур для бота"""

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class BotKeyboards:
    """Класс для создания клавиатур бота"""
    
    @staticmethod
    def get_main_keyboard() -> VkKeyboard:
        """
        Главная клавиатура с основными действиями.
        Показывается после команды /start или /help.
        """
        keyboard = VkKeyboard(one_time=False, inline=False)
        
        keyboard.add_button('📋 Список', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('❓ Помощь', color=VkKeyboardColor.SECONDARY)
        
        keyboard.add_line()
        keyboard.add_button('➕ Создать напоминание', color=VkKeyboardColor.POSITIVE)
        
        return keyboard
    
    @staticmethod
    def get_reminder_actions_keyboard(reminder_id: int) -> VkKeyboard:
        """
        Инлайн-клавиатура для действий с конкретным напоминанием.
        Показывается рядом с каждым напоминанием в списке.
        
        Args:
            reminder_id: ID напоминания для отмены
        """
        keyboard = VkKeyboard(one_time=False, inline=True)
        
        keyboard.add_callback_button(
            label=f'❌ Отменить #{reminder_id}',
            color=VkKeyboardColor.NEGATIVE,
            payload={'action': 'cancel_reminder', 'reminder_id': reminder_id}
        )
        
        return keyboard
    
    @staticmethod
    def get_inline_confirm_keyboard(reminder_id: int = None) -> VkKeyboard:
        """
        Инлайн-клавиатура для подтверждения действия (например, отмена всех).
        
        Args:
            reminder_id: ID напоминания (если отмена одного)
        """
        keyboard = VkKeyboard(one_time=False, inline=True)
        
        payload = {'action': 'confirm_cancel_all'}
        if reminder_id:
            payload = {'action': 'confirm_cancel_one', 'reminder_id': reminder_id}
        
        keyboard.add_callback_button(
            label='✅ Да, отменить',
            color=VkKeyboardColor.NEGATIVE,
            payload=payload
        )
        keyboard.add_callback_button(
            label='❌ Нет, оставить',
            color=VkKeyboardColor.SECONDARY,
            payload={'action': 'cancel_confirm'}
        )
        
        return keyboard
    
    @staticmethod
    def get_quick_reminder_keyboard() -> VkKeyboard:
        """
        Инлайн-клавиатура для быстрого создания напоминаний.
        Показывается при создании.
        """
        keyboard = VkKeyboard(one_time=True, inline=True)
        
        keyboard.add_callback_button(
            label='⏰ Через 5 минут',
            color=VkKeyboardColor.PRIMARY,
            payload={'action': 'quick_reminder', 'delay_minutes': 5}
        )
        keyboard.add_callback_button(
            label='⏰ Через 15 минут',
            color=VkKeyboardColor.PRIMARY,
            payload={'action': 'quick_reminder', 'delay_minutes': 15}
        )
        
        keyboard.add_line()
        keyboard.add_callback_button(
            label='⏰ Через 30 минут',
            color=VkKeyboardColor.PRIMARY,
            payload={'action': 'quick_reminder', 'delay_minutes': 30}
        )
        keyboard.add_callback_button(
            label='⏰ Через 1 час',
            color=VkKeyboardColor.PRIMARY,
            payload={'action': 'quick_reminder', 'delay_minutes': 60}
        )
        
        return keyboard