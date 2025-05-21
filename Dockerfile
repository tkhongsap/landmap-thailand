# Build stage
FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install Python and required dependencies
# Additional packages needed for Playwright on Alpine Linux
RUN apk add --no-cache python3 py3-pip chromium git curl \
    # Build dependencies for Python packages
    gcc python3-dev musl-dev libffi-dev openssl-dev \
    # Browser dependencies
    nss freetype harfbuzz ca-certificates ttf-freefont

# Copy and install JavaScript dependencies
COPY package*.json ./
RUN bun install

# Copy Python requirements
COPY requirements.txt ./

# Configure Playwright for Alpine Linux
# Specify where browsers should be installed
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
# Skip automatic browser download during pip install
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
# Use the system Chromium browser instead of downloading a separate one
ENV PLAYWRIGHT_CHROMIUM_PATH=/usr/bin/chromium-browser

# Install Python dependencies with special handling for Alpine
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir wheel && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir playwright==1.40.0

# Copy all application files
COPY . .

# Build the JavaScript application
RUN bun run build

# Expose the web server port
EXPOSE 3000

# Start the web server by default
CMD ["bun", "run", "start"]

