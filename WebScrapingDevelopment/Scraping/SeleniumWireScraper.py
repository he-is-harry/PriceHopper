import time 
from bs4 import BeautifulSoup
# import pandas as pd 
from seleniumwire import webdriver 
from seleniumwire.webdriver import Chrome 
from selenium.webdriver.common.by import By

# Define the Chrome webdriver options
options = webdriver.ChromeOptions() 
options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver 
driver = Chrome(options=options) 
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

# Create a request interceptor
def interceptor(request):
    del request.headers['User-Agent']  # Delete the header first
    request.headers['User-Agent'] = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15"

# Set the interceptor on the driver
driver.request_interceptor = interceptor

url = "https://www.loblaws.ca/bananas-bunch/p/20175355001_KG" 
 
driver.get(url) 
time.sleep(20)

page_source = driver.page_source
soup = BeautifulSoup(page_source, features="lxml")

f = open("app3.html", "w")
f.write(str(soup))
f.close()

# bodyText = driver.find_element(By.TAG_NAME, "body").text

# driver.quit()

# # Print all the text
# f = open("text.txt", "w")
# f.write(bodyText)
# f.close()


