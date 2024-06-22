import subprocess
import os
import signal
from bs4 import BeautifulSoup
import requests

torexe = subprocess.Popen(["/Applications/Tor Browser.app/Contents/MacOS/Tor/tor"])

session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

page = session.get("http://check.torproject.org")

soup = BeautifulSoup(page.text, features="html.parser")
# soup = BeautifulSoup(page.text, "html")

f = open("site.html", "w")
f.write(str(soup))
f.close()

# os.killpg(os.getpgid(torexe.pid), signal.SIGTERM)

# print(torexe.stdout)
# print(torexe.stderr)