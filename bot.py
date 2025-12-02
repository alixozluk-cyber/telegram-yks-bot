from datetime import datetime, date, time as dtime, timedelta
import time
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT = os.getenv("CHAT_ID")

YKS_DATE = date(2026, 6, 14)   # YKS tarihini buraya yaz

SEND_HOUR = 10
SEND_MINUTE = 15

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def days_until(target_date: date) -> int:
    today = date.today()
    delta = target_date - today
    return delta.days

def build_message():
    d = days_until(YKS_DATE)
    if d > 1:
        return f"YKS'ye {d} gün kaldı 💪"
    elif d == 1:
        return "Yarın YKS! Hazırsın! ✨"
    elif d == 0:
        return "Bugün YKS! Başarılar 🍀"
    else:
        return f"YKS {abs(d)} gün önceydi."

def send_message(text):
    payload = {"chat_id": CHAT, "text": text}
    try:
        r = requests.post(API_URL, data=payload, timeout=20)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def seconds_until_next(hour, minute):
    now = datetime.now()
    target = datetime.combine(now.date(), dtime(hour, minute))
    if now >= target:
        target = datetime.combine(now.date() + timedelta(days=1), dtime(hour, minute))
    return int((target - now).total_seconds())

if __name__ == "__main__":
    print("Bot başladı...")
    while True:
        wait = seconds_until_next(SEND_HOUR, SEND_MINUTE)
        time.sleep(wait)
        msg = build_message()
        code, resp = send_message(msg)
        print("Gönderildi:", code, resp)
        time.sleep(60)
