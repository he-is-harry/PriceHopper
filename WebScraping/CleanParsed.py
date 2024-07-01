
PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
CLEANED_RESULTS_FILE = "Files/CleanedParseList.txt"

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
parseListFile.close()

resListFile = open(PRICE_RESULTS_FILE, "r")
resList = resListFile.read().splitlines()
resListFile.close()

cleanedFile = open(CLEANED_RESULTS_FILE, "w")

resUrlDict = {}

for result in range(0, len(resList), 5):
    productLine = resList[result]
    url = productLine[productLine.rfind(" ") + 1 : ]
    resUrlDict[url] = True

for productLine in parseList:
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        url = productLine[lastSpaceIndex + 1 : ]
        if url not in resUrlDict:
            cleanedFile.write(productLine + "\n")

cleanedFile.close()