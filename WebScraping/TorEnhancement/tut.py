import requests

import subprocess

# Hard coded path to the Tor executable file
# torexe = subprocess.run(["/Applications/Tor Browser.app/Contents/MacOS/Tor/tor"], capture_output=True)
# torexe = os.popen("/Applications/Tor Browser.app/Contents/MacOS/Tor", mode="r")

session = requests.session()
session.proxies = {}

session.proxies['http'] = 'socks5h://localhost:9050'
session.proxies['https'] = 'socks5h://localhost:9050'

r = session.get("http://httpbin.org/ip")
print(r.text)