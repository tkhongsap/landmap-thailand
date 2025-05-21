# Build stage
FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install Python and required dependencies
RUN apk add --no-cache python3 py3-pip chromium git curl \
    # Additional dependencies for Playwright
    gcc python3-dev musl-dev libffi-dev openssl-dev \
    # For browser functionality
    nss freetype harfbuzz ca-certificates ttf-freefont

# Copy and install JavaScript dependencies
COPY package*.json ./
RUN bun install

# Copy Python requirements
COPY requirements.txt ./

# Set Playwright browser path
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

# Install Python dependencies with special handling for Alpine
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir wheel && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir playwright==1.40.0

# Use system Chromium instead of downloading a separate browser
ENV PLAYWRIGHT_CHROMIUM_PATH=/usr/bin/chromium-browser

# Copy all application files
COPY . .

# Build the JavaScript application
RUN bun run build

# Expose the web server port
EXPOSE 3000

# Start the web server by default
CMD ["bun", "run", "start"]

