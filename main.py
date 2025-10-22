print("✅ ClickUp → Telegram Notifier started!")

from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
#TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
token = "7558612818:AAH_RdDeGWdGltgWX1VoNnk2Q1Fz4NUW3Ww"
url = f"https://api.telegram.org/bot{token}/sendMessage"
@app.route('/')
def home():
    return "✅ ClickUp → Telegram Notifier is running!"

@app.route('/clickup', methods=['POST'])
def clickup_webhook():
    data = request.json
    print("📦 Received data from ClickUp:", data)

    # Extract some basic info (this can be customized later)
    event_text = data.get('event', 'Unknown event')
    task_name = data.get('task', {}).get('name', 'No task name')
    message = f"🔔 ClickUp Update: {event_text}\nTask: {task_name}"

    # Send to Telegram
    requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "text": message})
    return "✅ Message sent to Telegram", 200

if __name__ == '__main__':
    print("✅ ClickUp → Telegram Notifier started!")
    app.run(host='0.0.0.0', port=5000)