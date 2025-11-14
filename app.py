import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="MySQL Demo", page_icon="🐬")
st.title("Henkilöt ja heidän autonsa")

try:
    # Yhdistä MySQL-tietokantaan
    conn = mysql.connector.connect(
        host="localhost",
        user="veikko",         # vaihda tarvittaessa
        password="*******",  # vaihda tarvittaessa
        database="exampledb"   # vaihda tarvittaessa
    )
    cursor = conn.cursor()

    # Hae tiedot taulusta
    cursor.execute("SELECT nimi, auto FROM HenkilotAutot")
    rows = cursor.fetchall()

    # Muunna DataFrameksi
    df = pd.DataFrame(rows, columns=["Nimi", "Auto"])

    # Näytä taulukko Streamlitissä
    st.subheader("Tietokannan sisältö")
    st.table(df)

    # Sulje yhteys
    cursor.close()
    conn.close()

except Exception as e:
    st.error(f"MySQL-yhteys epäonnistui: {e}")
