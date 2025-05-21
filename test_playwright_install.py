#!/usr/bin/env python3
"""
Test script to verify Playwright installation
"""
try:
    from playwright.sync_api import sync_playwright
    print("✅ Successfully imported Playwright sync API")
    
    try:
        with sync_playwright() as p:
            print("✅ Successfully initialized Playwright")
            
            # Check if we can launch a browser
            try:
                browser = p.chromium.launch()
                print("✅ Successfully launched chromium browser")
                
                # Create a page
                try:
                    page = browser.new_page()
                    print("✅ Successfully created a new page")
                    
                    # Navigate to a simple website
                    try:
                        page.goto("https://example.com")
                        print("✅ Successfully navigated to example.com")
                        
                        # Get page title
                        title = page.title()
                        print(f"✅ Page title: {title}")
                        
                    except Exception as e:
                        print(f"❌ Error navigating to website: {str(e)}")
                    
                    browser.close()
                except Exception as e:
                    print(f"❌ Error creating page: {str(e)}")
                    browser.close()
            except Exception as e:
                print(f"❌ Error launching browser: {str(e)}")
    except Exception as e:
        print(f"❌ Error initializing Playwright: {str(e)}")
except ImportError as e:
    print(f"❌ Error importing Playwright: {str(e)}")

print("\nPlaywright installation test completed.")