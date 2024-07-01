from googlesearch import search
from ProxyGrabber import get_ip_proxy
import os, sys

proxyVal = get_ip_proxy("20.219.180.149:3129")
# print("Acquired public proxies: ", end="")
# print(proxyList)

# to search
query = "walmart avocado"
 
for j in search(query, tld="ca", num=10, stop=100, proxy=proxyVal, pause=2):
    print(j)
