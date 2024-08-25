import json
import sys
import time
import traceback
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller, Listener
import pyautogui
if sys.platform == "win32":
    import win32clipboard
elif sys.platform == "darwin":
    from AppKit import NSPasteboard, NSStringPboardType
from Source.HarryGoogleSearch.googlesearch import filter_result
from Source.Parsing.Parser import parseBody, parseUnitPrice, parseScientficPrice

PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
REPARSE_LIST_FILE = "Files/ReparseList.txt"
FINISHED_LIST_FILE = "Files/FinishedParsingList.txt"

INITIAL_DELAY = 5
LOAD_DELAY = 12
TNT_LOAD_DELAY = 17
NO_FRILLS_LOAD_DELAY = 25
LOBLAWS_LOAD_DELAY = 30
INSPECT_DELAY = 0.5
COPY_DELAY = 1
KEYBOARD_CMD_DELAY = 0.1
INSPECT_MOUSE_CLICK_X = 1550
INSPECT_MOUSE_CLICK_Y = 177

def join_direct_spans_in_div(div):
    text_parts = []
    toRemove = []
    for child in div.children:
        if child.name == 'span':
            text_parts.append(child.get_text())
            toRemove.append(child)

    # Remove the span after extracting the text
    for child in toRemove:
        child.decompose()

    joined_text = ''.join(text_parts)
    div.insert(0, joined_text)

def manualParseBody(html, product_name, url):
    if "walmart" in url.lower():
        soup = BeautifulSoup(html, features="html.parser")
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

        # Extract hero image
        productImageUrl = None
        activeImageDiv = soup.find_all("div", {"data-testid": "hero-image-container"})

        if len(activeImageDiv) > 0:
            productImageList = activeImageDiv[0].find_all("img")

            if len(productImageList) > 0:
                productImageUrl = productImageList[0]["src"]
        
        if productImageUrl is not None:
            return (productName, productUnitPrice, productScientificPrice, productImageUrl)
        else:
            return (productName, productUnitPrice, productScientificPrice)
    elif "tntsupermarket" in url.lower():
        soup = BeautifulSoup(html, 'html.parser')
        productNameElement = soup.find_all("h1", {"class": "productFullDetail-productName-6ZL"})
        productName = None
        if len(productNameElement) > 0:
            productName = productNameElement[0].get_text()
        
        productPriceElement = soup.find_all("div", {"class": "productFullDetail-productPrice-Aod"})
        productPriceStr = ""
        if len(productPriceElement) > 0:
            for child in productPriceElement[0].children:
                if child.name == 'span':
                    productPriceStr += child.get_text()
        weightElement = soup.find_all("div", {"class": "productFullDetail-weightUom-M4U"})
        if len(weightElement) > 0:
            for child in weightElement[0].children:
                if child.name == 'span':
                    productPriceStr += child.get_text()
            productPriceStr += weightElement[0].get_text()
        print(productPriceStr)
        productUnitPrice = parseUnitPrice(productPriceStr)

        productScientificPrice = parseScientficPrice(productPriceStr)
        # If the unit price is not scientific, we will get the listed
        # scientific price
        if productScientificPrice[0] <= 0:
            scientificElement = soup.find_all("div", {"class": "productFullDetail-priceAverageWeightg-Wxq"})
            productScientificPriceStr = ""
            if len(scientificElement) > 0:
                nested_spans = scientificElement[0].find_all("span")
                for span in nested_spans:
                    productScientificPriceStr += span.get_text()
            productScientificPrice = parseScientficPrice(productScientificPriceStr)

        # Extract image in carousel
        productImageUrl = None
        imageCarousel = soup.find_all(True, {"class": "carousel-imageDisplay-yEC"})

        if len(imageCarousel) > 0:
            productImage = imageCarousel[0].find_all("img", {"class": "image-loaded-jTo"})
            if len(productImage) > 0:
                productImageUrl = productImage[0]["src"]
                # Tnt uses relative links so we add the base prefix for relative links
                if not productImageUrl.startswith("https://www.tntsupermarket.com/") or productImageUrl.startswith("/"):
                    if productImageUrl.startswith("/"):
                        productImageUrl = "https://www.tntsupermarket.com" + productImageUrl
                    else:
                        productImageUrl = "https://www.tntsupermarket.com/" + productImageUrl

        if productImageUrl is not None:
            return (productName, productUnitPrice, productScientificPrice, productImageUrl)
        else:
            return (productName, productUnitPrice, productScientificPrice)
    elif "nofrills" in url.lower():
        soup = BeautifulSoup(html, 'html.parser')

        productInfoDivList = soup.find_all("div", {"class": "product-details-page-details"})
        if len(productInfoDivList) > 0:
            productInfoDiv = productInfoDivList[0]
        else:
            return (None, None, None)

        productBrandElement = productInfoDiv.find_all("span", {"class": "product-name__item--brand"})
        productNameElement = productInfoDiv.find_all("h1", {"class": "product-name__item--name"})
        productSize = productInfoDiv.find_all("span", {"class": "product-name__item--package-size"})
        productName = None
        if len(productNameElement) > 0:
            productName = productNameElement[0].get_text().strip()
        if len(productBrandElement) > 0:
            productName = productBrandElement[0].get_text().strip() + " " + productName
        if len(productSize) > 0:
            productName = productName + " " + productSize[0].get_text().strip()

        productPriceStr = ""
        priceInfoSpan = productInfoDiv.find_all("span", {"class": "selling-price-list__item__price"})
        if len(priceInfoSpan) > 0:
            for child in priceInfoSpan[0].children:
                if child.name == 'span':
                    productPriceStr += child.get_text()
        productUnitPrice = parseUnitPrice(productPriceStr)

        productScientificPrice = parseScientficPrice(productPriceStr)

        if productScientificPrice[0] <= 0:
            scientificElemList = productInfoDiv.find_all("li", {"class": "comparison-price-list__item"})
            if len(scientificElemList) > 0:
                scientificElemSpan = next(scientificElemList[0].children)
                productScientificPriceStr = ""
                for child in scientificElemSpan.children:
                    if child.name == 'span':
                        productScientificPriceStr += child.get_text()
                productScientificPrice = parseScientficPrice(productScientificPriceStr)

        # Extract the active image
        productImageUrl = None
        imageTrackDiv = productInfoDiv.find_all("div", {"class": "slick-track"})

        if len(imageTrackDiv) > 0:
            activeDiv = imageTrackDiv[0].find_all("div", {"data-index": "0"})

            if len(activeDiv) > 0:
                productImage = activeDiv[0].find_all("img")
                productImageUrl = productImage[0]["src"]

        if productImageUrl is not None:
            return (productName, productUnitPrice, productScientificPrice, productImageUrl)
        else:
            return (productName, productUnitPrice, productScientificPrice)
    elif "loblaws" in url.lower():
        soup = BeautifulSoup(html, 'html.parser')
        
        productInfoDivList = soup.find_all("div", {"class": "product-details-page-details"})
        if len(productInfoDivList) > 0:
            productInfoDiv = productInfoDivList[0]
        else:
            return (None, None, None)

        productBrandElement = productInfoDiv.find_all("span", {"class": "product-name__item--brand"})
        productNameElement = productInfoDiv.find_all("h1", {"class": "product-name__item--name"})
        productSize = productInfoDiv.find_all("span", {"class": "product-name__item--package-size"})
        productName = None
        if len(productNameElement) > 0:
            productName = productNameElement[0].get_text().strip()
        if len(productBrandElement) > 0:
            productName = productBrandElement[0].get_text().strip() + " " + productName
        if len(productSize) > 0:
            productName = productName + " " + productSize[0].get_text().strip()

        productPriceStr = ""
        priceInfoSpan = productInfoDiv.find_all("span", {"class": "selling-price-list__item__price"})
        if len(priceInfoSpan) > 0:
            for child in priceInfoSpan[0].children:
                if child.name == 'span':
                    productPriceStr += child.get_text()
        productUnitPrice = parseUnitPrice(productPriceStr)

        productScientificPrice = parseScientficPrice(productPriceStr)

        if productScientificPrice[0] <= 0:
            scientificElemList = productInfoDiv.find_all("li", {"class": "comparison-price-list__item"})
            if len(scientificElemList) > 0:
                scientificElemSpan = next(scientificElemList[0].children)
                productScientificPriceStr = ""
                for child in scientificElemSpan.children:
                    if child.name == 'span':
                        productScientificPriceStr += child.get_text()
                productScientificPrice = parseScientficPrice(productScientificPriceStr)

        # Extract image
        productImageUrl = None
        imageList = productInfoDiv.find_all("div", {"class": "product-image-list"})
        
        if len(imageList) > 0:
            productImage = imageList[0].find_all("img")
            if len(productImage) > 0:
                productImageUrl = productImage[0]["src"]

        # Sometimes, if the product is given by a carousel, it can be displayed differently
        if productImageUrl is None:
            imageTrackDiv = productInfoDiv.find_all("div", {"class": "slick-track"})

            if len(imageTrackDiv) > 0:
                activeDiv = imageTrackDiv[0].find_all("div", {"data-index": "0"})

                if len(activeDiv) > 0:
                    productImage = activeDiv[0].find_all("img")
                    productImageUrl = productImage[0]["src"]
        
        if productImageUrl is not None:
            return (productName, productUnitPrice, productScientificPrice, productImageUrl)
        else:
            return (productName, productUnitPrice, productScientificPrice)
    else:
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')

        # Find all div tags and join text within direct child spans
        for div in soup.find_all('div'):
            join_direct_spans_in_div(div)

        body = soup.find('body')
        bodyText = body.get_text(separator="\n")

        # Remove blank lines
        bodyLines = bodyText.splitlines()
        resultLines = []
        for bodyLine in bodyLines:
            if bodyLine.strip() != "":
                resultLines.append(bodyLine)
        bodyLines = "\n".join(resultLines)

        # print(bodyText)
        return parseBody(bodyText, product_name)

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
parseListFile.close()

keyboard = Controller()
print("Finished loading parseList, waiting 5 seconds to start")
time.sleep(INITIAL_DELAY)

# Open the inspect window for the tab
# Enter inspect mode
if sys.platform == "win32":
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)
elif sys.platform == "darwin":
    keyboard.press(Key.cmd)
    keyboard.press(Key.alt)
keyboard.press('i')
time.sleep(KEYBOARD_CMD_DELAY)
if sys.platform == "win32":
    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)
elif sys.platform == "darwin":
    keyboard.release(Key.cmd)
    keyboard.release(Key.alt)
keyboard.release('i')
time.sleep(INSPECT_DELAY)

# Jump to search bar
if sys.platform == "win32":
    keyboard.press(Key.ctrl)
elif sys.platform == "darwin":
    keyboard.press(Key.cmd)
keyboard.press('l')
time.sleep(KEYBOARD_CMD_DELAY)
if sys.platform == "win32":
    keyboard.release(Key.ctrl)
elif sys.platform == "darwin":
    keyboard.release(Key.cmd)
keyboard.release('l')

for index in range(0, len(parseList)):
    productLine = parseList[index]
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        productPart = productLine[0 : lastSpaceIndex]
        urlPart = productLine[lastSpaceIndex + 1 : ]
        print("Parsing " + str(len(parseList) - index) + ": " + productLine)

        for ch in urlPart:
            keyboard.type(ch)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        if "tntsupermarket" in urlPart:
            time.sleep(TNT_LOAD_DELAY)
        elif "nofrills" in urlPart:
            time.sleep(NO_FRILLS_LOAD_DELAY)
        elif "loblaws" in urlPart:
            time.sleep(LOBLAWS_LOAD_DELAY)
        else:
            time.sleep(LOAD_DELAY)

        pyautogui.click(INSPECT_MOUSE_CLICK_X, INSPECT_MOUSE_CLICK_Y) 

        if sys.platform == "win32":
            keyboard.press(Key.ctrl)
        elif sys.platform == "darwin":
            keyboard.press(Key.cmd)
        keyboard.press('c')
        time.sleep(KEYBOARD_CMD_DELAY)
        if sys.platform == "win32":
            keyboard.release(Key.ctrl)
        elif sys.platform == "darwin":
            keyboard.release(Key.cmd)
        keyboard.release('c')
        time.sleep(COPY_DELAY)

        # get clipboard data
        if sys.platform == "win32":
            win32clipboard.OpenClipboard()
            html = win32clipboard.GetClipboardData()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        elif sys.platform == "darwin":
            pb = NSPasteboard.generalPasteboard()
            html = pb.stringForType_(NSStringPboardType)
            pb.clearContents()

        try:
            if html is None:
                print("\033[93m" + "Warning: HTML was none. Check if inspect mode is on. Page potentially did not load fast enough." + "\033[0m")
                print("\033[92mCreating new tab\033[0m")

                # Create a new tab and enter inspect mode
                if sys.platform == "win32":
                    keyboard.press(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.press(Key.cmd)
                keyboard.press('t')
                time.sleep(KEYBOARD_CMD_DELAY)
                if sys.platform == "win32":
                    keyboard.release(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.release(Key.cmd)
                keyboard.release('t')

                if sys.platform == "win32":
                    keyboard.press(Key.ctrl)
                    keyboard.press(Key.shift)
                elif sys.platform == "darwin":
                    keyboard.press(Key.cmd)
                    keyboard.press(Key.alt)
                keyboard.press('i')
                time.sleep(KEYBOARD_CMD_DELAY)
                if sys.platform == "win32":
                    keyboard.release(Key.ctrl)
                    keyboard.release(Key.shift)
                elif sys.platform == "darwin":
                    keyboard.release(Key.cmd)
                    keyboard.release(Key.alt)
                keyboard.release('i')
                time.sleep(INSPECT_DELAY)

                if sys.platform == "win32":
                    keyboard.press(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.press(Key.cmd)
                keyboard.press('1')
                time.sleep(KEYBOARD_CMD_DELAY)
                if sys.platform == "win32":
                    keyboard.release(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.release(Key.cmd)
                keyboard.release('1')

                if sys.platform == "win32":
                    keyboard.press(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.press(Key.cmd)
                keyboard.press('w')
                time.sleep(KEYBOARD_CMD_DELAY)
                if sys.platform == "win32":
                    keyboard.release(Key.ctrl)
                elif sys.platform == "darwin":
                    keyboard.release(Key.cmd)
                keyboard.release('w')

                print("\033[91mCould not retrieve, set to reparse: \033[0m" + productLine)
                with open(REPARSE_LIST_FILE, "a") as reparseFile:
                    reparseFile.write(productLine + "\n")
            else:
                tupleAns = manualParseBody(html, product_name=productPart, url=urlPart)
                if tupleAns[0] is None or tupleAns[1] is None or tupleAns[1] == -1:
                    # We have to reparse these results
                    print("\033[91mCould not retrieve, set to reparse: \033[0m" + productLine)
                    with open(REPARSE_LIST_FILE, "a") as reparseFile:
                        reparseFile.write(productLine + "\n")
                else:
                    # Output the resulting result and indicate that it was parsed
                    with open(PRICE_RESULTS_FILE, "a") as priceResFile:
                        # Console logging
                        print(productLine)
                        print(tupleAns[0])
                        print(tupleAns[1])
                        if len(tupleAns) > 3:
                            print(str(tupleAns[2]))
                            print("Image: " + tupleAns[3] + "\n")
                        else:
                            print(str(tupleAns[2]) + "\n")
                        
                        # Saving to file
                        if len(tupleAns) > 3:
                            priceResFile.write(productLine + " | Image: " + tupleAns[3] + "\n") # Product Line and Image
                        else:
                            priceResFile.write(productLine + "\n") # Product Line
                        priceResFile.write(str(tupleAns[0]) + "\n") # Name
                        priceResFile.write(str(tupleAns[1]) + "\n") # Price
                        priceResFile.write(str(tupleAns[2]) + "\n\n") # Scientific Price
                    with open(FINISHED_LIST_FILE, "a") as finishedFile:
                        finishedFile.write(productLine + "\n")
        except:
            print(traceback.format_exc())
            print("\033[91mCould not retrieve, set to reparse: \033[0m" + productLine)
            with open(REPARSE_LIST_FILE, "a") as reparseFile:
                reparseFile.write(productLine + "\n")

        # Reset search bar
        if sys.platform == "win32":
            keyboard.press(Key.ctrl)
        elif sys.platform == "darwin":
            keyboard.press(Key.cmd)
        keyboard.press('l')
        time.sleep(KEYBOARD_CMD_DELAY)
        if sys.platform == "win32":
            keyboard.release(Key.ctrl)
        elif sys.platform == "darwin":
            keyboard.release(Key.cmd)
        keyboard.release('l')
        keyboard.press(Key.delete)
        keyboard.release(Key.delete)

    
