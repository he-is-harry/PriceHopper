import os
import sys
import psycopg2
from psycopg2.extensions import parse_dsn

# Configuration
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
PRODUCT_CATEGORIES_FILE = "Files/product_categories.txt"

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

# Normalize a category by capitalizing all of its words
def normalizeCategory(categoryStr):
    catWords = categoryStr.split()
    result = []
    for word in catWords:
        result.append(word[0].upper() + word[1 : ])
    return " ".join(result)

def parseCategoryLine(line):
    arrowIndex = line.find("->")

    # Parse search words
    searchWordsStr = line[ : arrowIndex].strip()
    searchWordsStr = searchWordsStr.replace("|", "")
    searchWords = " ".join(searchWordsStr.split())

    # Parse categories
    lineCategoriesStr = line[ arrowIndex + 2 : ].strip()
    lineCategoriesArr = lineCategoriesStr.split(",")
    categories = []
    for category in lineCategoriesArr:
        categories.append(normalizeCategory(category.strip()))
    
    return (searchWords, categories)


# Load product categories
categoriesDict = {}
with open(PRODUCT_CATEGORIES_FILE, "r") as categoriesFile:
    categoryLines = categoriesFile.read().splitlines()
    for line in categoryLines:
        parsedLine = parseCategoryLine(line)
        categoriesDict[parsedLine[0]] = parsedLine[1]

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
forProducts = 0
for i in range(0, len(resultsList), 5):
    line = resultsList[i].strip()
    imageDelimIndex = line.find("| Image:")
    if imageDelimIndex >= 0:
        line = line[ : imageDelimIndex].strip()
    lastSpace = line.rfind(" ")
    productWords = line[ : lastSpace]
    if productWords in categoriesDict:
        productCategories = categoriesDict[productWords]

        for category in productCategories:
            # Handle SQL properties
            # Ensure single quotes are changed to two side by side quotes
            category = category.replace("'", "''")

            # Check if category exists, and if so get its index
            cur.execute(f"SELECT category_id FROM categories WHERE category_name = '{category}'")
            categoryId = cur.fetchone()
            if categoryId is None:
                cur.execute(f"INSERT INTO categories (category_name) VALUES ('{category}')")
                cur.execute(f"SELECT category_id FROM categories WHERE category_name = '{category}'")
                categoryId = cur.fetchone()[0]
            else:
                categoryId = categoryId[0]
            
            # Get the product index
            productUrl = line[lastSpace + 1 : ]
            cur.execute(f"SELECT product_id FROM products WHERE url = '{productUrl}'")
            productId = cur.fetchone()[0]

            # Add the product category
            cur.execute(f"INSERT INTO product_categories (category_id, product_id) VALUES ({categoryId}, {productId})")
            numAdded += 1
    forProducts += 1

conn.commit()

print(str(numAdded) + " categories added for " + str(forProducts) + " products")



