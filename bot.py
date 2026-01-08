import requests, os
from bs4 import BeautifulSoup

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.crucero.com.ar/cruceros-desde-buenos-aires-a-europa"
html = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

precios = []
for item in soup.select(".cruise-result"):
    precio = item.select_one(".price").text
    precio_num = int(precio.replace("$","").replace(".",""))
    precios.append(precio_num)

precio_min = min(precios)

mensaje = f"🚢 Precio más barato hoy: ${precio_min}"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": mensaje}
)
