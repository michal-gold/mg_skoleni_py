
# jazyk python - verze 3.10 - slim verze
FROM python:3.10-slim

# kde pracuji
WORKDIR /app    

# kopiuj soubory
COPY main.py .

# instaluj balicky
RUN pip install - r requirements.txt --no-cache-dir

# zpristupni port ven - viz lekce od skolitele
# EXPOSE 8000

# spusti aplikaci
CMD ["python", "main.py"]
