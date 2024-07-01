import time 
from bs4 import BeautifulSoup
# import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
# from selenium.webdriver.common.by import By

# Define the Chrome webdriver options
options = webdriver.ChromeOptions() 
# options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver 
driver = Chrome(options=options) 
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

url = "https://www.walmart.com/ip/JENNIE-O-Young-Turkey-Breast-with-Gravy-Packet-Frozen-Bone-in-4-9-lb-Plastic-Bag/182083486" 
 
driver.get(url) 
time.sleep(10)

html = driver.page_source
soup = BeautifulSoup(html)

f = open("app3.html", "w")
f.write(str(soup))
f.close()


