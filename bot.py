"""Точка входа — запуск бота"""

import time
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from config import config
from handlers.message_handler import MessageHandler
from handlers.command_handler import CommandHandler
from handlers.callback_handler import CallbackHandler
from services.scheduler_service import SchedulerService
from utils.logger import BotLogger

# Создаём логгер для главного модуля
logger = BotLogger.get_logger(__name__)

# Стало (новая версия):
def send_message(vk, user_id: int, text: str) -> bool:
    try:
        vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=0
        )
        logger.debug(f"Сообщение отправлено пользователю {user_id}: {text[:50]}...")
        return True
    except Exception as e:
        print(f"Ошибка отправки сообщения {user_id}: {e}")
        logger.error(f"Ошибка отправки сообщения {user_id}: {e}")
        return False
    
def send_message_with_keyboard(vk, user_id: int, text: str, keyboard=None) -> bool:
    """Отправляет сообщение с клавиатурой"""
    try:
        params = {
            "user_id": user_id,
            "message": text,
            "random_id": get_random_id()
        }
        if keyboard:
            params["keyboard"] = keyboard.get_keyboard()
        
        vk.messages.send(**params)
        return True
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения с клавиатурой {user_id}: {e}")
        return False


def main():
    print("🚀 Запуск бота-напоминалки...")
    logger.info("🚀 Запуск бота-напоминалки...")
    
    # Инициализация VK
    vk_session = VkApi(token=config.VK_TOKEN)
    vk = vk_session.get_api()
    
    # Инициализация обработчиков
    message_handler = MessageHandler(vk)
    command_handler = CommandHandler(vk)
    callback_handler = CallbackHandler(vk)
    
    # Запуск планировщика
    scheduler = SchedulerService(vk, send_message)
    scheduler.start()
    
    # Основной цикл получения событий
    longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)

    logger.info("✅ Бот запущен и слушает сообщения...")
    
    print("✅ Бот запущен и слушает сообщения...")
    
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                message = event.object.message
                user_id = message["from_id"]
                text = message.get("text", "").strip()
                peer_id = message.get("peer_id", user_id)
                
                if not text:
                    continue

                logger.debug(f"Получено сообщение от {user_id}: {text}")
                
                # Обработка команд (/start, /help, /list, /cancel)
                if text.startswith("/"):
                    response_text, keyboard = command_handler.handle(user_id, text)
                    send_message_with_keyboard(vk, user_id, response_text, keyboard)
                else:
                    response = message_handler.handle(user_id, text)
                    if response:
                        send_message(vk, user_id, response)
            # Обработка нажатия на кнопку (callback)
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                user_id = event.object.user_id
                payload = event.object.payload

                logger.debug(f"Получен callback от {user_id}: {payload}")

                # Отвечаем на callback (чтобы кнопка перестала "грузиться")
                vk.messages.sendMessageEventAnswer(
                    event_id=event.object.event_id,
                    user_id=user_id,
                    peer_id=event.object.peer_id
                )

                # Обрабатываем действие
                response_text = callback_handler.handle(user_id, payload)

                # Отправляем ответное сообщение
                if response_text:
                    send_message(vk, user_id, response_text)
                
    
    except KeyboardInterrupt:
        print("\n🛑 Остановка бота...")
        logger.info("🛑 Остановка бота...")
        scheduler.stop()
    finally:
        print("👋 Бот остановлен")
        logger.info("👋 Бот остановлен")


if __name__ == "__main__":
    main()