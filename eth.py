import requests
import mysql.connector
from datetime import datetime
import logging

# --- LOKITUS ---
logging.basicConfig(
    filename="/home/ubuntu/eth_script.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# --- CoinGecko API ---
url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=eur"

try:
    # --- MySQL-yhteys ---
    conn = mysql.connector.connect(
        host="localhost",
        user="****",       
        password="****",   
        database="exampledb"     
    )
    cursor = conn.cursor()

    # Luo taulu, jos ei ole
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ethereum_hinta (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        hinta DECIMAL(18,8)
    )
    """)

    # --- Hae hinta API:sta ---
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    hinta = data["ethereum"]["eur"]
    timestamp = datetime.now()

    # --- Tallenna tietokantaan ---
    cursor.execute("INSERT INTO ethereum_hinta (timestamp, hinta) VALUES (%s, %s)", (timestamp, hinta))
    conn.commit()

