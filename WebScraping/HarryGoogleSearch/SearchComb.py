from googlesearch import search

NUM_RESULTS = 10
PAUSE = 15

searchResultsFile = open("search_results.txt", "w")
productCombFile = open("wishlist.txt", "r")
wishlist = productCombFile.read().splitlines()

for searchComb in wishlist:
    print("Searching: " + searchComb)
    searchResultsFile.write(searchComb)
    for url in search(searchComb, tld="ca", num=NUM_RESULTS, stop=NUM_RESULTS, pause=PAUSE):
        searchResultsFile.write(url + "\n")

searchResultsFile.close()