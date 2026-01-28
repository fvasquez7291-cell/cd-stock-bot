import requests
import os
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {"User-Agent": "Mozilla/5.0"}
PRODUCT_URL = "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-pokemon-tcg-mega-ev-ascended-heroes-tech-sticker-col-eng/"

STATE_FILE = "last_state.txt"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def check_stock(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    if soup.select_one(".out-of-stock"):
        return False

    cart_form = soup.select_one("form.cart")
    if not cart_form:
        return False

    button = cart_form.select_one("button")
    if not button or button.has_attr("disabled"):
        return False

    return True

# 🔹 Cargar estado anterior
last_state = None
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        last_state = f.read().strip()

current_state = "available" if check_stock(PRODUCT_URL) else "out"

# 🔔 Enviar mensaje solo si cambia
if last_state != current_state:
    if current_state == "available":
        send_telegram("✅ PRODUCTO DISPONIBLE\n" + PRODUCT_URL)
    else:
        send_telegram("❌ PRODUCTO AGOTADO\n" + PRODUCT_URL)

# 💾 Guardar estado actual
with open(STATE_FILE, "w") as f:
    f.write(current_state)
