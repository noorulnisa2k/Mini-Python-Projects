#!/usr/bin/env python3

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException, TimeoutException
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def setup_chrome_options():
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     return chrome_options

# try:
#     # Initialize Chrome options
#     options = setup_chrome_options()
    
#     # Initialize WebDriver with options
#     driver = webdriver.Firefox(options=options)
    
#     # Get Chrome version
#     chrome_version = driver.capabilities['browserVersion']
#     chrome_user_agent = driver.execute_script("return navigator.userAgent")
#     logger.info(f"Chrome Version: {chrome_version}")
#     logger.info(f"User Agent: {chrome_user_agent}")
    
#     # Open the URL with explicit wait
#     url = "http://twitter.com"
#     logger.info(f"Attempting to navigate to {url}")
#     driver.get(url)
    
#     # Wait for page load (max 10 seconds)
#     WebDriverWait(driver, 10).until(
#         lambda driver: driver.execute_script("return document.readyState") == "complete"
#     )
#     logger.info("Page loaded successfully")
    
# except WebDriverException as e:
#     logger.error(f"WebDriver error occurred: {str(e)}")
# except TimeoutException as e:
#     logger.error(f"Timeout waiting for page load: {str(e)}")
# except Exception as e:
#     logger.error(f"Unexpected error occurred: {str(e)}")
# finally:
#     # Ensure the driver quits
#     if 'driver' in locals():
#         driver.quit()
#         logger.info("WebDriver session ended")


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, time

# Path to your WebDriver executable
driver_path = "/home/noorulnisa/chromedriver"
service = Service(driver_path)
# Initialize the browser
driver = webdriver.Chrome(service=service)

try:
    # Open Google
    driver.get("https://www.google.com")
    
    # Find the search box
    search_box = driver.find_element(By.NAME, "q")
    
    # Type a search query
    search_box.send_keys("Selenium Python")
    
    # Press Enter
    search_box.send_keys(Keys.RETURN)
    
    # Wait for a few seconds to view the results
    driver.implicitly_wait(30)
    
    print("Search completed!")
    time.sleep(30)
finally:
    # Close the browser
    driver.quit()
