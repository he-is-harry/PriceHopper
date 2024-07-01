import random
from multiprocessing import Pool
import requests
import subprocess

torexe = subprocess.Popen(["/Applications/Tor Browser.app/Contents/MacOS/Tor/tor"])

session = requests.session()
creds = str(random.randint(10000,0x7fffffff)) + ":" + "foobar"
print(creds)
session.proxies = {'http': 'socks5h://{}@localhost:9050'.format(creds), 'https': 'socks5h://{}@localhost:9050'.format(creds)}
r = session.get('http://httpbin.org/ip')
print(r.text)

creds = str(random.randint(10000,0x7fffffff)) + ":" + "foobar"
print(creds)
session.proxies = {'http': 'socks5h://{}@localhost:9050'.format(creds), 'https': 'socks5h://{}@localhost:9050'.format(creds)}
r = session.get('http://httpbin.org/ip')
print(r.text)

torexe.terminate()