from googlesearch import search

NUM_RESULTS = 10
PAUSE = 15

searchResultsFile = open("search_results.txt", "w")
productCombFile = open("wishlist.txt", "r")
wishlist = productCombFile.read().splitlines()

for i in range(0, len(wishlist), 2):
    searchComb = wishlist[i]
    product = wishlist[i + 1]
    print("Searching: " + searchComb)
    # searchResultsFile.write(searchComb)
    for url in search(searchComb, tld="ca", num=NUM_RESULTS, stop=NUM_RESULTS, pause=PAUSE):
        searchResultsFile.write(product + " " + url + "\n")

searchResultsFile.close()