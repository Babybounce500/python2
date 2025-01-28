# 1. Verwende ein offizielles Python-Image als Basis
FROM python:3.9-slim

# 2. Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# 3. Kopiere die requirements.txt in das Arbeitsverzeichnis
COPY requirements.txt .

# 4. Installiere die Abhängigkeiten aus der requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopiere den gesamten Projektordner in das Arbeitsverzeichnis
COPY . .

# 6. Exponiere den Port, auf dem die Flask-App läuft
EXPOSE 5000

# 7. Definiere den Befehl zum Starten der Flask-App
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
