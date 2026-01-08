import requests, re
from bs4 import BeautifulSoup

def get_cruisesheet():
    url = "https://cruisesheet.com/cruises/from/buenos-aires"
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for row in soup.select("tr"):
        text = row.get_text(" ", strip=True).lower()

        if not any(x in text for x in ["barcelona","genoa","rome"]):
            continue

        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        price = re.sub(r"[^\d]", "", cols[3].text)
        if not price:
            continue

        link = row.select_one("a")
        link = link["href"] if link else ""

        results.append({
            "title": cols[1].text.strip(),
            "price": int(price),
            "link": link,
            "source": "cruisesheet.com"
        })

    return results
