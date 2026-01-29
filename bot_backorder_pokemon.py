import requests
from bs4 import BeautifulSoup
import os
import telegram

URL = "https://cddistribution.com/co/backorderjuguetes/?text-search=pok"
HEADERS = {"User-Agent": "Mozilla/5.0"}
STATE_FILE = "productos_previos.txt"


def obtener_productos():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    productos = set()

    for p in soup.select(".product-title a"):
        nombre = p.get_text(strip=True)
        if nombre:
            productos.add(nombre)

    return productos


def leer_estado_anterior():
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def guardar_estado(productos):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        for p in sorted(productos):
            f.write(p + "\n")


def main():
    productos_actuales = obtener_productos()
    productos_previos = leer_estado_anterior()

    nuevos = productos_actuales - productos_previos

    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

    if nuevos:
        mensaje = "🆕 NUEVOS PRODUCTOS BACKORDER (POKÉMON):\n\n"
        for p in sorted(nuevos):
            mensaje += f"• {p}\n"
    else:
        mensaje = "ℹ️ BACKORDER POKÉMON\nSin nuevos productos por ahora."

    bot.send_message(
        chat_id=os.environ["CHAT_ID"],
        text=mensaje
    )

    guardar_estado(productos_actuales)


if __name__ == "__main__":
    main()
