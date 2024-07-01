import random
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver as webdriverwire
from seleniumwire.webdriver import Chrome as ChromeWire
import time
import inflect

# Parser.py provides the main function: parseSite
# which will scrape a website and take the price of the product displayed
# 1. Map the corresponding parse function to the site
# 2. Scrape the site and convert it to text
# 3. Analyze the text for good matches of product name and price

IMPLICIT_WAIT = 3
REQUESTS_TIMEOUT = 10
SELENIUM_DELAY = 15
SELENIUM_WIRE_DELAY = 15

PRICE_LOGGING_ENABLED = False
PRICE_LOGGING_FILE = "Source/Parsing/PossiblePrices.txt"

def parseUnitPriceStrict(priceStr):
    try:
        return float(priceStr)
    except ValueError:
        return -1

def parseUnitPrice(priceStr):
    # Take the longest price string we can parse after the dollar sign
    # or the price before the cents sign (since cents goes after number)
    dollarIndex = priceStr.find('$')
    centsIndex = priceStr.find('¢')
    if centsIndex < 0:
        workStr = priceStr[dollarIndex + 1:]
    elif dollarIndex < 0:
        workStr = priceStr[0 : centsIndex]
    else:
        # Dollar will take precedence over cents
        workStr = priceStr[dollarIndex + 1:]
    
    while len(workStr) > 0:
        priceNum = parseUnitPriceStrict(workStr)
        if priceNum >= 0:
            return priceNum
        else:
            if dollarIndex >= 0:
                workStr = workStr[:-1]
            else:
                workStr = workStr[1:]
    return -1 # Could not parse unit price

# Currently, we have a very strict scientific price parser
# we will only accept prices of the form
# $[price]/[number][unit]
# We will return a tuple (price: float, number-units: int, unit: str)
# Valid units: g, kg, mg, L, ml, lb, lbs, oz (we put to lower case though)

def validUnit(unitStr):
    return (unitStr == "g" or unitStr == "kg" or unitStr == "mg" or unitStr == "l"
            or unitStr == "ml" or unitStr == "lb" or unitStr == "lbs" or unitStr == "oz")

def parseScientificUnit(unitStr):
    # Take as many numeric value as we can, which will represent an float
    # quantity of the number of units
    textStart = 0
    while textStart < len(unitStr) and ((unitStr[textStart] >= '0' and unitStr[textStart] <= '9') or unitStr[textStart] == '.'):
        textStart += 1
    if textStart == 0:
        unitNum = 1
    else:
        try:
            unitNum = float(unitStr[0 : textStart])
        except ValueError:
            return (-1, "")
    unitRem = unitStr[textStart:].lower()
    if validUnit(unitRem):
        return (unitNum, unitRem)
    else:
        return (-1, "")
    

def parseScientficPriceStrict(priceStr):
    # First isolate the price, then defer the parsing of the units
    dollarIndex = priceStr.find('$')
    centsIndex = priceStr.find('¢')
    slashIndex = priceStr.find('/')
    if (dollarIndex < 0 and centsIndex < 0) or slashIndex < 0:
        return (-1, 0, "")
    # Declare the price per unit
    if centsIndex < 0:
        workStr = priceStr[dollarIndex + 1 : slashIndex]
    elif dollarIndex < 0:
        workStr = priceStr[0 : centsIndex]
    else:
        # Dollar takes precedence over cents
        workStr = priceStr[dollarIndex + 1 : slashIndex]
    
    try:
        # Ideally, we assume that we don't have to adjust the workStr
        pricePerUnit = float(workStr)
    except ValueError:
        return (-1, 0, "")

    # Find the unit tuple
    unitTuple = parseScientificUnit(priceStr[slashIndex + 1:])
    if unitTuple[0] < 0:
        return (-1, 0, "")
    else:
        return (pricePerUnit, unitTuple[0], unitTuple[1])

def parseScientficPrice(priceStr):
    # Remove all the white space in the string, we assume we only have spaces
    priceStr = priceStr.replace(" ", "")
    # Take the longest scientific price, we include the dollar sign or cents
    dollarIndex = priceStr.find('$')
    centsIndex = priceStr.find('¢')
    if centsIndex < 0:
        workStr = priceStr[dollarIndex:]
    elif dollarIndex < 0:
        # Find the longest valid price we can use to start the string
        start = centsIndex
        # We allow floating point cents, although this is slighly nonsensical
        while (start - 1 >= 0 and (priceStr[start - 1] >= '0' and priceStr[start - 1] <= '9')
            or priceStr[start - 1] == '.'):
            start -= 1
        workStr = priceStr[start:]
    else:
        # Dollar takes precedence over cents
        workStr = priceStr[dollarIndex:]
    
    while len(workStr) > 0:
        scientificPriceTuple = parseScientficPriceStrict(workStr)
        if scientificPriceTuple[0] >= 0:
            return scientificPriceTuple
        else:
            workStr = workStr[:-1]
    return (-1, 0, "")

# Evaluate helper function to find closest product name to a unit price index
# we return "" if there are no product names
def findClosestProductName(unitPriceIndex, lineList, productNameIndexList):
    bestScore = float("inf")
    productNameIndex = -1
    for index in productNameIndexList:
        if abs(unitPriceIndex - index) < bestScore:
            bestScore = abs(unitPriceIndex - index)
            productNameIndex = index
    if productNameIndex >= 0:
        return lineList[productNameIndex]
    else:
        return ""
    
# We find the number of words that match, case insensitive
# we assume the product word list is already to lower
def findNumWordMatches(possibleName, product_word_list):
    ans = 0
    possibleNameLower = possibleName.lower()
    for word in product_word_list:
        if word in possibleNameLower:
            ans += 1
    return ans

# Evaluate the unit prices to see which is the most likely to be the unit price
def evaluateUnitPrice(index, lineList, productNameIndexList, product_word_list):
    # Use a par based system, we add the distance away from the closest product name
    # times 10 and add 0.5 x length of the price line
    # We also try to take closer to the top, so we add 0.1 x index
    # ... refer to document for scoring
    minDist = abs(productNameIndexList[0] - index)
    for i in range(1, len(productNameIndexList)):
        if abs(productNameIndexList[i] - index) < minDist:
            minDist = abs(productNameIndexList[i] - index)
    score = minDist * 10
    score += 0.5 * len(lineList[index])
    score += 0.1 * index
    closestProductName = findClosestProductName(index, lineList, productNameIndexList)
    score += 0.2 * len(closestProductName)
    score -= 5 * findNumWordMatches(closestProductName, product_word_list)
    return score

# parseBody: str -> (str, float, (float, float, str))
def parseBody(bodyText, product_name):
    lineList = bodyText.split("\n")

    # Create a map of indices of lines with the product name
    # so long as one of the words (or the plural) in the product name is 
    # in the name, we consider it to be valid
    product_word_list = product_name.lower().split(" ")
    plural_engine = inflect.engine()
    plural_words = []
    for word in product_word_list:
        plural_words.append(plural_engine.plural(word).lower())
    product_word_list.extend(plural_words)
    productNameIndexList = []
    noProductName = False
    for i in range(len(lineList)):
        # Ensure that the exists at least one word match and the product name is at
        # most 120 characters
        if findNumWordMatches(lineList[i], product_word_list) and len(lineList[i]) <= 120:
            productNameIndexList.append(i)

    if len(productNameIndexList) == 0:
        noProductName = True
        # We try to favour prices that are in the middle of the page then
        productNameIndexList.append(len(lineList) / 2)

    unitPriceMap = {}
    scientificPriceMap = {}

    if PRICE_LOGGING_ENABLED:   
        possiblePricesFile = open(PRICE_LOGGING_FILE, "a")

    for lineIndex in range(len(lineList)):
        if ('$' in lineList[lineIndex]) or ('¢' in lineList[lineIndex]):
            # Put an entry for both the unit and scientific price if possible
            res = parseUnitPrice(lineList[lineIndex])
            if res > 0:
                unitPriceMap[lineIndex] = res
            res = parseScientficPrice(lineList[lineIndex])
            if res[0] > 0:
                scientificPriceMap[lineIndex] = res

            # Save possible prices for future reference
            if PRICE_LOGGING_ENABLED:
                if(lineIndex > 0):
                    possiblePricesFile.write(lineList[lineIndex - 1] + "\n")
                possiblePricesFile.write(lineList[lineIndex] + "\t\t\tPrice: " + str(parseUnitPrice(lineList[lineIndex])) + "\tScientific: " + str(parseScientficPrice(lineList[lineIndex])) + "\n")
                if(lineIndex < len(lineList) - 1):
                    possiblePricesFile.write(lineList[lineIndex + 1] + "\n")
                possiblePricesFile.write("\n")

    if PRICE_LOGGING_ENABLED:
        possiblePricesFile.close()

    productNameAns = None
    productUnitPrice = None
    productScientificPrice = None

    # Take the unit price as the line that has the best score (lowest - since we use a par system)
    bestScore = float("inf")
    unitPriceIndex = -1
    for keyIndex in unitPriceMap:
        res = evaluateUnitPrice(keyIndex, lineList, productNameIndexList, product_word_list)
        if res < bestScore:
            bestScore = res
            unitPriceIndex = keyIndex

    if unitPriceIndex >= 0:
        productUnitPrice = unitPriceMap[unitPriceIndex]

    # Take the scientific price and the product name that is closest to the unit price
    if(unitPriceIndex >= 0):
        bestScore = float("inf")
        productNameIndex = -1
        if not noProductName:
            for index in productNameIndexList:
                if abs(unitPriceIndex - index) < bestScore:
                    bestScore = abs(unitPriceIndex - index)
                    productNameIndex = index
            productNameAns = lineList[productNameIndex]
        
        # Scientific price must be within 8 lines of the unit price line
        bestScore = float("inf")
        scientificPriceIndex = -1
        for index in scientificPriceMap:
            if abs(unitPriceIndex - index) < bestScore and abs(unitPriceIndex - index) <= 8:
                bestScore = abs(unitPriceIndex - index)
                scientificPriceIndex = index
        if scientificPriceIndex >= 0:
            productScientificPrice = scientificPriceMap[scientificPriceIndex]
    return (productNameAns, productUnitPrice, productScientificPrice)

def parseSiteWalmart(url, proxy):
    # This parse site only works for walmart
    session = requests.session()
    # Use proxy
    if proxy is not None:
        session.proxies = {}
        session.proxies['http'] = proxy
        session.proxies['https'] = proxy

    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 10; SM-F700N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    ]

    headers = {"User-Agent": random.choice(agents)}
    page = session.get(url, headers=headers, timeout=REQUESTS_TIMEOUT)

    soup = BeautifulSoup(page.text, features="html.parser")

    next_data = soup.find('script', {'id': '__NEXT_DATA__'})
    if next_data is not None:
        parsed_json = json.loads(next_data.text)
        skip_parse = False
    else:
        skip_parse = True

    # Declare product variables
    if not skip_parse:
        try:
            productName: str = parsed_json['props']['pageProps']['initialData']['data']['product']['name']
        except (TypeError, KeyError):
            productName = None
        try:
            product_price_cur: str = parsed_json['props']['pageProps']['initialData']['data']['product']['priceInfo']['currentPrice']['priceString']
        except (TypeError, KeyError):
            product_price_cur = None
        try:
            product_price_unit: str = parsed_json['props']['pageProps']['initialData']['data']['product']['priceInfo']['unitPrice']['priceString']
        except (TypeError, KeyError):
            product_price_unit = None

        if product_price_cur is not None:
            productUnitPrice = parseUnitPrice(product_price_cur)
        else:
            productUnitPrice = None
        if product_price_unit is not None:
            productScientificPrice = parseScientficPrice(product_price_unit)
        else:
            productScientificPrice = None
    else:
        productName = None
        productUnitPrice = None
        productScientificPrice = None

    # Add an extra check, if we find no values, we might be blocked
    # so send a warning
    # if productName is None and productUnitPrice is None and productScientificPrice is None:
    #     print("No read, possible block: " + url)
    #     f = open("noRead.html", "w")
    #     f.write(str(soup))
    #     f.close()
    
    return (productName, productUnitPrice, productScientificPrice)

def parseSiteSeleniumWire(url, product_name, proxy):
    # Define the Chrome webdriver options
    options = webdriverwire.ChromeOptions() 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    # By default, Selenium waits for all resources to download before taking actions.
    # However, we don't need it as the page is populated with dynamically generated JavaScript code.
    options.page_load_strategy = "none"

    # Use proxy
    if proxy is not None:
        sw_options = {
            'proxy': {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
        }
    else:
        sw_options = {}

    # Pass the defined options objects to initialize the web driver 
    driver = ChromeWire(options=options, seleniumwire_options=sw_options) 
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    driver.implicitly_wait(IMPLICIT_WAIT)
    # Create a request interceptor
    def interceptor(request):
        del request.headers['User-Agent']  # Delete the header first
        request.headers['User-Agent'] = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15"
    # Set the interceptor on the driver
    driver.request_interceptor = interceptor
    driver.get(url) 
    time.sleep(SELENIUM_WIRE_DELAY)
    bodyText = driver.find_element(By.TAG_NAME, "body").text
    # Close the WebDriver
    driver.quit()
    return parseBody(bodyText, product_name)

def parseSite(url, product_name, proxy = None):
    # Check if the site url, to change the corresponding scraper
    if "walmart" in url.lower():
        # Use requests to scrape
        return parseSiteWalmart(url, proxy)
    elif "foodbasics" in url.lower():
        # Use selenium-wire
        return parseSiteSeleniumWire(url, product_name, proxy)
    else:
        # Use selenium to scrape by default
        options = webdriver.ChromeOptions()
        # Avoid loading images
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        # Use proxy
        if proxy is not None:
            PROXIES = {
                'http': proxy,
                'https': proxy
            }
            proxy_arg = ';'.join('%s=%s' % (k, v) for k, v in PROXIES.items())
            options.add_argument('--proxy-server=%s' % proxy_arg)
        # Run in headless mode to avoid creating browser window
        options.add_argument("--headless=new")
        options.page_load_strategy = "eager"
        # Initialize WebDriver (assuming you have chromedriver installed)
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        # Navigate to the URL of the page you want to scrape
        driver.get(url)
        time.sleep(SELENIUM_DELAY)
        bodyText = driver.find_element(By.TAG_NAME, "body").text
        print(bodyText)
        # Close the WebDriver
        driver.quit()
        return parseBody(bodyText, product_name)

    
