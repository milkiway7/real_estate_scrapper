# 1. Bazowy obraz
FROM python:3.12-slim

# 2. Zainstaluj zależności systemowe potrzebne dla przeglądarek i xvfb
RUN apt-get update && apt-get install -y wget gnupg curl ca-certificates && \
    apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 \
    libxfixes3 libxkbcommon0 libgtk-3-0 libasound2 libdrm2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 \
    libx11-xcb1 fonts-liberation xvfb && \
    rm -rf /var/lib/apt/lists/*

# 3. Twórz katalog roboczy
WORKDIR /app

# 4. Skopiuj pliki projektu
COPY .env .
COPY . .

# 5. Zainstaluj pakiety Pythona
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. Zainstaluj przeglądarki Playwright
RUN playwright install

# 7. Skopiuj i nadaj prawa do skryptu startowego
COPY start.sh /start.sh
RUN chmod +x /start.sh

# 8. Punkt wejścia
CMD ["/start.sh"]
