from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Set up the user data directory
user_data_dir = os.path.expanduser("~/.selenium_chrome_user_data")

# Configure the WebDriver
options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")  # Use an absolute path
options.add_argument("--profile-directory=Default")

# Use WebDriver Manager to handle driver installation and setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

# Wait for QR code scan
input("Press Enter after scanning QR code and loading WhatsApp Web completely")

def read_messages():
    time.sleep(5)
    chat_boxes = driver.find_elements(By.CLASS_NAME, "_1pJ9J")
    for chat_box in chat_boxes:
        try:
            chat_box.click()
            time.sleep(2)
            messages = driver.find_elements(By.CLASS_NAME, "_1Gy50")
            for message in messages:
                print(message.text)
        except Exception as e:
            print(f"An error occurred: {e}")

read_messages()

# Close the browser
driver.quit()
