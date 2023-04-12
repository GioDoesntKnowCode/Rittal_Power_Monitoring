from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Prompt the user to enter their login credentials
username = input("Enter your username: ")
password = input("Enter your password: ")

# Launch the browser and navigate to your website
browser = webdriver.Chrome()
browser.get("http://localhost:8080")

# Click the "Login to Dashboard" button
login_button = browser.find_element(By.XPATH, "//button[contains(text(), 'Login to Dashboard')]")
login_button.click()

# Wait for the login page to load and enter the credentials
username_field = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
username_field.send_keys(username)
password_field = browser.find_element_by_id("password")
password_field.send_keys(password)
submit_button = browser.find_element_by_xpath("//button[contains(text(), 'Log in')]")
submit_button.click()

# Wait for the page to load and select "Dashboard 1" from the drop-down list
select_board = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "selected_board"))
)
select_board.click()
dashboard1_option = browser.find_element_by_xpath("//option[contains(text(), 'Dashboard 1')]")
dashboard1_option.click()

# Wait for the page to load and extract data from the first table
table = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table[1]"))
)
soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
# Parse the table using BeautifulSoup and extract the required data

# Close the browser
browser.quit()
