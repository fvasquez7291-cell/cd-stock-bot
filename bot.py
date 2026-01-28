import requests
import time
import os
from bs4 import BeautifulSoup
from unicodedata import normalize

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean_text(text):
    text = normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text.lower()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

def check_stock(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    text = clean_text(soup.get_text())

    if "agotado" in text:
        return False

    if "anadir al carrito" in text or "add to cart" in text:
        return True

    return False

PRODUCT_URL = "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-pokemon-tcg-mega-ev-ascended-heroes-tech-sticker-col-eng/"

available = check_stock(PRODUCT_URL)

if available:
    send_telegram("✅ PRODUCTO DISPONIBLE\n" + PRODUCT_URL)
