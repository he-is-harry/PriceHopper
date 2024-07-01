from Source.Parsing.Parser import parseSite

PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
priceResFile = open(PRICE_RESULTS_FILE, "a")

for productLine in parseList:
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        productPart = productLine[0 : lastSpaceIndex]
        urlPart = productLine[lastSpaceIndex + 1 : ]
        print("Parsing: " + productLine)
        tupleAns = parseSite(urlPart, productPart)
        priceResFile.write(productLine + "\n") # Product Line
        priceResFile.write(str(tupleAns[0]) + "\n") # Name
        priceResFile.write(str(tupleAns[1]) + "\n") # Price
        priceResFile.write(str(tupleAns[2]) + "\n\n") # Scientific Price

parseListFile.close()
priceResFile.close()