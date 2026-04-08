# -------------------------------
# Python ETL Application
# -------------------------------
FROM python:3.12-slim

WORKDIR /app

# Instalace knihoven pro SQLModel a MariaDB
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Přeneseme složku s R1.csv do kontejneru (řeší problém Socat/Volumes)
COPY R1.csv /app/data/R1.csv

# Přeneseme zdrojové kódy
COPY src/ /app/

# Spuštění aplikace
CMD ["python", "main.py"]
