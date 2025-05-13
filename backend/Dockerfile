FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DATABASE_URL=${DATABASE_URL}
ENV REDIS_URL=${REDIS_URL}
ENV DEBUG=${DEBUG}

CMD ["sh", "-c", "uvicorn chatapp.asgi:application --host 0.0.0.0 --port $PORT"]
