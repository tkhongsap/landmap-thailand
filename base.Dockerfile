FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache python3 py3-pip chromium git curl \
    # Required for Playwright
    && apk add --no-cache \
    ffmpeg \
    font-noto \
    nodejs \
    npm \
    libstdc++ \
    ca-certificates \
    dbus-x11 \
    nss \
    freetype \
    harfbuzz \
    ttf-freefont

# Copy and install JavaScript dependencies
COPY package*.json ./
RUN bun install

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright separately using npm to ensure compatibility with Alpine
RUN npm init -y && \
    npm install playwright && \
    npx playwright install chromium

