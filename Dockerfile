# Build stage
FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

# Install Python and required dependencies
RUN apk add --no-cache python3 py3-pip chromium

# Copy and install JavaScript dependencies
COPY package*.json ./
RUN bun install

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Copy all application files
COPY . .

# Build the JavaScript application
RUN bun run build

# Expose the web server port
EXPOSE 3000

# Start the web server by default
CMD ["bun", "run", "start"]

