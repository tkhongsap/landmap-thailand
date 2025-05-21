# Thailand Land Deed Screenshot Capture

A tool for capturing and processing screenshots from the Thai Land Department's online mapping service (landsmaps.dol.go.th).

## Overview

This project automates the process of:
1. Accessing the landsmaps.dol.go.th website
2. Searching for specific land deed numbers
3. Capturing screenshots of the results
4. Organizing the data for further processing

## Features

- Automated browser control with Playwright
- Configurable deed number ranges
- Province and district selection
- Headless mode for background execution
- Structured output of screenshots and metadata

## Requirements

- Python 3.7+
- Playwright
- Internet access to landsmaps.dol.go.th

## Quick Start

1. Install dependencies:
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. Run the script:
   ```bash
   python capture_screenshots.py --start 12340 --end 12345
   ```

## Detailed Documentation

For complete installation and usage instructions, see [landmaps_thailand.md](landmaps_thailand.md).

## Output

The script generates:
- Screenshots in `real_screenshots/` directory
- Metadata in `real_results/` directory

## Troubleshooting

If you encounter issues:
- Ensure stable internet connection
- Try smaller batch sizes
- Verify website accessibility
- Update Playwright if needed

## License

This project is for research and educational purposes only. 