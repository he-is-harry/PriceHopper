from bs4 import BeautifulSoup
import requests
import urllib3
from ProxyGrabber import get_public_proxies
import random

proxyList = get_public_proxies()
# for proxy in proxyList:
#     print(proxy)
#     try:
#         session = requests.session()
#         session.proxies = {}

#         session.proxies['http'] = proxy
#         session.proxies['https'] = proxy

#         r = session.get("http://httpbin.org/ip", timeout=3)
#         index = proxy.rfind(":")
#         if(index > 0):
#             proxyIP = proxy[0:index]
#             if ("\"origin\": \"" + proxyIP + "\"") in (r.text):
#                 print("IP:" + r.text)
#     except (requests.exceptions.ProxyError, urllib3.exceptions.ProxyError, ConnectionResetError, requests.exceptions.Timeout):
#         continue

session = requests.session()
session.proxies = {}

session.proxies['http'] = proxyList[0]
session.proxies['https'] = proxyList[0]

url = "https://www.walmart.ca/en/ip/banana/875806"

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
page = session.get(url, headers=headers)
# page = requests.get(url)

print("Requested page")

soup = BeautifulSoup(page.text, features="html.parser")
# soup = BeautifulSoup(page.text, "html")

f = open("site.html", "w")
f.write(str(soup))
f.close()
        
