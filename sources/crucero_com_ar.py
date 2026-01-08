import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE = "https://www.crucero.com.ar"

def get_crucero_com():
    url = "https://www.crucero.com.ar/c-28-croisieurope"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    for card in soup.select("div.resultado"):
        text = card.get_text(" ", strip=True).lower()

        if "buenos aires" not in text:
            continue
        if not any(x in text for x in ["barcelona", "genova", "roma", "civitavecchia"]):
            continue

        price_raw = card.select_one(".precio, .desde")
        if not price_raw:
            continue

        price = re.sub(r"[^\d]", "", price_raw.text)
        if not price:
            continue

        link = card.select_one("a")
        link = urljoin(BASE, link["href"]) if link else ""

        title = card.select_one("h3, h2")
        title = title.text.strip() if title else "Crucero"

        results.append({
            "title": title,
            "price": int(price),
            "link": link,
            "source": "crucero.com.ar"
        })

    return results
