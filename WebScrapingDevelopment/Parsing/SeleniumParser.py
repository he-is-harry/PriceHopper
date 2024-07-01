from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Constants declared
url = "https://www.nofrills.ca/turkey-5-7kg-frozen/p/21209114_EA?source=nspt"
product_name = "banana"

options = webdriver.ChromeOptions() 
options.add_argument("--headless")
options.page_load_strategy = "eager"

# Initialize WebDriver (assuming you have chromedriver installed)
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# Navigate to the URL of the page you want to scrape
driver.get(url)
time.sleep(10)

bodyText = driver.find_element(By.TAG_NAME, "body").text

# Close the WebDriver
driver.quit()

# Print all the text
f = open("text.txt", "w")
f.write(bodyText)
f.close()

# Extract the name, unit price, and scientific price of the product
# 1. We search for the product name and try to match it with lines that
# we like (we try to take the shorter lines), those should be the name
# 2. Then, look for $ and those will indicate prices
# 3. We will evaluate the prices if they are able to be parsed 
#   - We give points to prices which are closer to lines with the product name
#   - To differentiate between unit prices and scientific prices, we want to give
#     give points to unit prices which are shorter and then we would choose 
#     scientific prices which is closest to the unit price (could be the same line as the unit price)
# Use a 10 to 1 weighting comparing how close an object is to line with the product name
# and the length of the price

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


lineList = bodyText.split("\n")

# Create a map of indices of lines with the product name
lowerProdName = product_name.lower()
productNameIndexList = []
noProductName = False
for i in range(len(lineList)):
    if lowerProdName in lineList[i].lower():
        productNameIndexList.append(i)

if len(productNameIndexList) == 0:
    noProductName = True
    # We try to favour prices that are in the middle of the page then
    productNameIndexList.append(len(lineList) / 2)

unitPriceMap = {}
scientificPriceMap = {}

possiblePricesFile = open("PossiblePrices.txt", "a")

for lineIndex in range(len(lineList)):
    if ('$' in lineList[lineIndex]) or ('¢' in lineList[lineIndex]):
        # Save possible prices for future reference
        if(lineIndex > 0):
            possiblePricesFile.write(lineList[lineIndex - 1])
        possiblePricesFile.write(lineList[lineIndex])
        if(lineIndex < len(lineList) - 1):
            possiblePricesFile.write(lineList[lineIndex + 1] + "\n")

        # Put an entry for both the unit and scientific price if possible
        res = parseUnitPrice(lineList[lineIndex])
        if res > 0:
            unitPriceMap[lineIndex] = res
        res = parseScientficPrice(lineList[lineIndex])
        if res[0] > 0:
            scientificPriceMap[lineIndex] = res
possiblePricesFile.close()

# Evaluate the unit prices to see which is the most likely to be the unit price
def evaluateUnitPrice(index, lineList, productNameIndexList):
    # Use a par based system, we add the distance away from the closest product name
    # times 10 and add the length of the index
    minDist = abs(productNameIndexList[0] - index)
    for i in range(1, len(productNameIndexList)):
        if abs(productNameIndexList[i] - index) < minDist:
            minDist = abs(productNameIndexList[i] - index)
    return minDist * 10 + len(lineList[index])

productNameAns = None
productUnitPrice = None
productScientificPrice = None

# Take the unit price as the line that has the best score (lowest - since we use a par system)
bestScore = float("inf")
unitPriceIndex = -1
for keyIndex in unitPriceMap:
    res = evaluateUnitPrice(keyIndex, lineList, productNameIndexList)
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
    
    bestScore = float("inf")
    scientificPriceIndex = -1
    if scientificPriceMap:
        for index in scientificPriceMap:
            if abs(unitPriceIndex - index) < bestScore:
                bestScore = abs(unitPriceIndex - index)
                scientificPriceIndex = index
        productScientificPrice = scientificPriceMap[scientificPriceIndex]

print(productNameAns)
print(productUnitPrice)
print(productScientificPrice)



        



