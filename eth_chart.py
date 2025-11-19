import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt


# --- Otsikko ---
st.title("Ethereum-hintakehitys (EUR)")

# --- MySQL-yhteys ---
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="****",       
        password="****",    
        database="exampledb" 
    )
    cursor = conn.cursor()

    # Hae data taulusta ethereum_hinta
    cursor.execute("SELECT timestamp, hinta FROM ethereum_hinta ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Muunna DataFrameksi
    df = pd.DataFrame(rows, columns=["Aika", "Hinta (EUR)"])

    # --- Korjaus: varmista että arvot ovat euroissa ---
    df["Hinta (EUR)"] = df["Hinta (EUR)"].astype(float)

    if df.empty:
        st.warning("Tietokannassa ei ole hintadataa.")
    else:
        # Näytä taulukko
        st.subheader("Hintadata MySQL tietokannasta")
        st.write(df)

        # Piirrä graafi Altairilla
        chart = alt.Chart(df).mark_line(point=True).encode(
            x="Aika:T",
            y="Hinta (EUR):Q"
        ).properties(width=700, height=400)

        st.subheader("Hintakehitys")
        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"Virhe tietokantayhteydessä: {e}")

