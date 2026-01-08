from sources.crucero_com_ar import get_crucero_com
from sources.crucerum_com import get_crucerum
from sources.cruisesheet_com import get_cruisesheet
import requests, os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

all_results = []
all_results += get_crucero_com()
all_results += get_crucerum()
all_results += get_cruisesheet()

if not all_results:
    print("No se encontraron cruceros válidos")
    exit()

best = min(all_results, key=lambda x: x["price"])

msg = f"""🚢 MEJOR CRUCERO HOY

💰 USD {best['price']}
🛳 {best['title']}
🌐 Fuente: {best['source']}
🔗 {best['link']}
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
