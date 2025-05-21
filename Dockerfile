# Build stage
FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install Python and required dependencies
RUN apk add --no-cache python3 py3-pip chromium \
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
RUN bun install

# Copy Python requirements and install
COPY requirements.txt ./
# Disable any inherited proxy settings to avoid build failures when
# external proxies are not reachable during `pip install`.
RUN export http_proxy="" https_proxy="" HTTP_PROXY="" HTTPS_PROXY="" \
    && pip3 install --no-cache-dir -r requirements.txt
# Don't need to run playwright install as we're using system chromium
# RUN playwright install chromium

# Copy all application files
COPY . .

# Build the JavaScript application
RUN bun run build

# Expose the web server port
EXPOSE 3000

# Start the web server by default
CMD ["bun", "run", "start"]

