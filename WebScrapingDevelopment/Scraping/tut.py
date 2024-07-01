from bs4 import BeautifulSoup
import requests

url = "https://www.enable-javascript.com/"

# f = open("WalmartCookie.txt", "r")
# cookie_text = f.read()
# f.close()
# print(cookie_text)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/123.0.2420.97",
    # "Cookie": cookie_text,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate, br, zstd"}
page = requests.get(url, headers=headers)
# page = requests.get(url)


print("Requested page")

soup = BeautifulSoup(page.text, features="html.parser")
# soup = BeautifulSoup(page.text, "html")
print(soup.text)

f = open("app4.html", "w")
f.write(str(soup))
f.close()

# print(soup)
