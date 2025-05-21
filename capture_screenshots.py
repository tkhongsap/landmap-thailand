from playwright.sync_api import sync_playwright
import time
import os
import random
import argparse
import json
from datetime import datetime

def setup_directories():
    """Create directories for screenshots and results"""
    screenshot_dir = os.path.join(os.getcwd(), 'real_screenshots')
    results_dir = os.path.join(os.getcwd(), 'real_results')
    
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    return screenshot_dir, results_dir

def human_like_typing(page, selector, text):
    """Type text in a human-like manner with variable delays"""
    page.click(selector)
    page.fill(selector, "")  # Clear the field first
    for char in text:
        page.type(selector, char)
        # Random delay between keystrokes (50-150ms)
        time.sleep(random.uniform(0.05, 0.15))
    # Small pause after typing
    time.sleep(random.uniform(0.2, 0.5))

def capture_screenshot(page, deed_number, screenshot_dir):
    """Capture a full screenshot of the current page"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"deed_{deed_number}_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    # Take a full page screenshot
    page.screenshot(path=filepath, full_page=True)
    
    return filepath

def extract_land_deed_info(page, deed_number, screenshot_path):
    """Extract basic information to verify the screenshot contains real data"""
    info = {
        'deed_number': deed_number,
        'screenshot_path': screenshot_path,
        'timestamp': datetime.now().isoformat(),
        'has_data': False,
        'data_preview': {}
    }
    
    # Check if there's actual data on the page
    try:
        # Look for the information panel
        info_panel = page.locator('div:has-text("ข้อมูลแปลงที่ดิน")')
        if info_panel.count() > 0:
            info['has_data'] = True
            
            # Try to extract some basic information as preview
            try:
                # Extract deed number from the page to verify
                deed_elem = page.locator('text=เลขโฉนดที่ดิน').first()
                if deed_elem.count() > 0:
                    # Try to get the next element or sibling that might contain the value
                    value = page.evaluate('''(element) => {
                        const row = element.closest('.row');
                        if (row) {
                            const valueCol = row.querySelector('.col-sm-8, .col-md-8, .col-lg-8');
                            return valueCol ? valueCol.textContent.trim() : null;
                        }
                        return null;
                    }''', deed_elem)
                    
                    if value:
                        info['data_preview']['เลขโฉนดที่ดิน'] = value
                
                # Try to extract price information
                price_elem = page.locator('text=ราคาประเมินที่ดิน').first()
                if price_elem.count() > 0:
                    value = page.evaluate('''(element) => {
                        const row = element.closest('.row');
                        if (row) {
                            const valueCol = row.querySelector('.col-sm-8, .col-md-8, .col-lg-8');
                            return valueCol ? valueCol.textContent.trim() : null;
                        }
                        return null;
                    }''', price_elem)
                    
                    if value:
                        info['data_preview']['ราคาประเมินที่ดิน'] = value
            except Exception as e:
                print(f"Error extracting preview data: {str(e)}")
    except Exception as e:
        print(f"Error checking for data: {str(e)}")
    
    return info

def capture_deed_screenshots(deed_numbers, province="กรุงเทพมหานคร", district="04-บางรัก", headless=False):
    """Capture screenshots for the specified deed numbers"""
    screenshot_dir, results_dir = setup_directories()
    results = {}
    
    print(f"Starting screenshot capture for {len(deed_numbers)} deed numbers")
    print(f"Screenshots will be saved to: {screenshot_dir}")
    
    with sync_playwright() as p:
        # Launch browser with appropriate settings
        browser_type = p.chromium
        
        # Get the path to the Chromium executable - use system Chromium if available
        chromium_path = os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH')
        browser_options = {}
        
        if chromium_path:
            print(f"Using system Chromium at: {chromium_path}")
            browser_options['executable_path'] = chromium_path
        
        # Configure browser context with Thai language preference
        browser = browser_type.launch(headless=headless, **browser_options)
        context = browser.new_context(
            locale="th-TH",
            timezone_id="Asia/Bangkok",
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        )
        
        # Create a new page
        page = context.new_page()
        
        try:
            # Navigate to the website
            print("Navigating to landsmaps.dol.go.th...")
            page.goto("https://landsmaps.dol.go.th/", timeout=60000)
            
            # Wait for the page to load completely
            page.wait_for_load_state("networkidle")
            time.sleep(2)  # Additional wait for any dynamic content
            
            # Process each deed number
            for i, deed_number in enumerate(deed_numbers):
                print(f"Processing deed number {deed_number} ({i+1}/{len(deed_numbers)})")
                
                try:
                    # Select province
                    print(f"  Selecting province: {province}")
                    province_selector = 'select:has-text("กรุงเทพมหานคร")'
                    page.select_option(province_selector, province)
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Select district
                    print(f"  Selecting district: {district}")
                    district_selector = 'select:has-text("บางรัก")'
                    page.select_option(district_selector, district)
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Enter deed number
                    print(f"  Entering deed number: {deed_number}")
                    deed_input_selector = 'input[placeholder="เลขที่โฉนด"]'
                    human_like_typing(page, deed_input_selector, str(deed_number))
                    
                    # Click search button
                    search_button_selector = 'button:has-text("ค้นหา")'
                    print("  Clicking search button")
                    page.click(search_button_selector)
                    
                    # Wait for results to load
                    print("  Waiting for results...")
                    page.wait_for_load_state("networkidle")
                    time.sleep(random.uniform(2.0, 3.0))  # Additional wait for dynamic content
                    
                    # Capture screenshot
                    print("  Capturing screenshot...")
                    screenshot_path = capture_screenshot(page, deed_number, screenshot_dir)
                    print(f"  Screenshot saved to: {screenshot_path}")
                    
                    # Extract basic information to verify the screenshot
                    info = extract_land_deed_info(page, deed_number, screenshot_path)
                    
                    # Add to results
                    results[str(deed_number)] = info
                    
                    # Save individual result
                    individual_file = os.path.join(results_dir, f'deed_{deed_number}_info.json')
                    with open(individual_file, 'w', encoding='utf-8') as f:
                        json.dump(info, f, ensure_ascii=False, indent=2)
                    
                    # Add a random delay between requests
                    delay = random.uniform(2.0, 4.0)
                    print(f"  Waiting {delay:.1f} seconds before next request...")
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"  Error processing deed number {deed_number}: {str(e)}")
                    # Continue with next deed number
                    continue
        
        except Exception as e:
            print(f"Error accessing website: {str(e)}")
        
        finally:
            # Close browser
            browser.close()
    
    # Save all results to a single JSON file
    output_file = os.path.join(results_dir, 'all_deed_screenshots.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Completed processing {len(results)} deed numbers")
    print(f"Results saved to: {output_file}")
    print(f"Screenshots saved to: {screenshot_dir}")
    
    return results, screenshot_dir, output_file

def main():
    parser = argparse.ArgumentParser(description='Capture real screenshots from landsmaps.dol.go.th')
    parser.add_argument('--start', type=int, default=12340, help='Start deed number')
    parser.add_argument('--end', type=int, default=12345, help='End deed number')
    parser.add_argument('--province', type=str, default="กรุงเทพมหานคร", help='Province name')
    parser.add_argument('--district', type=str, default="04-บางรัก", help='District code-name')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Generate range of deed numbers
    deed_numbers = list(range(args.start, args.end + 1))
    
    # Capture screenshots
    capture_deed_screenshots(deed_numbers, args.province, args.district, args.headless)

if __name__ == "__main__":
    main()
