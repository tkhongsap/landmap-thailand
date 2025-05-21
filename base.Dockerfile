FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache python3 py3-pip chromium git curl \
    # Additional dependencies for Playwright on Alpine
    && apk add --no-cache \
    ffmpeg \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    nss \
    pciutils \
    dbus-x11

# Set environment variables for Playwright to use installed Chromium
ENV PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=0 \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
    PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Copy and install JavaScript dependencies
COPY package*.json ./
#RUN apk add openjdk11

RUN bun install

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# No need to install Playwright browsers since we're using system Chromium
# RUN PLAYWRIGHT_BROWSERS_PATH=/ms-playwright playwright install chromium

