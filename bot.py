import requests
import os
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

PRODUCT_URL = "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-pokemon-tcg-mega-ev-ascended-heroes-tech-sticker-col-eng/"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def check_stock(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    # ❌ Regla 1: producto agotado explícito
    if soup.select_one(".out-of-stock"):
        return False

    # ❌ Regla 2: no existe formulario de compra
    cart_form = soup.select_one("form.cart")
    if not cart_form:
        return False

    # ❌ Regla 3: botón deshabilitado
    button = cart_form.select_one("button")
    if not button or button.has_attr("disabled"):
        return False

    # ✅ Stock real
    return True

if check_stock(PRODUCT_URL):
    send_telegram("✅ STOCK REAL DISPONIBLE\n" + PRODUCT_URL)
