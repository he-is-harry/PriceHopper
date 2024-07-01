from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

proxies_to_test = []
with open("proxy_list_test.txt", "r") as f:
    lines = f.read().splitlines()
    for line in lines:
        proxies_to_test.append(line)

for proxy in proxies_to_test:
    proxies = {
        'http': proxy,
        'https': proxy
    }
    proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in proxies.items())

    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--proxy-server=%s' % proxy_arg)
                
    options.page_load_strategy = "none"

    driver = Chrome(options=options)
    driver.implicitly_wait(5)

    try:
        driver.get("https://www.proxynova.com/proxy-server-list/")
        time.sleep(15)

        bodyText = driver.find_element(By.TAG_NAME, "body").text
        driver.quit()

        print(bodyText)
    except:
        continue