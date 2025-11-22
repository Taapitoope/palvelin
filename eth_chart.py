import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt
import time

st.set_page_config(page_title="Data Dashboard", layout="wide")
st.title("📊 Data Dashboard: Sää & Ethereum")

placeholder = st.empty()

while True:
    with placeholder.container():
        # --- Säädata ---
        st.header("Säädata Raahesta 🌤️")
        st.caption("ℹ️ Tietokantaa päivitetään cron-ajastuksella 15 minuutin välein.")
        st.caption("🔄 Tämä näkymä päivittyy automaattisesti 15 minuutin välein.")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="****",        
                password="****", 
                database="weather_db"
            )
            df_weather = pd.read_sql(
                "SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50",
                conn
            )
            conn.close()

            if df_weather.empty:
                st.warning("Tietokannassa ei ole säähavaintoja.")
            else:
                st.subheader("Viimeisimmät havainnot")
                st.dataframe(df_weather)

                chart_weather = alt.Chart(df_weather).mark_line(point=True).encode(
                    x="timestamp:T",
                    y="temperature:Q",
                    tooltip=["city", "temperature", "description", "timestamp"]
                ).properties(width=700, height=400)

                st.subheader("Lämpötilakehitys")
                st.altair_chart(chart_weather, use_container_width=True)

        except Exception as e:
            st.error(f"Virhe sää-tietokantayhteydessä: {e}")

        # --- Ethereum ---
        st.header("Ethereum-hintakehitys (EUR)")
        st.caption("ℹ️ Tietokantaa päivitetään cron-ajastuksella 10 minuutin välein.")
        st.caption("🔄 Tämä näkymä päivittyy automaattisesti 10 minuutin välein.")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="***",        
                password="***", 
                database="exampledb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, hinta FROM ethereum_hinta ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            df_eth = pd.DataFrame(rows, columns=["Aika", "Hinta (EUR)"])
            df_eth["Hinta (EUR)"] = df_eth["Hinta (EUR)"].astype(float)

            if df_eth.empty:
                st.warning("Tietokannassa ei ole Ethereum-hintadataa.")
            else:
                st.subheader("Hintadata MySQL-tietokannasta (uusin ylimpänä)")
                st.dataframe(df_eth)

                # Kuvaajaa varten käännetään takaisin aikajärjestykseen
                df_eth_chart = df_eth.sort_values("Aika", ascending=True)

                chart_eth = alt.Chart(df_eth_chart).mark_line(point=True).encode(
                    x="Aika:T",
                    y="Hinta (EUR):Q"
                ).properties(width=700, height=400)

                st.subheader("Hintakehitys")
                st.altair_chart(chart_eth, use_container_width=True)

        except Exception as e:
            st.error(f"Virhe Ethereum-tietokantayhteydessä: {e}")

    # Päivitysväli: tässä 30 sekuntia
    time.sleep(30)