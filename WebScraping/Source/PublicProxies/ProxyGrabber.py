import sys
# import traceback
from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import time
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By
import math
import threading
import queue
import keyboard
from random import shuffle, randint

# Configuration
good_proxies_file_config = "../../Files/_good_proxies.txt"
bad_proxies_file_config = "../../Files/_bad_proxies.txt"
validate_implicit_wait_config = 5
validate_delay_config = 5
validate_threads_config = 7
proxy_validate_limit_config = 200

proxy_nova_implicit_wait_config = 5
proxy_nova_delay_config = 15

def get_proxies_proxy_nova(proxyList, valid_starters):
    # Data cleaning function
    # Remove JavaScript used to obfuscate the Proxy IP
    def removeJSPrefix(x):
        xstr = str(x)
        index = xstr.rfind(")")
        return xstr[index + 1 : ]

    # Extract rows which are favourable to us
    def getFirstNum(string):
        index = 0
        while string[index] >= '0' and string[index] <= '9':
            index += 1
        if index == 0:
            return 0
        return int(string[0 : index])

    def validRow(row):
        if row["Proxy Port"] == -1:
            return False
        # Check uptime (require >= 60%)
        # print(str(getFirstNum(str(row["Uptime"]))) + " " + str(row["Proxy Country"]).lower() + " " + str("elite" not in str(row["Anonymity"]).lower() and "anonymous" not in str(row["Anonymity"]).lower()))
        if getFirstNum(str(row["Uptime"])) < 10:
            return False
        if 'china' in str(row["Proxy Country"]).lower():
            return False
        if "elite" not in str(row["Anonymity"]).lower() and "anonymous" not in str(row["Anonymity"]).lower():
            return False
        return True
    # Shuffle the valid starters to help reduce the chance of querying between program runs
    shuffle(valid_starters)
    for proxy in valid_starters:
        proxies = {
            'http': proxy,
            'https': proxy
        }
        proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in proxies.items())
        # proxy_arg = oneProxy[0 : oneProxy.find(":")]
        # print(proxy_arg)

        # proxy_ip = oneProxy[0 : oneProxy.find(":")]

        # webdriver.DesiredCapabilities.CHROME['proxy'] = {
        #     "httpProxy": oneProxy,
        #     "sslProxy": oneProxy,
        #     "proxyType": "manual",
        # }

        # webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server=%s' % proxy_arg)
        options.add_argument("--headless=new")
        options.page_load_strategy = "none"

        driver = Chrome(options=options) 
        driver.implicitly_wait(proxy_nova_implicit_wait_config)
        
        try:
            driver.get("https://www.proxynova.com/proxy-server-list/")
            time.sleep(proxy_nova_delay_config)

            html = driver.page_source
            soup = BeautifulSoup(html)

            proxy_table = soup.select('table#tbl_proxy_list')[0] 

            table_df = pd.read_html(StringIO(str(proxy_table)))[0]

            table_df["Proxy IP"] = table_df["Proxy IP"].apply(removeJSPrefix)
            table_df["Proxy Port"] = table_df["Proxy Port"].apply(lambda x: -1 if math.isnan(x) else int(x))
            
            for index, row in table_df.iterrows():
                if validRow(row):
                    proxyList.append(str(row["Proxy IP"]) + ":" + str(row["Proxy Port"]))
            print(table_df)
            break
        except:
            continue

def get_proxies_proxy_scrape(proxyList):
    protocol = "http"
    country = "all"
    timeout = "10000"
    ssl = "all"
    anonymity = "elite,anonymous"
    apiUrl = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol={pr}&timeout={ti}&country={co}&ssl={sl}&anonymity={an}".format(
        pr = protocol, ti=timeout, co = country, sl=ssl, an = anonymity)
    r = requests.get(apiUrl)

    textResult = r.text
    addressArray = textResult.splitlines()

    # As long as the line starts with a number, we assume that it is an ip address
    for line in addressArray:
        if len(line) > 0 and line[0] >= '0' and line[0] <= '9':
            proxyList.append(line)

    # Then we add all socks5 protocols
    protocol = "socks5"
    country = "all"
    timeout = "10000"
    ssl = "yes"
    anonymity = "elite,anonymous"
    apiUrl = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol={pr}&timeout={ti}&country={co}&ssl={sl}&anonymity={an}".format(
        pr = protocol, ti=timeout, co = country, sl=ssl, an = anonymity)
    r = requests.get(apiUrl)

    textResult = r.text
    addressArray = textResult.splitlines()

    # As long as the line starts with a number, we assume that it is an ip address
    for line in addressArray:
        if len(line) > 0 and line[0] >= '0' and line[0] <= '9':
            proxyList.append("socks5://" + line)

def get_proxies_github_proxifly(proxyList):
    r = requests.get("https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt")
    textResult = r.text
    addressArray = textResult.splitlines()

    # Check if line ends with a number
    for line in addressArray:
        if len(line) > 0 and line[len(line) - 1] >= '0' and line[len(line) - 1] <='9':
            # Remove prefix
            proxyList.append(line[line.find("//") + 2 : ])

def get_ip_proxy(proxy):
    val = proxy.rfind(":")
    if val >= 0:
        return proxy[0 : val]
    else:
        return proxy
    
def validate_exit_finally():
    global bad_proxies
    # Save bad proxies
    with open(bad_proxies_file_config, "w") as f:
        for key in bad_proxies:
            f.write(key + " " + str(bad_proxies[key]) + "\n")

# Validate the proxies using threading
q = queue.Queue()
valid_proxies = []
valid_array_lock = threading.Lock()
proxies_left = False
# Stores ip's
bad_proxies = {}
good_proxies_ips = {}
# Stores actual proxy ports
good_proxies = {}
# Indicates if the shortcut pre-saved approach to 
# validating proxies should be used
fast_shortcut = False

def check_proxies():
    global q
    global valid_proxies
    global proxies_left
    global bad_proxies
    global good_proxies
    global good_proxies_ips
    global fast_shortcut

    while not q.empty():
        proxy = q.get()
        print("Proxy (" + str(q.qsize()) + "): " + proxy)
        # Non thread safe access, OK since IP's are unique
        proxy_ip = get_ip_proxy(proxy)
        if not fast_shortcut and get_ip_proxy(proxy_ip) in bad_proxies and get_ip_proxy(proxy_ip) not in good_proxies_ips:
            x = randint(1, 3)
            if x < bad_proxies[proxy_ip]: # Set a chance to check the proxy up to a limit of 3
                print("Skipped: " + proxy)
                continue
        elif fast_shortcut and get_ip_proxy(proxy_ip) not in good_proxies_ips:
            print("Skipped: " + proxy)
            continue
        # print(proxy)
        try:
            PROXIES = {
                'http': proxy,
                'https': proxy
            }
            proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in PROXIES.items())

            options = webdriver.ChromeOptions()
            # options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('--proxy-server=%s' % proxy_arg)
            # options.add_argument("--log-level=OFF")
            options.add_argument("--headless=new")
            
            options.page_load_strategy = "none"

            driver = Chrome(options=options)
            driver.implicitly_wait(validate_implicit_wait_config)

            # driver.get("http://httpbin.org/ip")
            # bodyText = driver.find_element(By.TAG_NAME, "body").text
            # print(bodyText)
            # time.sleep(VALIDATE_DELAY)
            
            # driver.get("https://check.torproject.org/")
            driver.get("https://www.enable-javascript.com/")
            time.sleep(validate_delay_config)

            # headerText = driver.find_element(By.TAG_NAME, "h1").text
            resultText = driver.find_element(By.CLASS_NAME, "enabled")
            driver.quit()

            # if "Tor" in headerText:
            # if "Javascript is enabled in your web browser" in resultText:
            # else:
            #     proxy_ip = get_ip_proxy(proxy)
            #     bad_proxies[proxy_ip] = bad_proxies.get(proxy_ip, 0) + 1
            print(resultText)
            with valid_array_lock:
                valid_proxies.append(proxy)
                print("Appended: " + proxy)
                if proxy not in good_proxies:
                    with open(good_proxies_file_config, "a") as f:
                        f.write(proxy + "\n")
        except:
            # print(traceback.format_exc())
            proxy_ip = get_ip_proxy(proxy)
            bad_proxies[proxy_ip] = bad_proxies.get(proxy_ip, 0) + 1
            continue
    proxies_left = False

def validate_proxies(proxy_list_raw, fast = False):
    global valid_proxies
    valid_proxies = []
    global q
    global proxies_left
    global bad_proxies
    global good_proxies
    global good_proxies_ips
    global fast_shortcut
    counter = 0
    q.queue.clear()
    for p in proxy_list_raw:
        if counter >= proxy_validate_limit_config:
            break
        q.put(p)
        counter += 1

    # Load good proxies
    good_proxies.clear()
    with open(good_proxies_file_config, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            good_proxies[line] = True
            good_proxies_ips[get_ip_proxy(line)] = True

    # Load bad proxies
    bad_proxies.clear()
    with open(bad_proxies_file_config, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            space_index = line.find(" ")
            if (space_index >= 0):
                bad_proxies[line[0 : space_index]] = int(line[space_index + 1 : ])
            else:
                bad_proxies[line] = 1

    # Set fast shortcut preference
    fast_shortcut = fast

    if (q.qsize() > 0):
        threads = []
        for _ in range(validate_threads_config):
            threads.append(threading.Thread(target=check_proxies, daemon=True))
        for t in threads:
            t.start()
        proxies_left = True
        while proxies_left:
            if keyboard.is_pressed('q'):
                print("Q Pressed - Quitting Program")
                validate_exit_finally()
                sys.exit(1)
        # Wait for all threads to finish
        for t in threads:
            t.join()

        # Save bad proxies
        with open(bad_proxies_file_config, "w") as f:
            for key in bad_proxies:
                f.write(key + " " + str(bad_proxies[key]) + "\n")
    return valid_proxies

# Find one proxy to use
# def get_one_valid(proxy_list_raw):
#     for proxy in proxy_list_raw:
#         try:
#             session = requests.session()
#             session.proxies = {}

#             session.proxies['http'] = proxy
#             session.proxies['https'] = proxy

#             r = session.get("https://httpbin.org/ip", timeout=3)
#             index = proxy.rfind(":")
#             if(index > 0):
#                 proxyIP = proxy[0:index]
#                 if ("\"origin\": \"" + proxyIP + "\"") in (r.text):
#                     return proxy
#         except:
#             continue
#     return None


# We may continue adding more and more resources to build a large list of proxies
def get_public_proxies(fast = False, configuration = {}):
    global good_proxies_file_config
    global bad_proxies_file_config

    print(configuration)
    if "good_proxies_file_config" in configuration:
        good_proxies_file_config = configuration["good_proxies_file_config"]
    if "bad_proxies_file_config" in configuration:
        bad_proxies_file_config = configuration["bad_proxies_file_config"]
    print(good_proxies_file_config)

    proxyList = []
    validProxies = []
    proxyStarters = []

    # Load from https://docs.proxyscrape.com/
    get_proxies_proxy_scrape(proxyStarters)

    valid_proxies_res = validate_proxies(proxyStarters, fast = fast)
    validProxies.extend(valid_proxies_res)
    # print(validProxies)
    
    # # Get some valid proxies to use to scrape other proxy lists
    # # Load from https://www.proxynova.com/proxy-server-list/
    # get_proxies_proxy_nova(proxyList, valid_proxies_res)

    # Load from https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt
    # get_proxies_github_proxifly(proxyList)

    valid_proxies_res = validate_proxies(proxyList, fast = fast)
    validProxies.extend(valid_proxies_res)

    # with open("../_latest_good_proxies.txt", "w") as f:
    #     for proxy in validProxies:
    #         f.write(proxy + "\n")

    return validProxies

if __name__ == '__main__':
    get_public_proxies(fast = False)
