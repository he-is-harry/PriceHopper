import os
import sys
import psycopg2
from psycopg2.extensions import parse_dsn

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

# Connect to database
parsed_database_url = parse_dsn(database_url)

conn = psycopg2.connect(database = parsed_database_url["dbname"], 
                        user = database_username, 
                        host= parsed_database_url["host"],
                        password = database_password,
                        port = parsed_database_url["port"])
cur = conn.cursor()

# Get categories with no image
cur.execute(f"SELECT category_id FROM categories WHERE category_image IS NULL")
categoryIdList = cur.fetchall()

# Loop through categories and add the category's first product's image as the
# category image
numAdded = 0
for categoryTuple in categoryIdList: # Tuple is of form [<category id>]
    # Get first image
    cur.execute(f"SELECT product_id FROM product_categories WHERE category_id = {categoryTuple[0]}")
    productId = cur.fetchone()[0]
    cur.execute(f"SELECT image FROM products WHERE product_id = {productId}")
    firstImage = cur.fetchone()[0]

    # Set category image
    cur.execute(f"UPDATE categories SET category_image = '{firstImage}' WHERE category_id = {categoryTuple[0]}")
    numAdded += 1

conn.commit()

print(str(numAdded) + " category images added")


