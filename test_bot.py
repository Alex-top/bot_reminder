import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import config

def main():
    print("🚀 Тестовый бот запущен...")
    
    try:
        # Инициализация
        vk_session = vk_api.VkApi(token=config.VK_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)
        
        print("✅ Подключение установлено. Ждём события от Long Poll API...")
        print("👉 Отправьте любое сообщение вашему сообществу в ЛИЧНЫЕ СООБЩЕНИЯ")
        
        # Основной цикл
        for event in longpoll.listen():
            print(f"🔔 Получено событие: {event.type}")
            
            if event.type == VkBotEventType.MESSAGE_NEW:
                # Получаем данные
                msg = event.object.message
                user_id = msg['from_id']
                text = msg['text']
                peer_id = msg['peer_id']
                
                print(f"   📩 Текст: '{text}' от пользователя {user_id}")
                
                # Отправляем эхо-ответ
                vk.messages.send(
                    peer_id=peer_id,
                    message=f"✅ Тест: вы написали '{text}'",
                    random_id=0
                )
                print(f"   📨 Ответ отправлен")
            else:
                print(f"   ⚠️ Это не сообщение, игнорируем")
                
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()