import requests
from bs4 import BeautifulSoup

import time
from urllib.parse import urljoin

url = "https://books.toscrape.com/catalogue/page-1.html"
livres = []

while url:
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")

    for article in soup.find_all("article", class_="product_pod"):
        titre = article.h3.a["title"]
        prix = article.find("p", class_="price_color").text.strip()
        disponibilite = article.find("p", class_="instock availability").text.strip()
        livres.append({
            "titre": titre,
            "prix": prix,
            "disponibilite": disponibilite,
        })

    # Lien vers la page suivante, absent sur la dernière page
    suivant = soup.find("li", class_="next")
    url = urljoin(url, suivant.a["href"]) if suivant else None

    time.sleep(1)  # pause entre les requêtes pour ne pas surcharger le site
# 4. enregistrement des résultats[cite: 154]

import csv
import os
from datetime import datetime

fichier = "prix_livres.csv"
date_collecte = datetime.now().isoformat(timespec="seconds")
colonnes = ["date_collecte", "titre", "prix", "disponibilite"]

# L'en-tête n'est écrit que si le fichier n'existe pas encore ou est vide
ecrire_entete = not os.path.exists(fichier) or os.path.getsize(fichier) == 0

with open(fichier, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=colonnes)
    if ecrire_entete:
        writer.writeheader()
    for livre in livres:
        writer.writerow({"date_collecte": date_collecte, **livre})

print(f"{len(livres)} lignes ajoutées à {fichier}")
