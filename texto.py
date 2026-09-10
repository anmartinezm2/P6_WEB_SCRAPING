import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 1. Hacer la petición a la página objetivo
url = "https://ninacosmetic.mx/bissu/"

response = requests.get(url)
response.encoding = 'utf-8'

# 2. Convertir el HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Buscar los productos
productos = soup.find_all("li", class_="product")

# 4. Crear lista para almacenar los datos
datos = []

# 5. Recorrer cada producto
for producto in productos:

    # Obtener nombre
    titulo = producto.find(class_="woocommerce-loop-product__title")

    if titulo:
        nombre = titulo.text.strip()
    else:
        nombre = None

    # Obtener precios
    precio = producto.find(class_="price")

    if precio:
        precio_texto = precio.get_text(" ", strip=True)
    else:
        precio_texto = ""

    # Extraer precio de menudeo
    menudeo = re.search(
        r"Menudeo\s*\$?\s*([\d,.]+)",
        precio_texto,
        re.IGNORECASE
    )

    # Extraer precio de mayoreo
    mayoreo = re.search(
        r"Mayoreo\s*\$?\s*([\d,.]+)",
        precio_texto,
        re.IGNORECASE
    )

    # Convertir a número
    precio_menudeo = (
        float(menudeo.group(1).replace(",", ""))
        if menudeo else None
    )

    precio_mayoreo = (
        float(mayoreo.group(1).replace(",", ""))
        if mayoreo else None
    )

    # Marca
    marca = "Bissú"

    # Guardar datos
    datos.append({
        "producto": nombre,
        "precio_menudeo": precio_menudeo,
        "precio_mayoreo": precio_mayoreo,
        "marca": marca
    })

# 6. Crear DataFrame
df = pd.DataFrame(datos)

# 7. Guardar CSV
df.to_csv(
    "catalogo_bissu.csv",
    index=False,
    encoding="utf-8-sig"
)

# 8. Mostrar resultados
print(df)

print("Scraping exitoso y archivo catalogo_bissu.csv creado.")
