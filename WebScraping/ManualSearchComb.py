import sys
import time
from bs4 import BeautifulSoup
from pynput.keyboard import Key, Controller, Listener
import pyautogui
if sys.platform == "win32":
    import win32clipboard
elif sys.platform == "darwin":
    from AppKit import NSPasteboard, NSStringPboardType
from Source.HarryGoogleSearch.googlesearch import filter_result

COMPANIES_FILE_PATH = "Files/companies.txt"
PRODUCTS_FILE_PATH = "Files/product_types.txt"
SEARCH_RESULTS_FILE_PATH = "Files/TestParseList.txt"

INITIAL_DELAY = 5
SEARCH_DELAY = 6
# INSPECT_DELAY = 2
COPY_DELAY = 1
KEYBOARD_CMD_DELAY = 0.1
INSPECT_MOUSE_CLICK_X = 1532
INSPECT_MOUSE_CLICK_Y = 177

STOP = 10

companies_file = open(COMPANIES_FILE_PATH, "r")
products_file = open(PRODUCTS_FILE_PATH, "r")

companies = companies_file.read().splitlines()
products = products_file.read().splitlines()

wishlist = []
for product in products:
    split_list = product.split("|")
    searchProduct = split_list[0].strip()
    extraProductWords = ""
    if len(split_list) > 1:
        extraProductWords = split_list[1].strip()
    for company in companies:
        wishlist.append(company + " " + searchProduct) # search
        wishlist.append(searchProduct + " " + extraProductWords) # product words to parse with

companies_file.close()
products_file.close()

keyboard = Controller()
print("Finished loading wishlist, waiting 5 seconds to start")
time.sleep(INITIAL_DELAY)

# Jump to search bar
keyboard.press(Key.ctrl)
keyboard.press('l')
time.sleep(KEYBOARD_CMD_DELAY)
keyboard.release(Key.ctrl)
keyboard.release('l')

# Open the inspect window for the tab
# Enter inspect mode
keyboard.press(Key.ctrl)
keyboard.press(Key.shift)
keyboard.press('i')
time.sleep(KEYBOARD_CMD_DELAY)
keyboard.release(Key.ctrl)
keyboard.release(Key.shift)
keyboard.release('i')

for i in range(0, len(wishlist), 2):
    searchComb = wishlist[i]
    product = wishlist[i + 1]
    print("Searching: " + searchComb)

    for ch in searchComb:
        keyboard.type(ch)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(SEARCH_DELAY)

    pyautogui.click(INSPECT_MOUSE_CLICK_X, INSPECT_MOUSE_CLICK_Y) 

    keyboard.press(Key.ctrl)
    keyboard.press('c')
    time.sleep(KEYBOARD_CMD_DELAY)
    keyboard.release(Key.ctrl)
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

    hashes = set()
    count = 0
    results = []

    soup = BeautifulSoup(html, 'html.parser')
    try:
        anchors = soup.find(id='search').findAll('a')
        # Sometimes (depending on the User-agent) there is
        # no id "search" in html response...
    except AttributeError:
        # Remove links of the top bar.
        gbar = soup.find(id='gbar')
        if gbar:
            gbar.clear()
        anchors = soup.findAll('a')

    # Process every anchored URL.
    for a in anchors:

        # Get the URL from the anchor tag.
        try:
            link = a['href']
        except KeyError:
            continue

        # Filter invalid links and links pointing to Google itself.
        link = filter_result(link, include_google_links = False)
        if not link:
            continue

        h = hash(link)
        if h in hashes:
            continue
        hashes.add(h)

        results.append(link)

        count += 1
        if count >= STOP:
            break
    
    print(results)
    with open(SEARCH_RESULTS_FILE_PATH, "a") as searchResultsFile:
        for url in results:
            searchResultsFile.write(product + " " + url + "\n")

    # Reset search bar
    keyboard.press(Key.ctrl)
    keyboard.press('l')
    time.sleep(KEYBOARD_CMD_DELAY)
    keyboard.release(Key.ctrl)
    keyboard.release('l')
    keyboard.press(Key.delete)
    keyboard.release(Key.delete)

sys.exit()

    
