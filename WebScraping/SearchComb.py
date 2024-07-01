from Source.HarryGoogleSearch.googlesearch import search

COMPANIES_FILE_PATH = "Files/companies.txt"
PRODUCTS_FILE_PATH = "Files/product_types.txt"
SEARCH_RESULTS_FILE_PATH = "Files/ParseList.txt"

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

NUM_RESULTS = 10
PAUSE = 15

# Clear the search results file
# searchResultsFile = open(SEARCH_RESULTS_FILE_PATH, "w")
# searchResultsFile.close()

for i in range(0, len(wishlist), 2):
    searchComb = wishlist[i]
    product = wishlist[i + 1]
    print("Searching: " + searchComb)
    # Save results between each search combination
    with open(SEARCH_RESULTS_FILE_PATH, "a") as searchResultsFile:
        for url in search(searchComb, tld="ca", num=NUM_RESULTS, stop=NUM_RESULTS, pause=PAUSE):
            searchResultsFile.write(product + " " + url + "\n")
            print(product + " " + url)

