#!/bin/bash

# Build a test image to verify Playwright works in Alpine Linux
echo "Building test Docker image for Playwright on Alpine..."
docker build -t playwright-alpine-test .

# Run the test script inside the container
echo -e "\nRunning Playwright test inside container..."
docker run --rm playwright-alpine-test python3 test_playwright_install.py