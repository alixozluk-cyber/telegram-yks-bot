# main.py
import os
import requests
from datetime import datetime, date
import schedule
import time
import random
import sys

# --- Ayarlar (env değişkenlerinden okunur) ---
TOKEN = os.getenv("BOT_TOKEN")
CHAT = os.getenv("CHAT_ID")   # örn: -1001234567890 veya @kanaladi
YKS_DATE_STR = os.getenv("YKS_DATE", "2025-06-15")  # YYYY-MM-DD format default
TEST_MODE = os.getenv("TEST_MODE", "0")  # "1" ise test gönder (derhal)
SEND_TIME = os.getenv("SEND_TIME", "10:15")  # "HH:MM", default 10:15

if not TOKEN or not CHAT:
    print("HATA: BOT_TOKEN veya CHAT_ID bulunamadı. Ortam değişkenlerini kontrol et.")
    sys.exit(1)

# parse YKS tarihi
try:
    YKS_YEAR, YKS_MONTH, YKS_DAY = map(int, YKS_DATE_STR.split("-"))
    YKS_DATE = date(YKS_YEAR, YKS_MONTH, YKS_DAY)
except Exception as e:
    print("HATA: YKS_DATE formatı YYYY-MM-DD olmalı. Aldığım değer:", YKS_DATE_STR)
    sys.exit(1)

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# --- 30 sert motivasyon sözü ---
motivasyonlar = [
    "Bugün çalışmazsan yarın utanırsın.",
    "Rakiplerin uyumuyor, senin bahanen ne?",
    "Hayat zor değil, sen erteleyerek zorlaştırıyorsun.",
    "Günü değil, geleceğini kurtar.",
    "Kendine acımayı bırak, sorumluluk al.",
    "Başarmak istiyorsan önce oturup çalışacaksın.",
    "Konuşmayı bırak, yapmaya başla.",
    "“Yarın” dediğin şey yıllardır gelmedi.",
    "Disiplin yoksa sonuç da yok.",
    "Kafanı topla; sınav seni beklemiyor, yaklaşıyor.",
    "Bugün zorlan, yarın gül.",
    "Yorgunum demek lüks; hedefi olanın bahanesi olmaz.",
    "Çalışmazsan yerinde sayarsın. Yerinde sayan kaybeder.",
    "İstiyorum yetmez, hak edeceksin.",
    "Kötü günler çalışmayanlar içindir.",
    "Düşünmeyi bırak, masaya otur.",
    "Başlamak zor, ama pişmanlık daha zor.",
    "Sana kimse başarı borçlu değil.",
    "Bugün ter akıtmazsan, sınavda gözyaşı dökersin.",
    "Kendini kandırmayı bırak; saat işlemeye devam ediyor.",
    "“Olmaz” diyenlerin hepsi çalışmayanlar.",
    "Kendine ihanet etme, çalış.",
    "Başarının bedeli terdir, laf değil.",
    "Ertelemek kaybetmenin ilk adımıdır.",
    "Odaklan, çünkü kimse senin yerine kazanmayacak.",
    "Korku geçer, sonuç kalır.",
    "Bir saatlik çalışma, bin saatlik pişmanlığı yok eder.",
    "Disiplin canını yakar ama sonuçlar iyileştirir.",
    "Bugün değilse ne zaman? Gerçekten.",
    "Hedefine ihanet etme. Çalış ve al."
]

def days_until(target_date: date) -> int:
    today = date.today()
    return (target_date - today).days

def build_message():
    d = days_until(YKS_DATE)
    if d > 1:
        base = f"<b>📅 YKS'ye son *{d} gün* kaldı!</b>"
    elif d == 1:
        base = "📅 Yarın YKS! Son düzeltmeler zamanı!"
    elif d == 0:
        base = "📅 Bugün YKS! Bol şans!"
    else:
        base = f"📅 YKS {abs(d)} gün önceydi ({YKS_DATE.isoformat()})."

    motiv = random.choice(motivasyonlar)
    # Telegram Markdown ya da HTML kullanmak istiyorsan parse_mode ekleyebilirsin.
    mesaj = f"{base}\n\n🔥 <i>{motiv}</i>"
    return mesaj

def send_message(text):
    payload = {
        "chat_id": CHAT,
        "text": text,
        # "parse_mode": "Markdown"  # istersen açabilirsin
    }
    try:
        r = requests.post(API_URL, data=payload, timeout=15)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

# Gönderim fonksiyonu (schedule tarafından çağrılır)
def job_send():
    mesaj = build_message()
    code, resp = send_message(mesaj)
    print(f"[{datetime.now().isoformat()}] Gönderildi: HTTP {code} | resp: {resp}")

def main_loop():
    # schedule ayarı
    schedule.clear()
    schedule.every().day.at(SEND_TIME).do(job_send)
    print(f"Bot çalışıyor. Her gün saat {SEND_TIME}'de gönderim yapılacak. YKS tarihi: {YKS_DATE.isoformat()}")
    # Eğer test modu açıksa hemen bir kere gönder
    if TEST_MODE == "1":
        print("TEST_MODE=1 olduğundan anında test mesajı gönderiliyor...")
        job_send()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main_loop()
