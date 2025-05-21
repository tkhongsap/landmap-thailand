FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache python3 py3-pip chromium git curl

# Copy and install JavaScript dependencies
COPY package*.json ./
#RUN apk add openjdk11

RUN bun install

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN PLAYWRIGHT_BROWSERS_PATH=/ms-playwright playwright install chromium

