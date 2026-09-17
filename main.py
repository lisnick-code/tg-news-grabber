import os
import requests
from telethon import TelegramClient, events

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Список юзернеймов каналов без @
TARGET_CHANNELS = [
    'advokatmillerua',
    'ukraine_91'
  'UaOnlii'
]

client = TelegramClient('news_session', API_ID, API_HASH)

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
