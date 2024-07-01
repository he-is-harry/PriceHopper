import json
from bs4 import BeautifulSoup
import requests

url = "https://www.walmart.ca/en/search?q=avocados"

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"}
page = requests.get(url, headers=headers)
# page = requests.get(url)

soup = BeautifulSoup(page.text, features="html.parser")
# soup = BeautifulSoup(page.text, "html")

next_data = soup.find('script', {'id': '__NEXT_DATA__'})
parsed_json = json.loads(next_data.text)

# Declare product variables
product_name: str
product_price_cur: str
product_price_unit: str

try:
    product_name: str = parsed_json['props']['pageProps']['initialData']['data']['product']['name']
except (TypeError, KeyError):
    product_name = None

try:
    product_price_cur: str = parsed_json['props']['pageProps']['initialData']['data']['product']['priceInfo']['currentPrice']['priceString']
except (TypeError, KeyError):
    product_price_cur = None

try:
    product_price_unit: str = parsed_json['props']['pageProps']['initialData']['data']['product']['priceInfo']['unitPrice']['priceString']
except (TypeError, KeyError):
    product_price_unit = None


print(product_name)
print(product_price_cur)
print(product_price_unit)

# product_name_text = BeautifulSoup(product_name).text
# product_price_cur_text = BeautifulSoup(product_price_cur).text
# product_price_unit_text = BeautifulSoup(product_price_unit).text

# print(product_name_text)
# print(product_price_cur_text)
# print(product_price_unit_text)



# bodyText = soup.get_text("\n")

# f = open("beautifulText.txt", "w")

# f.write(bodyText)
# f.close()
