import requests, re
from bs4 import BeautifulSoup

def get_crucerum():
    url = "https://www.crucerum.com/buscar-cruceros"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for card in soup.select(".resultado-crucero"):
        text = card.get_text(" ", strip=True).lower()

        if "2027" not in text:
            continue

        if not any(x in text for x in ["buenos aires", "argentina", "south america"]):
            continue

        if not any(x in text for x in ["barcelona", "genova", "roma", "civitavecchia", "spain", "italy", "europe"]):
            continue

        p = card.select_one(".precio")
        if not p:
            continue

        raw = p.text.lower()
        is_desde = "desde" in raw
        currency = "USD" if "u$s" in raw or "usd" in raw else "EUR" if "€" in raw else "ARS"
        price = re.sub(r"[^\d]", "", raw)
        if not price:
            continue

        a = card.select_one("a")
        link = a["href"] if a else ""

        results.append({
            "title": a.text.strip() if a else "Crucero",
            "price": int(price),
            "currency": currency,
            "desde": is_desde,
            "link": link,
            "source": "crucerum.com"
        })

    return results
