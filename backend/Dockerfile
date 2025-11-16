# backend/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# nc para esperar a Postgres en local, build-essential para psycopg
RUN apt-get update && apt-get install -y netcat-openbsd build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

# El contenedor escucha en 8000; en local lo mapeas (p. ej. 8003:8000)
EXPOSE 8000

CMD ["./entrypoint.sh"]
