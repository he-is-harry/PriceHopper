# We have a relative path here, we expect this file to be run from
# inside the Parsing folder
from Parser import parseSite

parseListFile = open("ParseList.txt", "r")
parseList = parseListFile.read().splitlines()
priceResFile = open("PriceResults.txt", "w")

for productLine in parseList:
    lineArr = productLine.split(" ")
    # To allow our automater to be a bit smarter, we only run when there are
    # two elements in the line
    if len(lineArr) == 2:
        print("Parsing: " + productLine)
        tupleAns = parseSite(lineArr[1], lineArr[0])
        priceResFile.write("Product Line: " + productLine + "\n")
        priceResFile.write("Name: " + str(tupleAns[0]) + "\n")
        priceResFile.write("Price: " + str(tupleAns[1]) + "\n")
        priceResFile.write("Scientific Price: " + str(tupleAns[2]) + "\n\n")

parseListFile.close()
priceResFile.close()