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

        if "2027" not in text:
            continue

        if not any(x in text for x in ["buenos aires", "argentina", "south america", "BA"]):
            continue

        if not any(x in text for x in ["barcelona", "genova", "roma", "civitavecchia", "spain", "españa", "italy", "europe", "europa"]):
            continue

        price_raw = card.select_one(".precio, .desde")
        if not price_raw:
            continue

        raw = price_raw.text.lower()
        is_desde = "desde" in raw
        currency = "USD" if "u$s" in raw or "usd" in raw else "EUR" if "€" in raw else "ARS"

        price = re.sub(r"[^\d]", "", raw)
        if not price:
            continue

        link = card.select_one("a")
        link = urljoin(BASE, link["href"]) if link else ""

        title = card.select_one("h3, h2")
        title = title.text.strip() if title else "Crucero"

        results.append({
            "title": title,
            "price": int(price),
            "currency": currency,
            "desde": is_desde,
            "link": link,
            "source": "crucero.com.ar"
        })

    return results
