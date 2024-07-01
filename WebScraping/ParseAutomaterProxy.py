import queue
import threading
import sys
import keyboard
from Source.Parsing.Parser import parseSite
from Source.PublicProxies.ProxyGrabber import get_public_proxies

PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
REPARSE_LIST_FILE = "Files/ReparseList.txt"
FINISHED_LIST_FILE = "Files/FinishedParsingList.txt"

BATCH_SIZE = 20
THREADS = 5

# Global threaded variables
q = queue.Queue()
thread_lock = threading.Lock()
cur_proxy_index = 0
proxyList = []
products_batch_left = False

def parse_product():
    global q
    global cur_proxy_index
    global proxyList
    global products_batch_left

    while not q.empty():
        parse_line = q.get()
        print("Parsing (" + str(q.qsize()) + "): " + parse_line)
        parse_line_array = parse_line.split(" ")
        with thread_lock:
            proxy = proxyList[cur_proxy_index]
            cur_proxy_index = (cur_proxy_index + 1) % len(proxyList)
        tupleAns = parseSite(parse_line_array[1], parse_line_array[0], proxy)
        if tupleAns[0] is None or tupleAns[1] is None:
            # We have to reparse these results
            print("Could not retrieve, set to reparse: " + parse_line)
            with thread_lock:
                with open(REPARSE_LIST_FILE, "a") as reparseFile:
                    reparseFile.write(parse_line)
        else:
            # Output the resulting result and indicate that it was parsed
            with thread_lock:
                with open(PRICE_RESULTS_FILE, "a") as priceResFile:
                    print(parse_line)
                    print(tupleAns[0])
                    print(tupleAns[1])
                    print(tupleAns[2] + "\n")
                    priceResFile.write(parse_line + "\n")
                    priceResFile.write(str(tupleAns[0]) + "\n")
                    priceResFile.write(str(tupleAns[1]) + "\n")
                    priceResFile.write(str(tupleAns[2]) + "\n\n")
                with open(FINISHED_LIST_FILE, "a") as finishedFile:
                    finishedFile.write(parse_line)
    products_batch_left = False

if __name__ == '__main__':
    parseListFile = open(PARSE_LIST_FILE, "r")
    parseList = parseListFile.read().splitlines()
    curParsedTotal = 0
    proxy_config = {
        "good_proxies_file_config": "Files/_good_proxies.txt",
        "bad_proxies_file_config": "Files/_bad_proxies.txt",
    }

    while curParsedTotal < len(parseList):
        q.queue.clear()
        for i in range(curParsedTotal, min(len(parseList), curParsedTotal + BATCH_SIZE)):
            q.put(parseList[i])
        
        proxyList = get_public_proxies(fast = True, configuration=proxy_config)
        while len(proxyList) == 0:
            print("Could not retrieve any proxies, retrying")
            proxyList = get_public_proxies(fast = True, configuration=proxy_config)
        
        if q.qsize() > 0:
            threads = []
            for _ in range(THREADS):
                threads.append(threading.Thread(target=parse_product, daemon=True))
            for t in threads:
                t.start()
            products_batch_left = True
            while products_batch_left:
                if keyboard.is_pressed('q'):
                    print("Q Pressed - Quitting Program")
                    sys.exit(1)
            # Wait for all threads to finish
            for t in threads:
                t.join()
        
        curParsedTotal += BATCH_SIZE