"""Точка входа — запуск бота"""

import time
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import config
from handlers.message_handler import MessageHandler
from handlers.command_handler import CommandHandler
from services.scheduler_service import SchedulerService


# Стало (новая версия):
def send_message(vk, user_id: int, text: str) -> bool:
    try:
        vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=0
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки сообщения {user_id}: {e}")
        return False


def main():
    print("🚀 Запуск бота-напоминалки...")
    
    # Инициализация VK
    vk_session = VkApi(token=config.VK_TOKEN)
    vk = vk_session.get_api()
    
    # Инициализация обработчиков
    message_handler = MessageHandler(vk)
    command_handler = CommandHandler(vk)
    
    # Запуск планировщика
    scheduler = SchedulerService(vk, send_message)
    scheduler.start()
    
    # Основной цикл получения событий
    longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)
    
    print("✅ Бот запущен и слушает сообщения...")
    
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message
                user_id = message["from_id"]
                text = message.get("text", "").strip()
                
                if not text:
                    continue
                
                # Обработка команд (/start, /help, /list, /cancel)
                if text.startswith("/"):
                    response = command_handler.handle(user_id, text)
                else:
                    response = message_handler.handle(user_id, text)
                
                # Отправка ответа
                if response:
                    print(f"🔍 ОТВЕТ БУДЕТ ОТПРАВЛЕН: {response[:50]}")  # <-- ДОБАВЬТЕ ЭТУ СТРОКУ
                    try:
                        result=vk.messages.send(
                            user_id=user_id,
                            message=response,
                            random_id=0
                        )
                        print(f"✅ ОТПРАВЛЕНО! Результат: {result}")
                    except Exception as e:
                        print(f"❌ ОШИБКА ОТПРАВКИ: {e}")
                
    
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
        scheduler.stop()
    finally:
        print("👋 Бот остановлен")


if __name__ == "__main__":
    main()