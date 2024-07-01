import time
from Source.Parsing.Parser import parseSite

PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
REPARSE_LIST_FILE = "Files/ReparseList.txt"
FINISHED_LIST_FILE = "Files/FinishedParsingList.txt"

DELAY = 15

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
parseListFile.close()

for productLine in parseList:
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        productPart = productLine[0 : lastSpaceIndex]
        urlPart = productLine[lastSpaceIndex + 1 : ]
        print("Parsing: " + productLine)
        tupleAns = parseSite(urlPart, productPart)
        if tupleAns[0] is None or tupleAns[1] is None:
            # We have to reparse these results
            print("Could not retrieve, set to reparse: " + productLine)
            with open(REPARSE_LIST_FILE, "a") as reparseFile:
                reparseFile.write(productLine + "\n")
        else:
            # Output the resulting result and indicate that it was parsed
            with open(PRICE_RESULTS_FILE, "a") as priceResFile:
                print(productLine)
                print(tupleAns[0])
                print(tupleAns[1])
                print(str(tupleAns[2]) + "\n")
                priceResFile.write(productLine + "\n") # Product Line
                priceResFile.write(str(tupleAns[0]) + "\n") # Name
                priceResFile.write(str(tupleAns[1]) + "\n") # Price
                priceResFile.write(str(tupleAns[2]) + "\n\n") # Scientific Price
            with open(FINISHED_LIST_FILE, "a") as finishedFile:
                finishedFile.write(productLine + "\n")
        time.sleep(DELAY)

