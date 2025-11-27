
# Käytetään kevyttä Python imagea
FROM python:3.11-slim

# Työhakemisto kontissa
WORKDIR /app

# Kopioi riippuvuudet ja asenna ne
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopioi sovelluskoodi
COPY . .

# Käynnistä Flask API
CMD ["python3", "api.py"]

