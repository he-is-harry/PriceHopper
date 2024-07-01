import time
import traceback 
from bs4 import BeautifulSoup
# import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By

with open("../_latest_good_proxies.txt", "r") as f:
    proxiesList = f.read().splitlines()

counter = 1
for proxy in proxiesList:
    try:
        PROXIES = {
            'http': proxy,
            'https': proxy
        }

        # Compute the proxy definitions
        proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in PROXIES.items())

        # Define the Chrome webdriver options
        options = webdriver.ChromeOptions() 
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--proxy-server=%s' % proxy_arg)
        # options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

        # By default, Selenium waits for all resources to download before taking actions.
        # However, we don't need it as the page is populated with dynamically generated JavaScript code.
        options.page_load_strategy = "none"

        # Pass the defined options objects to initialize the web driver 
        driver = Chrome(options=options) 
        # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
        driver.implicitly_wait(15)

        url = "https://www.nofrills.ca/strawberries-1lb/p/20049778001_EA" 
        
        driver.get(url) 
        time.sleep(30)

        print(driver.find_element(By.TAG_NAME, "body").text)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")

        f = open("selSite" + str(counter) + ".html", "w")
        counter += 1
        f.write(str(soup.encode("utf-8")))
        f.close()
    except:
        print(traceback.format_exc())
        continue


