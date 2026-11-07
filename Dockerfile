FROM node:20-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer libreoffice-calc libreoffice-impress libreoffice-draw \
    ghostscript ocrmypdf tesseract-ocr-ara tesseract-ocr-eng \
    fonts-noto-core fonts-noto-extra fonts-hosny-amiri fonts-dejavu fontconfig \
 && rm -rf /var/lib/apt/lists/* && fc-cache -f
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY . .
USER node
EXPOSE 3000
CMD ["node","server.js"]
