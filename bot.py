import requests, os, re
from bs4 import BeautifulSoup

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.crucero.com.ar/cruceros-desde-buenos-aires-a-europa"
headers = {"User-Agent": "Mozilla/5.0"}

html = requests.get(URL, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

mejor_precio = None
mejor_link = URL

for a in soup.find_all("a", href=True):
    texto = a.get_text()
    precios = re.findall(r"\$\s?\d{1,3}(?:\.\d{3})+", texto)
    if precios:
        valor = int(precios[0].replace("$","").replace(".",""))
        if not mejor_precio or valor < mejor_precio:
            mejor_precio = valor
            mejor_link = a["href"]

if not mejor_precio:
    raise Exception("No se encontró ningún precio")

mensaje = f"🚢 Precio más barato hoy: ${mejor_precio}\n🔗 {mejor_link}"

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={"chat_id": CHAT_ID, "text": mensaje}
)
