import requests
import pandas as pd

API_KEY = "demo"

URL = (
    "https://www.alphavantage.co/query"
    "?function=TIME_SERIES_DAILY"
    "&symbol=IBM"
    "&outputsize=full"
    f"&apikey={API_KEY}"
)

response = requests.get(URL, timeout=30)

response.raise_for_status()

dados = response.json()

serie = dados["Time Series (Daily)"]

linhas = []

for data, valores in serie.items():

    linhas.append({
        "data": data,
        "abertura": valores["1. open"],
        "maxima": valores["2. high"],
        "minima": valores["3. low"],
        "fechamento": valores["4. close"],
        "volume": valores["5. volume"]
    })

df = pd.DataFrame(linhas)

df.sort_values(
    "data",
    inplace=True
)

df.to_csv(
    "cotacoes_alpha_vantage.csv",
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8-sig"
)

print(
    f"Registros exportados: {len(df)}"
)