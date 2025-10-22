# ✅ ClickUp → Telegram Notifier
# Flask app that connects ClickUp task updates to Telegram

from flask import Flask, request
import requests

app = Flask(__name__)

# ========== 1️⃣  CONFIGURATION ==========
# 🔹 Replace these with your real values
CLICKUP_TOKEN = "pk_43665435_QDVEG3ZVR5IANAHR8P503SDNOCGOEC3B"
TEAM_ID = "25757233"
BOT_TOKEN = "7558612818:AAH_RdDeGWdGltgWX1VoNnk2Q1Fz4NUW3Ww"
CHAT_ID = "-4603847315"  # your group or user ID

# Build URLs
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
WEBHOOK_ENDPOINT = "https://clickup-telegram-notifier.onrender.com/clickup-webhook"

# Headers for ClickUp API
headers = {
    "Authorization": CLICKUP_TOKEN,
    "Content-Type": "application/json"
}


# ========== 2️⃣  REGISTER CLICKUP WEBHOOK ==========
def register_clickup_webhook():
    payload = {
        "endpoint": WEBHOOK_ENDPOINT,
        "events": ["taskCreated", "taskUpdated"]
    }
    response = requests.post(
        f"https://api.clickup.com/api/v2/team/{TEAM_ID}/webhook",
        headers=headers,
        json=payload
    )

    print("📡 Webhook registration response:", response.text)


# ========== 3️⃣  FLASK ROUTES ==========

@app.route('/')
def home():
    return "✅ ClickUp → Telegram Notifier is running!"


@app.route('/clickup-webhook', methods=['POST'])
def clickup_webhook():
    data = request.json
    print("📦 Received data from ClickUp:", data)

    # Extract info from payload (depends on ClickUp’s structure)
    event_text = data.get('event', 'Unknown event')
    task_name = data.get('task', {}).get('name', 'No task Name')

    # Prepare message
    message = f"🔔 ClickUp Update: {event_text}\nTask: {task_name}"

    # Send to Telegram
    requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "text": message})
    print("📨 Sent to Telegram:", message)

    return "✅ Message sent to Telegram", 200


# ========== 4️⃣  START APP ==========
if __name__ == '__main__':
    print("✅ ClickUp → Telegram Notifier started!")
    register_clickup_webhook()
    app.run(host='0.0.0.0', port=10000)

# ==========  (5) START APP ==========

import requests
from datetime import datetime

def send_telegram(task):
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"

    task_name = task.get("name")
    timestamp_ms = task.get("date_created")
    date_created = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M')

    message = f"📌 New Task Created:\n*{task_name}*\n🕒 Created on: {date_created}"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    requests.post(url, data=payload)
