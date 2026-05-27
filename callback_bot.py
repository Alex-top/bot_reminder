from flask import Flask, request
import vk_api
import json
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

VK_TOKEN = os.getenv("VK_TOKEN")
GROUP_ID = os.getenv("VK_GROUP_ID")

# КОД ПОДТВЕРЖДЕНИЯ - получим позже
CONFIRMATION_CODE = ""

def send_message(user_id, text):
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    vk.messages.send(user_id=user_id, message=text, random_id=0)

@app.route('/', methods=['POST'])
def handle_callback():
    data = request.get_json()
    print(f"Получен запрос: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    if data.get('type') == 'confirmation':
        return CONFIRMATION_CODE
    
    if data.get('type') == 'message_new':
        user_id = data['object']['message']['from_id']
        user_text = data['object']['message']['text']
        send_message(user_id, f"✅ Бот работает! Вы написали: {user_text}")
        return 'ok'
    
    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)