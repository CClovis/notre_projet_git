import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

# 1. Envoi de la requête HTTP pour récupérer le code HTML de la page[cite: 126, 155]
response = requests.get(url)
response.raise_for_status()  # Vérifie que la requête a réussi (code 200)


# 2. Analyse du HTML avec BeautifulSoup[cite: 126, 155]
response.encoding = response.apparent_encoding
soup = BeautifulSoup(response.text, "html.parser")

# 3. Localisation et extraction des informations pour chaque livre[cite: 126, 152, 154]
livres = []
for article in soup.find_all("article", class_="product_pod"):
    titre = article.h3.a["title"]
    prix = article.find("p", class_="price_color").text.strip()
    disponibilite = article.find("p", class_="instock availability").text.strip()

    livres.append({
        "titre": titre,
        "prix": prix,
        "disponibilite": disponibilite,
    })

# 4. Affichage des résultats[cite: 154]
for livre in livres:
    print(livre)

print(f"\nNombre de livres récupérés : {len(livres)}")