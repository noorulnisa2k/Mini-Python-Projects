from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from threading import Thread, Lock
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging    
import inspect    
import re    
import os
import datetime
from datetime import timezone
import time
import pyautogui

# Import keyword lists from separate files
from keyword_lists import list1, list2, AMlist01, AMlist1, AMlist02, Appartment, Busy, list1AMNW, AlreadyHaveSolar, xfer_list  # Import the xfer_list
# from keyword_lists import xfer_list  # Import the xfer_list

# Configure logging   
logging.basicConfig(filename='extracted_keywords.log', level=logging.INFO)
 
# Define a lock to synchronize button clicks
button_click_lock = Lock()

# Define a variable to track the last detected list name 
last_detected_list = ""

# External keyword lists (add more as needed)
external_keyword_lists = {
    "external_listIntro": {
        "keywords": ['hello', 'hi','what can i help you with', 'hey', 'i\'m good', 'hack', 'who is that'],
        "button_selector": "#Greetings",
        "wait_time": 2.0,  # Customize wait time for this list
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list2": {
        "keywords": ['good', 'fine', 'i\'m fine', 'great', 'awesome', 'wonderful', 'what do you want', 'i\'m fine thank you', 'fantastic','what\'s this for'],
        "button_selector": "#Pitch",
        "wait_time": 11.0  # Customize wait time for this list
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list3": {           
        "keywords": ['fine and you','good how are you','how are you','today i am outside','today i\'m outside'],
        "button_selector": "#Pitch", 
        "wait_time": 11.0,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list4": {
        "keywords": ['renting','renter','i am a tenent','tenent','i am renting an appartment'],
        "button_selector": "#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "Appartment.py"   # perform clicking on buttons mentioned in this list. 
    },
    "external_list5": {
        "keywords": ['i am a homeowner but my son takes decisions for me', 'i\'m a homeowner but my daughter takes decisions for me', 'i do not own my house'],
        "button_selector": "#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list6": {
        "keywords": ['snowy area','snow','metal roof','double story house','bar','coffee shop','barbers shop','construction company','trailer park'],
        "button_selector": "#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list  
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list7": {
        "keywords": ['snowey','countryside','court building','mobile home','motor home','can\'t hear you','bad connection'],
        "button_selector": "#Thankyou\ for\ your\ time", 
        "wait_time": 5.5,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list. 
    },
    "external_list8": {
        "keywords": ['not interested', 'we are not interested', 'she is not interested', 'he is not interested','i can\'t afford it', 'well actually we\'re not interested yet'],
        "button_selector": "#Thanks\ Anyway", 
        "wait_time": 2,  # Customize wait time for this list
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.  
    },
    "external_list9": {
        "keywords": ['call me back', 'call back after couple of hours', 'bad time right now','bad time','no thank you','not bad','no time for this call'],
        "button_selector": "#Thanks\ Anyway", 
        "wait_time": 2,  # Customize wait time for this list  
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "Busy.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list10": {
        "keywords": ['busy', 'i am at work', 'i am not doing good', 'i\'m okay thank you', 'i\'m working right now sorry'],
        "button_selector": "#Thanks\ Anyway",
        "wait_time": 2,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "Busy.py"   # perform clicking on buttons mentioned in this list. 
    },
    "external_list11": {
        "keywords": ['you have called','not feeling good', 'i\'m sick', 'i\'m not doing good'],
        "button_selector": "#Thanks\ Anyway",  
        "wait_time": 3.0,  # Customize wait time for this list   
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list12": {
        "keywords": ['scratch my number from your list','put me on your system\'s do not call list'],
        "button_selector": "#DNC\ Pitch",
        "wait_time": 4.5,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list13": {
        "keywords": ['solar install','solar installer','works for solar company'],
        "button_selector": "#DNC\ Pitch",
        "wait_time": 4.5,  # Customize wait time for this list 
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "list1.py"   # perform clicking on buttons mentioned in this list.
    },
    "external_list14": {
        "keywords": ['busy', 'i am at work', 'i am not doing good'],
        "button_selector": "#Thanks\ Anyway",
        "wait_time": 2,  # Customize wait time for this list  
        # "Additional_wait": 5,  # Wait for additional time
        # "Associated_list": "Busy.py"   # perform clicking on buttons mentioned in this list. 
    },
	"external_list15": {
        "keywords": ['wait let me get him on the line', 'wait let me get her on the line', 'wait she is comming', 'wait he is comming', 'she is comming', 'he is comming', 'wait', 'hold on'],
        "button_selector": "#Ok",
        # "wait_time": 2,  # Customize wait time for this list   - Busy
        # "keyword_lists": ["AlreadyHaveSolar"] 
    },
    # Add more external keyword lists here
}

# Step 2: Handle SSL warning
def handle_ssl_warning():
    try:
        advance_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Advance')]")
        advance_button.click()
        proceed_link = driver.find_element(By.XPATH, "//a[contains(text(), 'proceed to localhost (unsafe)')]")
        proceed_link.click()
    except:
        pass

# Function to extract keywords from the "iframe_hello" div     
def extract_keywords_from_div():
    try:
        # Find the div with id "iframe_hello"
        iframe_hello_div = wait.until(EC.presence_of_element_located((By.ID, "iframe_hello")))

        # Find and extract text content from the "info" div
        info_div = iframe_hello_div.find_element(By.ID, "info")
        info_text = info_div.text
        print("Info Text:", info_text)
        logging.info("Info Text: %s", info_text)

        # Find and extract text content from the "results" div, including final and interim spans
        results_div = iframe_hello_div.find_element(By.ID, "results")
        final_span = results_div.find_element(By.ID, "final_span").text
        interim_span = results_div.find_element(By.ID, "interim_span").text
        print("Final Span:", final_span)
        print("Interim Span:", interim_span)
        logging.info("Final Span: %s", final_span)
        logging.info("Interim Span: %s", interim_span)

        # Combine the text from "info" and "results" for keyword matching
        combined_text = f"{info_text} {final_span} {interim_span}"
        print("Extracted keywords from div:", combined_text)  # Debugging line
        logging.info("Extracted keywords from div: %s", combined_text)
        return combined_text
    except NoSuchElementException as e:
        logging.error("Element not found: %s", str(e))
        print("Element not found:", str(e))
    except Exception as e:
        logging.error("Error extracting keywords from div: %s", str(e))
        print("Error extracting keywords from div:", str(e))
        return ""

# Function to check if any keyword is present in the external keyword lists
def check_for_external_keywords(console_output):
    detected_keywords = []
    for keyword_list_name, keyword_list in external_keyword_lists.items():
        for keyword in keyword_list["keywords"]:
            # complete detection check
            if console_output.lower().strip() == keyword:
                detected_keywords.append((keyword_list_name, keyword))
            else:
                # single word detection that is present in list
                if keyword in console_output.lower().strip() and console_output.lower().strip() != "":
                    detected_keywords.append((keyword_list_name, keyword))
    return detected_keywords

# Function to switch to the default content
def switch_to_default_content(driver):
    try:
        driver.switch_to.default_content()
    except Exception as e:
        print(f"Error switching to default content: {str(e)}")

# Function to switch back to "iframe_hello"
def switch_to_iframe_hello(driver):
    try:
        driver.switch_to.default_content()  # Switch back to the main frame
        driver.find_element(By.ID, "iframe_hello")
        # driver.switch_to.frame(iframe_hello_div)
        print("Switched back to iframe_hello")
    except NoSuchElementException as e:
        print("Element not found:", str(e))
    except Exception as e:
        print("Error switching to iframe_hello:", str(e))

detected_keywords_during_wait = []
greetings_audio=False
purpose_audio=False

# Original version of handle_external_keyword_lists
def handle_external_keyword_lists(driver):
    try:
        # Extract dynamic keywords from the div with id "iframe_hello"
        iframe_keywords = extract_keywords_from_div()

        # keywords same to file
        if iframe_keywords.strip():
            extracted_keywords_to_file(iframe_keywords)

        # Check for keywords in the extracted text against external keyword lists
        detected_keywords = check_for_external_keywords(iframe_keywords)

        if detected_keywords:
            for keyword_list_name, keyword in detected_keywords:
                # Perform actions for matched keywords from external lists
                switch_to_default_content(driver)
                iframe_soundboard = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iframe_soundboard")))

                global purpose_audio, greetings_audio

                # Click the button assigned to the keyword list
                button_selector = external_keyword_lists[keyword_list_name]["button_selector"]

                if button_selector== "#Ok":
                    button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
                    button.click()
                    greetings_audio = False
                elif button_selector=="#Greetings" and greetings_audio == False:
                    button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
                    button.click()
                    greetings_audio = True
                elif button_selector == "#Pitch" and greetings_audio == True:
                    button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
                    button.click()
                    purpose_audio= True
                else:
                    button = iframe_soundboard.find_element(By.CSS_SELECTOR, "#Hold\ on\ a\ moment")
                    button.click()
                    greetings_audio = False

                # Add a unique wait time for the keyword list
                wait_time = external_keyword_lists[keyword_list_name]["wait_time"]
                time.sleep(wait_time)

                # Switch back to the keyword extraction div
                switch_to_iframe_hello(driver)

                print(f"Matched keyword '{keyword}' in external list '{keyword_list_name}'")

    except Exception as e:
        print(f"Error handling external keyword lists: {str(e)}")

# Function to switch to the iframe with id "vicidial_iframe"
def switch_to_vicidial_iframe():
    try:
        driver.switch_to.default_content()  # Switch back to the main frame
        iframe = driver.find_element(By.ID, "vicidial_iframe")
        driver.switch_to.frame(iframe)
        print("Switched to vicidial_iframe")
    except NoSuchElementException as e:
        print("Element not found:", str(e))
    except Exception as e:
        print("Error switching to vicidial_iframe:", str(e))

def handle_keyword_actions(keyword_list_name):
    global last_detected_list  # Access the global  last_detected_list variable 
    switch_to_vicidial_iframe()
    button_selector = keyword_lists[keyword_list_name]["button_selector"]
    link_selector = keyword_lists[keyword_list_name]["link_selector"]

    try:
        # Click the button
        button = driver.find_element(By.CSS_SELECTOR, button_selector)
        button.click()
        
        if keyword_list_name == "xfer_list":
            # Additional functions for 'xfer_list'
            # Wait for the button with the specified alt attribute to be clickable
            button_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//img[@alt='Transfer - Conference']")))
            button_element.click()
            print("'Transfer - Config' clicked.")

            # Get the parent window handle
            parentHandle = driver.current_window_handle

            # Get Window Handles (both parent and child)
            handles = driver.window_handles
            print("Window Handles: ", handles)

            # Switch to the new (child) window
            for handle in handles:
              if handle != parentHandle:
                driver.switch_to.window(handle)
                print(f"Switched to Child Window: {handle}")
                break

            # Additional functions for 'xfer_list' continued
            checkbox_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "consultative_checkbox")))
            checkbox_element = checkbox_span.find_element(By.ID, "consultativexfer")

            if not checkbox_element.is_selected():
              checkbox_element.click()
              print("'CONSULTATIVE' checkbox selected.")
            else:
              print("'CONSULTATIVE' checkbox is already selected.")

            dial_button_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DialWithCustomer")))
            dial_button = dial_button_span.find_element(
            # By.XPATH, "//*[@src='./images/vdc_XB_dialwithcustomer.gif']")
            By.CSS_SELECTOR, "#DialWithCustomer > a > img")
            dial_button.click()
            print("'DialWithCustomer' button clicked.")

            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "Leave3WayCall")))

            leave_button_span = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Leave3WayCall")))
            leave_button = leave_button_span.find_element(
            # By.XPATH, "//*[@src='./images/vdc_XB_leave3waycall.gif']")
            By.CSS_SELECTOR, "#Leave3WayCall > a > img")
            leave_button.click()
            print("'Leave3WayCall' button clicked.")

            # Switch back to the parent window
            # driver.switch_to.window(parentHandle)
            # time.sleep(1)

            # Double-click the link for 'xfer_list'
            xfer_list_link_selector = "#DispoSelectC > font:nth-child(1) > a"
            xfer_list_link = driver.find_element(By.CSS_SELECTOR, xfer_list_link_selector)
            actions = ActionChains(driver)
            actions.double_click(xfer_list_link).perform()

        else:
            # Default behavior for other lists
            # Double-click the link
            link = driver.find_element(By.CSS_SELECTOR, link_selector)
            actions = ActionChains(driver)
            actions.double_click(link).perform()

        # print(f"Matched keyword '{keyword}' in list '{keyword_list_name}'")
        print(f"Matched keyword keyword in list '{keyword_list_name}'")

    except NoSuchElementException as e:
        print("Element not found:", str(e))
    except Exception as e:
        print(f"Error performing actions for keyword keyword in list '{keyword_list_name}': {str(e)}")
        # print(f"Error performing actions for keyword '{keyword}' in list '{keyword_list_name}': {str(e)}")

# Combine the imported keyword lists into a single dictionary
keyword_lists = {
    "list1": list1.keyword_list,
    "list2": list2.keyword_list,
    "AMlist1": AMlist1.keyword_list,
    "AMlist01": AMlist01.keyword_list,
    "AMlist02": AMlist02.keyword_list,
    "Appartment": Appartment.keyword_list,
    "Busy": Busy.keyword_list,
    "list1AMNW": list1AMNW.keyword_list,
    "AlreadyHaveSolar": AlreadyHaveSolar.keyword_list,
    "xfer_list": xfer_list.keyword_list,  # Add the xfer_list
    # Add other keyword lists here
}

# Function to check if any keyword is present in the console output
def check_for_keywords(console_output):
    detected_keywords = []

    for keyword_list_name, keyword_list in keyword_lists.items():
            for keyword in keyword_list["keywords"]:
                # complete detection check
                if console_output.lower().strip() == keyword:
                    detected_keywords.append((keyword_list_name, keyword))
                else:
                    # single word detection that is present in list
                    if console_output.lower().strip() in keyword and console_output.lower().strip() != "":
                        detected_keywords.append((keyword_list_name, keyword))
    return detected_keywords

def extracted_keywords_to_file(keywords):
    extracted_keyword =f"{time.strftime('%Y-%m-%d %H:%M:%S')} : {keywords}"
    with open('data.txt', 'a') as file:
        file.write(extracted_keyword + '\n')
    
if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-gpu-blacklist")
    options.add_argument("--disable-web-security")  # To suppress CORS policy errors
    driver = webdriver.Chrome(options=options)

    # to maximize the browser window
    driver.maximize_window()

    # Open the website
    driver.get("https://localhost/AutoCallResponder/")
    handle_ssl_warning()
    wait = WebDriverWait(driver, 10)

    def set_window_size():
        for _ in range(5):
            pyautogui.hotkey('ctrl', '-')
            time.sleep(1)  # Wait for the window size to adjust

    # Set window size to 75% when the window loads
    set_window_size()
    # Function to check and click the "start_button" if needed
    def check_and_click_start_button():
        try:
            start_button = driver.find_element(By.ID, "start_button")
            start_img = start_button.find_element(By.ID, "start_img")
            src_attribute = start_img.get_attribute("src")

            if src_attribute == "mic.gif":
                start_button.click()
                print("Clicked 'start_button' to activate mic-animate.gif")
            elif src_attribute != "mic-animate.gif":
                # Click it to change src attribute to mic-animate.gif
                start_button.click()
                print("Clicked 'start_button' to change src attribute to mic-animate.gif")
        except NoSuchElementException as e:
            print("Element not found:", str(e))
        except Exception as e:
            print("Error checking and clicking 'start_button':", str(e))
    # Codes End Here

    try:
        # Start the continuous check for the microphone status
        start_checking_microphone_thread = Thread(target=check_and_click_start_button)
        start_checking_microphone_thread.daemon = True
        start_checking_microphone_thread.start()

        while True:

            ###############################################################################

            # Handle external keyword lists
            driver.switch_to.default_content()
            handle_external_keyword_lists(driver)
            check_and_click_start_button()

            ################################################################################

            if purpose_audio:
                print("Wait for additional 5 sec")
                time.sleep(5)       # additional wait time
                iframe_keywords = extract_keywords_from_div()
                
                # keywords same to file
                if iframe_keywords.strip():
                    extracted_keywords_to_file(iframe_keywords)

                detected_keywords = check_for_keywords(iframe_keywords)
                purpose_audio=False
                if detected_keywords:
                    keyword_list_name=detected_keywords[0]
                    handle_keyword_actions(keyword_list_name[0])
                    is_keyword_action_perfomed =True
                else:
                    handle_keyword_actions('list1AMNW')
                    is_keyword_action_perfomed =True

                if is_keyword_action_perfomed:
                    greetings_audio=False
                    purpose_audio=False

            ##########################################################################

            # After performing clicking, wait for the form to load in "vicidial_iframe"
            # try:
            #     wait.until(EC.presence_of_element_located((By.ID, "vicidial_iframe")))
            #     print("Form loaded in vicidial_iframe")
            # except NoSuchElementException as e:
            #     print("Element not found:", str(e))
            # except Exception as e:
            #     print("Error waiting for form to load in vicidial_iframe:", str(e))


            # Wait for a few seconds before checking again
            time.sleep(4)
        
    except KeyboardInterrupt:
        print("Script terminated by user")

    finally:
        driver.quit()
