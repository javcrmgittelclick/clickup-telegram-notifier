# ✅ ClickUp → Telegram Notifier
# Flask app that connects ClickUp task updates to Telegram


from flask import Flask, request
import requests
from datetime import datetime
from threading import Thread

app = Flask(__name__)

# ========== 1️⃣  CONFIGURATION ==========

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
    try:
        response = requests.post(
            f"https://api.clickup.com/api/v2/team/{TEAM_ID}/webhook",
            headers=headers,
            json=payload
        )
        print("📡 Webhook registration response:", response.text)
    except Exception as e:
        print("⚠️ Webhook registration failed:", e)

# ========== 3️⃣  TELEGRAM SENDER ==========
def send_telegram(task):
    task_name = task.get("name", "No task Name")
    timestamp_ms = task.get("date_created")
    if timestamp_ms:
        date_created = datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M')
    else:
        date_created = "Unknown"

    message = f"📌 New Task Created:\n*{task_name}*\n🕒 Created on: {date_created}"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(TELEGRAM_URL, data=payload)
        print("📨 Sent to Telegram:", message)
    except Exception as e:
        print("⚠️ Failed to send Telegram message:", e)

# ========== 4️⃣  FLASK ROUTES ==========
@app.route('/')
def home():
    return "✅ ClickUp → Telegram Notifier is running!"


@app.route('/clickup-webhook', methods=['POST'])
def clickup_webhook():
    try:
        # force=True parses JSON even if headers are wrong
        data = request.get_json(force=True)
    except Exception as e:
        print("⚠️ Failed to parse JSON:", e)
        return "Bad Request", 400

    print("📦 Received data from ClickUp:", data)

    # Only send Telegram if 'task' exists
    task = data.get("task")
    if task:
        # Run asynchronously so webhook returns immediately
        Thread(target=send_telegram, args=(task,)).start()

    return "OK", 200

# ========== 5️⃣  START APP ==========
if __name__ == '__main__':
    print("✅ ClickUp → Telegram Notifier started!")
    register_clickup_webhook()
    app.run(host='0.0.0.0', port=10000)



