from bs4 import BeautifulSoup
import requests

url = "https://www.walmart.ca/en/ip/apple-gala/6000195494285"
PROXY = "67.43.227.228:2369"

# f = open("WalmartCookie.txt", "r")
# cookie_text = f.read()
# f.close()
# print(cookie_text)

session = requests.session()
session.proxies = {}

session.proxies['http'] = PROXY
session.proxies['https'] = PROXY

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97",
    # "Cookie": cookie_text,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd"}

print("Requested page")
page = session.get(url, headers=headers, timeout=15)
# page = requests.get(url)



soup = BeautifulSoup(page.text, features="html.parser")
# soup = BeautifulSoup(page.text, "html")

f = open("site.html", "w")
f.write(str(soup.encode("utf-8")))
f.close()

# print(soup)
