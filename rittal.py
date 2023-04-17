from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import argparse


def main(args):

    # Prompt the user to enter their login credentials
    username = input("Enter your username: ")
    password = input("Enter your password: ")


    # Launch the browser and navigate to your website
    browser = webdriver.Chrome("chromedriver")
    browser.get("http://localhost:8080")

    browser.find_element("id","loginUsername").send_keys(username)
    browser.find_element("id","loginPassword").send_keys(password)

    browser.find_element("id","dijit_form_Button_0").click()   # Login

    WebDriverWait(driver=browser, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    error_message = "Incorrect username or password."
    errors = browser.find_elements("css selector", ".flash-error")

    if any(error_message in e.text for e in errors):
        print("[!] Login failed")
    else:
        print("[+] Login successful")

    time.sleep(5) # Wait for page to load


    browser.find_elements(By.CLASS_NAME,"dojoxGridExpandoNode")[1].click()


    table = browser.find_element("id","pdu3TotalTable") # Store whole table 

    print(table.text)



    time.sleep(5)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get data from Watts Up power meter.')
    parser.add_argument('-s', '--sample-interval', dest='interval', default=2.0, type=float, help='Sample interval (default 2 s)')
    parser.add_argument('-t', '--timeout', dest='timeout', default=10.0, type=float, help='Timeout for experiment (default 10 s)')
    parser.add_argument('-l', '--log', dest='log', action='store_true', help='log data in real time')
    # parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

    args = parser.parse_args()
    main(args)