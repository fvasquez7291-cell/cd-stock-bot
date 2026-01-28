import requests
import os
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

HEADERS = {"User-Agent": "Mozilla/5.0"}

# 🔹 PRODUCTOS A MONITOREAR
PRODUCTS = [
    {
        "id": "ascended_heroes",
        "name": "Pokemon TCG Mega EV Ascended Heroes Tech Sticker",
        "url": "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-pokemon-tcg-mega-ev-ascended-heroes-tech-sticker-col-eng/"
    },
    {
        "id": "mewtwo_deck",
        "name": "Pokemon TCG Team Rocket Mewtwo EX League Battle Deck",
        "url": "https://cddistribution.com/co/tienda-online/venta-mayorista/juguetes-nuevos/pokemon-tcg/cartas-de-pokemon-tcg-team-rocket-mewtwo-ex-league-battle-deck-eng/"
    }
]

STATE_FILE = "last_state.txt"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})


def check_stock(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    # ❌ producto agotado explícito
    if soup.select_one(".out-of-stock"):
        return False

    # ❌ no existe formulario de compra
    cart_form = soup.select_one("form.cart")
    if not cart_form:
        return False

    # ❌ botón deshabilitado
    button = cart_form.select_one("button")
    if not button or button.has_attr("disabled"):
        return False

    # ✅ stock real
    return True


# 🔹 Cargar estado anterior
last_states = {}
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        for line in f:
            pid, state = line.strip().split("=")
            last_states[pid] = state


new_states = {}

for product in PRODUCTS:
    pid = product["id"]
    name = product["name"]
    url = product["url"]

    current_state = "available" if check_stock(url) else "out"
    previous_state = last_states.get(pid)

    # 🔔 Avisar solo si cambia el estado
    if previous_state != current_state:
        if current_state == "available":
            send_telegram(f"✅ STOCK DISPONIBLE\n{name}\n{url}")
        else:
            send_telegram(f"❌ PRODUCTO AGOTADO\n{name}\n{url}")

    new_states[pid] = current_state


# 💾 Guardar estados actuales
with open(STATE_FILE, "w") as f:
    for pid, state in new_states.items():
        f.write(f"{pid}={state}\n")
