# Thailand Land Deed Screenshot Capture - Local Installation Guide

This guide will help you set up and run the screenshot capture script on your local machine to obtain real screenshots from the landsmaps.dol.go.th website.

## Prerequisites

1. Python 3.7 or higher
2. Internet access to the landsmaps.dol.go.th website
3. Basic familiarity with running commands in a terminal/command prompt

## Installation Steps

### 1. Install Python (if not already installed)

Download and install Python from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation.

### 2. Install Required Packages

Open a terminal/command prompt and run:

```bash
pip install playwright
playwright install chromium
```

This installs the Playwright automation library and the Chromium browser it needs to run.

### 3. Download the Script

Save the `capture_real_screenshots.py` script to a location on your computer.

## Usage Instructions

### Basic Usage

Open a terminal/command prompt, navigate to the folder containing the script, and run:

```bash
python capture_real_screenshots.py --start 12340 --end 12345
```

This will:
1. Open a browser window
2. Navigate to landsmaps.dol.go.th
3. Search for deed numbers 12340 through 12345
4. Capture screenshots of the results
5. Save them to a `real_screenshots` folder

### Command Line Options

The script supports several options:

```bash
python capture_real_screenshots.py --help
```

Key options:
- `--start`: First deed number to capture (default: 12340)
- `--end`: Last deed number to capture (default: 12345)
- `--province`: Province name (default: กรุงเทพมหานคร)
- `--district`: District code-name (default: 04-บางรัก)
- `--headless`: Run browser in headless mode (no visible window)

Example with different district:
```bash
python capture_real_screenshots.py --start 12340 --end 12345 --district "01-พระนคร"
```

## Output

The script creates two directories:

1. `real_screenshots/`: Contains PNG screenshots of each deed number result
   - Naming format: `deed_NUMBER_TIMESTAMP.png`

2. `real_results/`: Contains JSON files with metadata
   - `deed_NUMBER_info.json`: Individual metadata for each screenshot
   - `all_deed_screenshots.json`: Combined metadata for all screenshots

## Troubleshooting

### Script Crashes or Timeouts
- Ensure you have a stable internet connection
- Try running with fewer deed numbers at a time
- Increase the timeout by modifying the script (line with `timeout=60000`)

### Website Access Issues
- Verify you can access landsmaps.dol.go.th manually in a browser
- If the website requires login, you may need to modify the script

### Browser Automation Problems
- Try updating Playwright: `pip install --upgrade playwright`
- Reinstall browser: `playwright install chromium`

## Next Steps

After capturing the screenshots, you can:

1. Use the provided OCR extraction script to extract information from the screenshots
2. Manually review the screenshots to verify the data
3. Share the screenshots and extracted data as needed

For any issues or questions, please let me know!
