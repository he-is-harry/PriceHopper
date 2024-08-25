# Python program to save results from PriceList.txt to a postgres database
import os
import sys
import psycopg2
from psycopg2.extensions import parse_dsn
from urllib.parse import urlparse

# Configuration
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
COMPANY_DOMAINS_FILE = "Files/companies.txt"

# Load company domains
companyDict = {}
with open(COMPANY_DOMAINS_FILE, "r") as companiesFile:
    companyLines = companiesFile.read().splitlines()
    for line in companyLines:
        splitIndex = line.find("|")
        companyName = line[ : splitIndex].strip()
        companyDomain = line[ splitIndex + 1 : ].strip()
        companyDict[companyDomain] = companyName

# Get database information
try:
    database_url = os.environ["PRICE_SCRAPING_DATABASE_URL"]
except KeyError:
    print("Database url could not be found, please ensure you have a environment variable named PRICE_SCRAPING_DATABASE_URL")
    sys.exit(0)
try:
    database_username = os.environ["PRICE_SCRAPING_DATABASE_USERNAME"]
except KeyError:
    print("Database username could not be found, please ensure you have a environment variable named PRICE_SCRAPING_DATABASE_USERNAME")
    sys.exit(0)
try:
    database_password = os.environ["PRICE_SCRAPING_DATABASE_PASSWORD"]
except KeyError:
    print("Database password could not be found, please ensure you have a environment variable named PRICE_SCRAPING_DATABASE_PASSWORD")
    sys.exit(0)

# Parsing method to read results from the price results file into a SQL query
# Throws an error if the line cannot be parsed indicating the price result files has
# some inconsistences.
def parseResult(productLine: str, productName: str, productPrice: str, scientificPrice: str):
    imageIndex = productLine.find("| Image:")
    productUrl = "NULL"
    productImageUrl = "NULL"
    if (imageIndex >= 0):
        productImageUrl = productLine[imageIndex + 8 : ].strip()
        standardLine = productLine[ : imageIndex].strip()
        productUrl = standardLine[standardLine.rfind(" ") + 1 : ]
    else:
        productLine = productLine.strip()
        productUrl = productLine[productLine.rfind(" ") + 1 : ]
    parsedUrl = urlparse(productUrl)
    productCompany = "NULL"
    for domain in companyDict:
        if domain in parsedUrl.hostname:
            productCompany = companyDict[domain]
    
    parsedProductPrice = float(productPrice)

    scientificPriceDecimal = "NULL"
    scientificPriceUnit = "NULL"
    scientificPriceUnitAmount = "NULL"
    if (scientificPrice != "None"):
        scientificPrice = scientificPrice.strip('()')
        scientificPrice = scientificPrice.split(',')
        parsedSciPriceDecimal = float(scientificPrice[0].strip())
        if (parsedSciPriceDecimal > 0):
            scientificPriceDecimal = parsedSciPriceDecimal
            scientificPriceUnitAmount = float(scientificPrice[1].strip())
            scientificPriceUnit = scientificPrice[2].strip().strip("'")

    # Handle SQL properties, single quotes must be converted to two side by side quotes
    productName = productName.replace("'", "''")
    if productCompany != "NULL":
        productCompany = productCompany.replace("'", "''")

    # Embed quotes in string values that exist
    productName = f"'{productName}'"
    if productUrl != "NULL":
        productUrl = f"'{productUrl}'"
    if scientificPriceUnit != "NULL":
        scientificPriceUnit = f"'{scientificPriceUnit}'"
    if productCompany != "NULL":
        productCompany = f"'{productCompany}'"
    if productImageUrl != "NULL":
        productImageUrl = f"'{productImageUrl}'"
    
    result = f"INSERT INTO products (name, price, scientific_price, sci_unit_amount, sci_unit, company, url, image) VALUES({productName}, {parsedProductPrice}, {scientificPriceDecimal}, {scientificPriceUnitAmount}, {scientificPriceUnit}, {productCompany}, {productUrl},{productImageUrl})"
    return result
        
# Connect to database
parsed_database_url = parse_dsn(database_url)

conn = psycopg2.connect(database = parsed_database_url["dbname"], 
                        user = database_username, 
                        host= parsed_database_url["host"],
                        password = database_password,
                        port = parsed_database_url["port"])
cur = conn.cursor()

# Loop results
priceResultsFile = open(PRICE_RESULTS_FILE, "r")
resultsList = priceResultsFile.read().splitlines()
priceResultsFile.close()

numAdded = 0
for i in range(0, len(resultsList), 5):
    cmd = parseResult(resultsList[i], resultsList[i + 1], resultsList[i + 2], resultsList[i + 3])
    cur.execute(cmd)
    numAdded += 1

conn.commit()
cur.close()
conn.close()

print(str(numAdded) + " products succesfully added")

