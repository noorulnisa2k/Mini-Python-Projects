import websockets
import asyncio
import base64
import json
import sys
import threading

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
from selenium.webdriver.remote.webdriver import WebDriver
import logging    
import inspect    
import re    
import os
import datetime
from datetime import timezone
import time
# from configure import auth_key

import pyaudio

logging.basicConfig(filename='extracted_keywords.log', level=logging.INFO)
 

auth_key = "2d33fb9affc5471bb57b6dc056b28582"
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
external_keyword_lists = {
    # "external_listIntro": {
    #     "keywords": ['hello','what can i help you with', 'hey', 'i\'m good', 'hack', 'who is that', 'all right', 'who is this', 'is on the call', 'when are you are speaking', 'you are speaking', 'who is on the', 'who is under found', 'who is on', 'who is understand', 'hay','who is calling','who is on the call','who is on the phone','who is there','who accounting','who is','is calling','anyone on the call','anyone there','anybody there', 'speak up','pick up','why not you are speaking','talk please','2 is calling','not bad'],
    #     "button_selector": "#Greetings",
    #     "wait_time": 3.3,  # Customize wait time for this list   - Intro
    #     "link_selector": "#DispoSelectB > font:nth-child(7) > a"   
    # },
    "external_list2": {
        "keywords": ['good', 'fine', 'i\'m fine', 'great', 'awesome', 'wonderful', 'what do you want', 'i\'m fine thank you', 'fantastic','what\'s this for','god bless you', 'fabilous', 'doing good', 'it\'s your time', 'doing fine', 'doing great', 'feeling well', 'i am doing fine', 'i am okay thank you', 'i\'m okay thank you', 'i am doing well how about you'],
        "button_selector": "#Pitch", #COMBINE GOOD WITH THIS PITCH 
        #"button_selector": "#playPauseButton", #COMBINE GOOD WITH THIS PITCH 
        "wait_time": 11,  # Customize wait time for this list   - Intro
        "link_selector": "#DispoSelectB > font:nth-child(7) > a",
        
    },
    "external_list3": {             #excluding intro, DNQ, DNC, and Busy if a keyword is detected from any other external keyword_lists and imadiate after that a keyword or phrase is dected and not available in any list switch to div iframe_soundboard and click hold on pitch then switch_to_default_content and perform xfer_list button and link clicking 
        "keywords": ['fine and you','good how are you','how are you','today i am outside','today i\'m outside'],
        "button_selector": "#Pitch", #COMBINE THANKS FOR ASKING WITH THIS PITCH 
        "wait_time": 11,  # Customize wait time for this list   - Intro
        "link_selector": "#DispoSelectB > font:nth-child(7) > a",
    },
    "external_list4": {
        "keywords": ['renting','renter','i am a tenent','tenent','i am renting an appartment','appartment building','this is a condo','i live in a condo','this is a condominium','this is a high rise','i live in a high rise','this is a law firm','this is a town house','this is an iv park'],
        "button_selector": r"#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list   - Renter
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list5": {
        "keywords": ['i am a homeowner but my son takes decisions for me', 'i own my house but my son takes decisions for me', 'son takes decisions', 'my son is my power of attorney', 'my daughter is my power of attorney', 'my son takes decisions for me', 'i am a homeowner but my daughter takes decisions for me', 'i\'m a homeowner but my daughter takes decisions for me', 'i own my house but my daughter takes decisions for me', 'my daughter takes decision for me', 'i am not a homeowner', 'i don\'t own my house', 'i do not own my house', 'i am not a decision maker', 'my son is homeowner but he did not lives with me', 'son is homeowner', 'he did not lives with me', 'she did not lives with me', 'son owns the house', 'did not lives with me', 'my daughter is homeowner but she did\'nt lives with me', 'daughter is homeowner', 'daughter owns the house', 'the bank owns the house', 'i am leasing the house', 'it\'s on the lease', 'leasing', 'lease', 'no this is a business', 'business', 'the house is on my sons name', 'the house is on my daughters name', 'mortgage', 'house is in the market'],
        "button_selector": r"#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list   - DNQ
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list6": {
        "keywords": ['snowy area','snow','metal roof','double story house','bar','coffee shop','barbers shop','construction company','trailer park','dentist office','trailer home','looking for a job','heavy dense wooded area','we do not need it','we do not need solar','we don\'t need solar','solar company','solar companies','not qualify','not qualifies','they say you did not qualify','did\'nt qualify','we talked to solar companies','shade ','tall buildings','i have tall buildings that shade my roof','tall trees','shade on my roof','tall buildings are shadding my roof','tall trees around my house','tall trees around my property','resturant','this is a resturant','clinic','doctor','i am at the doctor\'s office','rise','high rise','this is a high rise','shopping mall','i am in a shopping mall','driving','i am driving','this is an office','this is an office','hospital','this is a hospital ','shade on my roof','trees cover my roof','we dont have lot of sun','majority shade it\'s not really a good option','we just about to eat dinner so could you call back another time'],
        "button_selector": r"#Thankyou\ for\ your\ time",  
        "wait_time": 5.5,  # Customize wait time for this list   - DNQ
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list7": {
        "keywords": ['snowey','countryside','court building','mobile home','motor home','shipping yard','shipping ','company','departmental','store','shopping mall','center','heavy dense wooded area','dense','heavy woods','surrounded by woods','company','companies','business','school','college','ministry','military ','air force','navy','some other time','vacation','we are on vacation now get hold of us some other time','tall trees','shade on my roof','you actually have reached the business','you have reached the business','forest','we live in mountains','we live in a tent','breaking up','can\'t hear you','bad connection','flood'],
        "button_selector": r"#Thankyou\ for\ your\ time", 
        "wait_time": 5.5,  # Customize wait time for this list   - DNQ
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list8": {
        "keywords": ['not interested', 'we are not interested', 'she is not interested', 'he is not interested', 'at this time', 'i cannot afford it', 'i can\'t afford it','i can\'t afford it', 'not a good time', 'not this time', 'good i\'m all set with that thank you for calling', 'i\'m good for now thank you thanks for calling bye bye', 'well actually we\'re not interested yet',' but you\'re welcome to call back ','in about a month if you\'d like','house in the market'],
        "button_selector": r"#Thanks\ Anyway", 
        "wait_time": 2,  # Customize wait time for this list   - NI
        "link_selector": "#DispoSelectB > font:nth-child(10) > a",
    },
    "external_list9": {
        "keywords": ['call me back', 'call back after couple of hours', 'bad time right now','bad time','no thank you','no time for this call','not bad i guess no time for this call','i am busy at the moment call me back', 'call back in the evening', 'call back in the afternoon', 'call back tomorrow', 'call back in the late afternoon', 'call back homeowner is not at home', 'call back homeowner is out of town', 'you have to call in the evening he is out', 'we got strome','not very well', 'you have to call in the afternoon he is not available', 'you have to call back in couple of days he is out of town', 'you have to call in the evening she is out', 'you have to call in the afternoon she is not available', 'you have to call back in couple of days she is out of town','you have to call back','dinner','launch','having my launch','having my dinner'],
        "button_selector": r"#Thanks\ Anyway", 
        "wait_time": 2,  # Customize wait time for this list   - Callback
        "link_selector": "#DispoSelectA > font:nth-child(7) > a",
    },
    "external_list10": {
        "keywords": ['busy', 'i am at work', 'i am not doing good', 'i\'m okay thank you', 'i\'m working right now sorry'],
        "button_selector": r"#Thanks\ Anyway",
        "wait_time": 2,  # Customize wait time for this list   - Busy
        "link_selector": "#DispoSelectA > font:nth-child(4) > a",
    },
    "external_list11": {
        "keywords": ['you have called','not feeling good', 'i am sick', 'i\'m sick', 'i am not doing good', 'i\'m not doing good'],
        "button_selector": r"#Thanks\ Anyway",  # Combine Sorry to hear that pitch
        "wait_time": 3.0,  # Customize wait time for this list   - Intro
        "link_selector": "#DispoSelectB > font:nth-child(7) > a",
    },
    "external_list12": {
        "keywords": ['scratch my number from your list','call center do not call list','put me on your system\'s do not call list','military','put me on your internal do not call list','sheriff','police officer','sheriff\'s office','this is the sheriff','i am a police officer','head quarters','headquarters','headquarter','police','this is a police headquarters','this is a police station','do not call me again','do not call me ever again','remove my number from your system','black list','talk to your supervisor','manager','talk to your manager','supervisior','connect me with your supervisior','put me on your do not call list','do not call list','i am on federal and state do not call list','i am on a federal do not call list','where did you get my information', 'do not call me again', 'i am on a state do not call list'],
        "button_selector": r"#DNC\ Pitch",
        "wait_time": 4.5,  # Customize wait time for this list   - DNC
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list13": {
        "keywords": ['solar install','solar installer','sister works for solar company','brother works for solar company','uncle','daughter in law','son in law','this is a school','this is a migistrate\'s office','i am a migistrate','works for solar company','works in solar company','solar company','my daughter works for solar company','my son works for solar company','i owns a solar company','i am in airforce', 'i am in navy', 'i am in military'],
        "button_selector": r"#DNC\ Pitch",
        "wait_time": 4.5,  # Customize wait time for this list   - DNC
        "link_selector": "#DispoSelectB > font:nth-child(4) > a",
    },
    "external_list14": {
        "keywords": ['Hold on a second', 'wait a moment', 'let me get him', 'let me get her'],
        "button_selector": "#Ok",
        "wait_time": 2,  # Customize wait time for this list   - Busy
        "link_selector": "#DispoSelectA > font:nth-child(4) > a",
    },
    "external_listXfer": {
        "keywords": ['yes i am', 'this is homeowner', 'this is he', 'this is she'],
        "button_selector": r"#Hold\ on\ a\ moment",
        "wait_time": 2,  # Customize wait time for this list   - Busy
        "link_selector": "#DispoSelectC > font:nth-child(7) > a",  # For reference this list will use selectors of Xfer_list
    },
    # Add more external keyword lists here
}

p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
driver = ''
purpose_audio = ""
call_ended = False


def extracted_print(data):
    for i in range(10):
        print(data)

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

def handle_keyword_actions(iframe_keywords,keyword_list_name):
    print('inside handle key words')
    switch_to_vicidial_iframe()
    button_selector = external_keyword_lists[keyword_list_name]["button_selector"]
    link_selector = external_keyword_lists[keyword_list_name]["link_selector"]

    try:
        textarea = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="comments"]')))
        textarea.send_keys(iframe_keywords)

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

    except NoSuchElementException as e:
        print("Element not found:", str(e))
    except Exception as e:
        print(f"Error performing actions for keyword keyword in list '{keyword_list_name}': {str(e)}")
        # print(f"Error performing actions for keyword '{keyword}' in list '{keyword_list_name}': {str(e)}")


def handle_external_keyword_lists(driver, detected_words):
    global call_ended
    # try:
    #   pass
    # Check for keywords in the extracted text against external keyword lists
    detected_words = detected_words.replace(',',"").replace('.','')
    detected_keywords = check_for_external_keywords(detected_words)
    print(f"detection matches {detected_keywords}")
    if detected_keywords:
        for keyword_list_name, keyword in detected_keywords:
            # Perform actions for matched keywords from external lists
            switch_to_default_content(driver)
            iframe_soundboard = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "iframe_soundboard")))

            # Click the button assigned to the keyword list
            button_selector = external_keyword_lists[keyword_list_name]["button_selector"]

            # if button_selector in audio_played:
            #     button = iframe_soundboard.find_element(By.CSS_SELECTOR, "#Hold\ on\ a\ moment")
            #     button.click()
            # else:
            #     button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
            #     button.click()
            #     audio_played.append(button_selector)

            global purpose_audio

            # if button_selector=="#Greetings" and greetings_audio == False:
            #     button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
            #     button.click()
            #     greetings_audio = True
            if button_selector == "#Pitch":
                button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
                button.click()
                purpose_audio= True
            elif purpose_audio == True and button_selector not in ["#Greetings","#Pitch"]:
                button = iframe_soundboard.find_element(By.CSS_SELECTOR, button_selector)
                button.click()
                purpose_audio= True
            else:
                button = iframe_soundboard.find_element(By.CSS_SELECTOR, "#Hold\ on\ a\ moment")
                button.click()
                purpose_audio = False

            # Add a unique wait time for the keyword list
            wait_time = external_keyword_lists[keyword_list_name]["wait_time"]
            time.sleep(wait_time)

            # Switch back to the keyword extraction div
            switch_to_iframe_hello(driver)

            print(f"Matched keyword '{keyword}' in external list '{keyword_list_name}'")
            print(f">>>>>>>>>>>>>>>>>>>>>>>>>{detected_keywords[0]}")
            if keyword_list_name=="external_listXfer":
                handle_keyword_actions(keyword,keyword_list_name)
                call_ended = True
                return call_ended

        # return greetings_audio

    # except Exception as e:
    #   print(f"Error handling external keyword lists: {str(e)}")

        
async def send_receive():
    global call_ended
    elapsed_time = 0
    is_detected = False
    print(call_ended)
    print(f'Connecting websocket to url ${URL}')

    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:

        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            global call_ended
            while call_ended == False:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data":str(data)})
                    await _ws.send(json_data)

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

                await asyncio.sleep(0.01)
          
            return True

        async def receive():
            start_time = time.time()
            is_detected = False
            global call_ended
            while call_ended == False:
                try:
                    result_str = await _ws.recv()
                    if json.loads(result_str)['message_type'] == 'FinalTranscript':
                        is_detected = True
                        print(is_detected)
                        # print(json.loads(result_str)['text'])
                        words = json.loads(result_str)['text']
                        print(words)
                        # extracted_print(words)
                        call_ended = handle_external_keyword_lists(driver, words)
                        is_detected = False
                        print(is_detected)
                        # start_time = time.time()

                        # if call_ended:
                        #     print("Call ended. Stopping execution.")
                        #     return "stop"
                        
                    elapsed_time = time.time() - start_time  # Calculate elapsed time
                    print(elapsed_time)
                    if elapsed_time > 7 and is_detected == False:
                        call_ended = True
                        return "hangup"
                        

                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break

                except Exception as e:
                    assert False, "Not a websocket 4008 error"

        # Run both send and receive concurrently
        result = await asyncio.gather(send(), receive())

        # Check if receive() detected "call_ended"
        if "stop" in result:
            return "stop"
        elif "hangup" in result:
            print("%%%%%  call hangup  %%%%")
            switch_to_vicidial_iframe()
            try:
                button = driver.find_element(By.CSS_SELECTOR, "#MainTable > tbody > tr:nth-child(3) > td:nth-child(1) > font > center:nth-child(6) > a:nth-child(17) > img")
                button.click()
            except:
                print("clear button not found")
            # link = driver.find_element(By.CSS_SELECTOR, detected_list[1])
            # actions = ActionChains(driver)
            # actions.double_click(link).perform()
            return "stop"
        

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.debugger_address = "localhost:9222"

    driver = webdriver.Chrome(options=options)
    # driver = sys.argv[1]
    # while True:
    print("second scrit>>>>>>>>>>")
    result = asyncio.run(send_receive())
    if result == "stop":
        print("Exiting main function.")
        try:
            driver.switch_to.default_content()
            button = driver.find_element(By.XPATH, "//button[@id='copy_button']")
            button.click()
        except Exception as e:
            print(f"Couldn't find button: {e}")
        # break        