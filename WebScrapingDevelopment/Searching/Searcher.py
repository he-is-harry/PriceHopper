import time
from ParsingCopy.Parser import parseSite
try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
 
NUM_RESULTS = 10
SEARCH_TIME_DELAY = 5
TIME_DELAY = 10

# to search
companyName = "walmart"
productName = "angus steak"
query = companyName + " " + productName

def findNumWordMatches(possibleName, product_word_list):
    ans = 0
    possibleNameLower = possibleName.lower()
    for word in product_word_list:
        if word in possibleNameLower:
            ans += 1
    return ans
 
bestScore = float("inf")
bestUrl = None
counter = 0
product_name_list = productName.lower().split(" ")
for url in search(query, tld="com", num=5, stop=NUM_RESULTS, pause=SEARCH_TIME_DELAY):
    print("Trying: " + url)
    tupleAns = parseSite(url, productName)
    score = 0 # Use a par based system
    if tupleAns[0] is not None:
        score -= 12 * findNumWordMatches(tupleAns[0], product_name_list)
    if tupleAns[2] is not None:
        score -= 5
    if tupleAns[1] is not None:
        score -= 10
    if score < bestScore: # Take the highest urls
        bestUrl = url
        bestScore = score
        
    if counter != NUM_RESULTS - 1:
        time.sleep(TIME_DELAY)
    counter += 1

print("Best url: " + bestUrl)

    