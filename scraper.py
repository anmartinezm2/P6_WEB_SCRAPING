import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://ninacosmetic.mx/bissu/"
response = requests.get(url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")
productos = soup.find_all("li", class_="product")

datos = []
for producto in productos:
    nombre = producto.find(class_="woocommerce-loop-product__title").text.strip()
    precio_texto = producto.find(class_="price").get_text(" ", strip=True)

    menudeo = re.search(r"Menudeo\s*\$?\s*([\d,.]+)", precio_texto)
    mayoreo = re.search(r"Mayoreo\s*\$?\s*([\d,.]+)", precio_texto)

    precio_menudeo = float(menudeo.group(1).replace(",", "")) if menudeo else None
    precio_mayoreo = float(mayoreo.group(1).replace(",", "")) if mayoreo else None

    marca = "Bissú"

    datos.append({
        "producto": nombre,
        "precio_menudeo": precio_menudeo,
        "precio_mayoreo": precio_mayoreo,
        "marca": marca
    })

df = pd.DataFrame(datos)
df.to_csv("catalogo_bissu.csv", index=False)
print("Scraping exitoso y archivo catalogo_bissu.csv creado.")
