import requests, os, re
from bs4 import BeautifulSoup

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.crucero.com.ar/cruceros-desde-buenos-aires-a-europa"
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

texto = soup.get_text()
precios = re.findall(r"\$\s?\d{1,3}(?:\.\d{3})+", texto)

if not precios:
    raise Exception("No se encontraron precios en la página")

valores = [int(p.replace("$","").replace(".","")) for p in precios]
precio_min = min(valores)

mensaje = f"🚢 Precio más barato hoy: ${precio_min}"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": mensaje}
)
