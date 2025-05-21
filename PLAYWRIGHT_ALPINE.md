# Playwright on Alpine Linux

This document explains how the Playwright installation is configured to work properly on Alpine Linux, which was causing build failures.

## The Issue

Alpine Linux uses musl libc instead of glibc, which can cause compatibility issues with Playwright. The specific errors encountered were:

```
ERROR: Could not find a version that satisfies the requirement playwright==1.40.0 (from versions: none)
ERROR: No matching distribution found for playwright==1.40.0
```

## Solution

The solution involves several key changes to make Playwright work with Alpine Linux:

1. **Add necessary system dependencies**:
   ```dockerfile
   RUN apk add --no-cache python3 py3-pip chromium git curl \
       gcc python3-dev musl-dev libffi-dev openssl-dev \
       nss freetype harfbuzz ca-certificates ttf-freefont
   ```

2. **Configure Playwright environment variables**:
   ```dockerfile
   ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
   ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
   ENV PLAYWRIGHT_CHROMIUM_PATH=/usr/bin/chromium-browser
   ```

3. **Install Python dependencies with special handling**:
   ```dockerfile
   RUN pip3 install --upgrade pip && \
       pip3 install --no-cache-dir wheel && \
       pip3 install --no-cache-dir -r requirements.txt && \
       pip3 install --no-cache-dir playwright==1.40.0
   ```

4. **Use system Chromium instead of downloading a browser**:
   Instead of running `playwright install chromium`, we use the system's Chromium browser by setting `PLAYWRIGHT_CHROMIUM_PATH=/usr/bin/chromium-browser`.

## Testing

To test that Playwright is working correctly:

```bash
# Run the included test script
./test_dockerfile.sh
```

This will build the Docker image and run a simple test to verify Playwright functionality.

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are correctly installed
2. Check that the environment variables are correctly set
3. Verify that Chromium is installed and accessible
4. Try running the test script to debug issues