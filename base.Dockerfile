FROM oven/bun:1.1.29-alpine AS build

WORKDIR /app

COPY package*.json ./
#RUN apk add openjdk11



RUN bun install

