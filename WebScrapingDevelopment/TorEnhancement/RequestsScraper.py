import random
from bs4 import BeautifulSoup
import requests
import subprocess

url = "https://www.walmart.ca/en/ip/apple-gala/6000195494285"

torexe = subprocess.Popen(["/Applications/Tor Browser.app/Contents/MacOS/Tor/tor"])

session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

r = session.get("http://httpbin.org/ip")
print("IP: " + r.text)

agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-F700N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
]

headers = {
    "User-Agent": random.choice(agents),
    # "Cookie": cookie_text,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd",
    "Cookie": "walmart.nearestPostalCode=L3R4M9; walmart.shippingPostalCode=L3R4M9; defaultNearestStoreId=3053;"
}
# cookies = {
#     'walmart.nearestPostalCode': 'L3R4M9',
#     'walmart.shippingPostalCode': 'L3R4M9',
#     'defaultNearestStoreId': 3053,
# }
# cookie_lst = []
# cookie_lst.append(requests.cookies.create_cookie("walmart.nearestPostalCode", "L3R4M9"))
# cookie_lst.append(requests.cookies.create_cookie("walmart.shippingPostalCode", "L3R4M9"))
# cookie_lst.append(requests.cookies.create_cookie("defaultNearestStoreId", 3053))

# requests.utils.add_dict_to_cookiejar(session.cookies)

try:
    page = session.get(url, headers=headers, timeout=10)
    # page = requests.get(url)

    soup = BeautifulSoup(page.text, features="html.parser")
    # soup = BeautifulSoup(page.text, "html")

    f = open("site.html", "w")
    f.write(str(soup))
    f.close()
except (requests.exceptions.ReadTimeout):
    print("Request timed out")


torexe.terminate()

# print(soup)
