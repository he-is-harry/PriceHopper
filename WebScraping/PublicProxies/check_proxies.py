import threading
import queue

import requests

q = queue.Queue()
valid_proxies = []

with open("proxy_list.txt", "r") as f:
    proxies = f.read().split("\n")
    counter = 0
    for p in proxies:
        if counter >= 10:
            break
        q.put(p)
        counter += 1

def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            session = requests.session()
            session.proxies = {}

            session.proxies['http'] = proxy
            session.proxies['https'] = proxy

            r = session.get("http://httpbin.org/ip", timeout=3)
            index = proxy.rfind(":")
            if(index > 0):
                proxyIP = proxy[0:index]
                if ("\"origin\": \"" + proxyIP + "\"") in (r.text):
                    print("IP:" + r.text)
        except:
            continue

for _ in range(10):
    threading.Thread(target=check_proxies).start()