from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from math import ceil

def parse_page(url):
    page = get(url)
    page_contents = page.content
    bs = BeautifulSoup(page_contents, "html.parser")
    all_items = bs.find_all("ul", {"class": "annunci-list"})
    all_rows = all_items[0].find_all("li", {"class": "listing-item listing-item--tiny js-row-detail"})
    for row in all_rows:
        dictionary = {}
        dictionary["Item"] = row.a.text.strip()
        prezzo = row.find("li", {"class": "lif__item lif__pricing"})
        data = row.find_all("div", {"class": "lif__data"})
        try:
            dictionary["Price"] = f"{prezzo.text.strip()}"
        except AttributeError:
            dictionary["Price"] = f"None"
        try:
            locali = f"{data[0].span.text.strip()}"
            dictionary["Locali"] = locali
        except (IndexError, AttributeError):
            dictionary["Locali"] = "None" 
        try:
            mq = f"{data[1].span.text.strip()} mq"
            dictionary["Superficie"] = mq
        except (IndexError, AttributeError):
            dictionary["Superficie"] = "None" 
        try:
            bagni = f"{data[2].span.text.strip()}"
            dictionary["Bagni"] = bagni
        except (IndexError, AttributeError):
            dictionary["Bagni"] = "None" 
        yield dictionary

pagina = "https://www.immobiliare.it/vendita-case/monza/?pag="
all_houses = []
first_page = get("https://www.immobiliare.it/vendita-case/monza/?pag=1")
page_contents = first_page.content
bs = BeautifulSoup(page_contents, "html.parser")
num_items = bs.find("span", {"class": "pull-left visible-xs raleway"})
num_items = int(num_items.strong.text.replace("risultati", "").replace(".", "").strip())
num_pages = ceil(num_items/25)
for pag in range(1, num_pages):
    print(f"parsing page {pag}")
    lista = list(parse_page(f"{pagina}{pag}"))
    for elemento in lista:
        all_houses.append(elemento)
df = pd.DataFrame(all_houses)
df.to_csv("houses.csv")
