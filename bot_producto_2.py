import requests
from bs4 import BeautifulSoup
import os
import telegram

URL = "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-de-pokemon-tcg-team-rocket-mewtwo-ex-league-battle-deck-eng/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text().lower()

    if "agotado" in text or soup.select_one(".out-of-stock"):
        status = "❌ PRODUCTO AGOTADO"
    elif "añadir al carrito" in text or "add to cart" in text or soup.select_one("form.cart"):
        status = "✅ STOCK DISPONIBLE"
    else:
        status = "⚠️ ESTADO NO CLARO (CD cambió la página)"

    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    bot.send_message(
        chat_id=os.environ["CHAT_ID"],
        text=f"{status}\n{URL}"
    )

if __name__ == "__main__":
    main()
