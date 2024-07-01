import subprocess
import time 
from bs4 import BeautifulSoup
# import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By

torexe = subprocess.Popen(["/Applications/Tor Browser.app/Contents/MacOS/Tor/tor"])
PROXIES = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050'
}

# Compute the proxy definitions
proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in PROXIES.items())

# Define the Chrome webdriver options
options = webdriver.ChromeOptions() 
options.add_argument('--proxy-server=%s' % proxy_arg)
# options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver 
driver = Chrome(options=options) 
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

driver.get("http://httpbin.org/ip")
bodyText = driver.find_element(By.TAG_NAME, "body").text
print(bodyText)


torexe.terminate()


