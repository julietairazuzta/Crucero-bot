import requests, re
from bs4 import BeautifulSoup

def get_crucerum():
    url = "https://www.crucerum.com/buscar-cruceros"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for card in soup.select(".resultado-crucero"):
        text = card.get_text(" ", strip=True).lower()

        if "buenos aires" not in text:
            continue
        if not any(x in text for x in ["barcelona","genova","roma","civitavecchia"]):
            continue

        p = card.select_one(".precio")
        if not p:
            continue

        price = re.sub(r"[^\d]", "", p.text)
        if not price:
            continue

        a = card.select_one("a")
        link = a["href"] if a else ""

        results.append({
            "title": a.text.strip() if a else "Crucero",
            "price": int(price),
            "link": link,
            "source": "crucerum.com"
        })

    return results
