from urllib.parse import urlparse

PARSE_LIST_FILE = "Files/ParseList.txt"
COMPANIES_FILE = "Files/companies.txt"
FILTERED_RESULTS_FILE = "Files/FilteredParseList.txt"

parseListFile = open(PARSE_LIST_FILE, "r")
parseList = parseListFile.read().splitlines()
parseListFile.close()

companiesFile = open(COMPANIES_FILE, "r")
companiesList = companiesFile.read().splitlines()
companiesFile.close()

# Make the company names more friendly for urls
companiesList[companiesList.index("no frills")] = "nofrills"
companiesList[companiesList.index("whole foods")] = "wholefoods"

filteredFile = open(FILTERED_RESULTS_FILE, "w")

url_set = {}

for productLine in parseList:
    lastSpaceIndex = productLine.rfind(" ")
    if lastSpaceIndex >= 0:
        url = productLine[lastSpaceIndex + 1 : ]
        urlParseRes = urlparse(url)
        foundCompany = False
        urlCompany = ""
        for company in companiesList:
            if company in urlParseRes.hostname:
                foundCompany = True
                urlCompany = company
                break
        valid = True
        # Remove duplicate pages from the parseList
        if url in url_set:
            valid = False
        # Add a rule to ignore browse pages on walmart, since those are
        # not product pages
        if "browse/" in url.lower() and urlCompany.lower() == "walmart":
            valid = False
        
        if foundCompany and valid:
            filteredFile.write(productLine + "\n")
            url_set[url] = True

filteredFile.close()
            



