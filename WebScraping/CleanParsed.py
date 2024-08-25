
PARSE_LIST_FILE = "Files/ParseList.txt"
FINISHED_LIST_FILE = "Files/FinishedParsingList.txt"
CLEANED_RESULTS_FILE = "Files/CleanedParseList.txt"

REPARSE_LIST_FILE = "Files/ReparseList.txt"
REMOVE_REPARSE = True

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
parseListFile.close()

resListFile = open(FINISHED_LIST_FILE, "r")
resList = resListFile.read().splitlines()
resListFile.close()

reparseListFile = open(REPARSE_LIST_FILE, "r")
reparseList = reparseListFile.read().splitlines()
reparseListFile.close()

cleanedFile = open(CLEANED_RESULTS_FILE, "w")

resUrlDict = {}

# Remove values with results
for result in range(0, len(resList)):
    productLine = resList[result]
    url = productLine[productLine.rfind(" ") + 1 : ]
    resUrlDict[url] = True

# Remove products set to reparse
for result in range(0, len(reparseList)):
    productLine = reparseList[result]
    url = productLine[productLine.rfind(" ") + 1 : ]
    resUrlDict[url] = True

for productLine in parseList:
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        url = productLine[lastSpaceIndex + 1 : ]
        if url not in resUrlDict:
            cleanedFile.write(productLine + "\n")

cleanedFile.close()