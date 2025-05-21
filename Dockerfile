# Build stage
FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN bun install

COPY . .

RUN bun run build

EXPOSE 3000

CMD ["bun", "run", "start"]

