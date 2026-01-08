import requests, re
from bs4 import BeautifulSoup

def get_cruisesheet():
    url = "https://cruisesheet.com/cruises/from/buenos-aires"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for row in soup.select("tr"):
        text = row.get_text(" ", strip=True).lower()

        if "2027" not in text:
            continue

        if not any(x in text for x in ["argentina", "south america", "buenos aires"]):
            continue

        if not any(x in text for x in ["barcelona", "genoa", "rome", "spain", "italy", "europe"]):
            continue

        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        raw = cols[3].text.lower()
        is_desde = "from" in raw or "desde" in raw
        currency = "USD" if "$" in raw else "EUR"
        price = re.sub(r"[^\d]", "", raw)
        if not price:
            continue

        link = row.select_one("a")
        link = link["href"] if link else ""

        results.append({
            "title": cols[1].text.strip(),
            "price": int(price),
            "currency": currency,
            "desde": is_desde,
            "link": link,
            "source": "cruisesheet.com"
        })

    return results
