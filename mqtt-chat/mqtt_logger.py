#!/usr/bin/env python3
import json, logging
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import pooling

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "chat/messages"

DB_CONFIG = {
    "host": "localhost",
    "user": "*******",
    "password": "*******",
    "database": "mqtt_chat"
}

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

db_pool = pooling.MySQLConnectionPool(pool_name="mqtt_pool", pool_size=5, **DB_CONFIG)

def save_message(nickname, message, client_id):
    try:
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (nickname, message, client_id) VALUES (%s, %s, %s)",
            (nickname, message, client_id))
        conn.commit()
        logger.info(f"Tallennettu: [{nickname}] {message[:50]}...")
    except mysql.connector.Error as err:
        logger.error(f"Tietokantavirhe: {err}")
    finally:
        cursor.close(); conn.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Yhdistetty MQTT-brokeriin")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Yhteysvirhe, koodi: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        nickname = data.get('nickname', 'Tuntematon')[:50]
        message = data.get('text', '')
        client_id = data.get('clientId', '')[:100]
        if message:
            save_message(nickname, message, client_id)
    except Exception as e:
        logger.error(f"Virhe: {e}")

def main():
    logger.info("MQTT Logger käynnistyy...")
    try:
        conn = db_pool.get_connection(); conn.close()
        logger.info("Tietokantayhteys OK")
    except mysql.connector.Error as err:
        logger.error(f"Ei yhteyttä tietokantaan: {err}")
        return

    client = mqtt.Client(client_id="mqtt_logger")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
