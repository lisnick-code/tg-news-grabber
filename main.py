import os
import asyncio
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Переменные окружения
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("STRING_SESSION")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

TARGET_CHANNELS = [
    'advokatmillerua',
    'ukraine_91',
    'UaOnlii'
]

# Минимальный веб-сервер для удовлетворения проверок Render (Port Check)
class DummyHealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHealthCheck)
    server.serve_forever()

# Запускаем веб-сервер в отдельном потоке
threading.Thread(target=run_health_check_server, daemon=True).start()

# Инициализируем клиента Telegram
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHANNELS))
async def handler(event):
    message = event.message
    if not message.text and not message.media:
        return

    payload = {
        'id': message.id,
        'title': message.text[:100] if message.text else "Без заголовка",
        'text': message.text or '',
        'date': str(message.date)
    }

    try:
        res = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print(f"[+] Передано в Make: {res.status_code}")
    except Exception as e:
        print(f"[-] Ошибка отправки: {e}")

print("Граббер запущен...")
client.start()
client.run_until_disconnected()
