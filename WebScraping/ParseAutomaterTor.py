import queue
import threading
import traceback
from Source.Parsing.Parser import parseSite

# Before running the code in this file, ensure that Tor is running on your computer
# at port 9050

PARSE_LIST_FILE = "Files/ParseList.txt"
PRICE_RESULTS_FILE = "Files/PriceResults.txt"
REPARSE_LIST_FILE = "Files/ReparseList.txt"
FINISHED_LIST_FILE = "Files/FinishedParsingList.txt"

BATCH_SIZE = 50
THREADS = 7

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
        lastSpaceIndex = parse_line.rfind(" ")
        if lastSpaceIndex >= 0:
            product = parse_line[0 : lastSpaceIndex]
            url = parse_line[lastSpaceIndex + 1 : ]

            with thread_lock:
                proxy = proxyList[cur_proxy_index]
                cur_proxy_index = (cur_proxy_index + 1) % len(proxyList)
            try:
                tupleAns = parseSite(url, product, proxy)
                if tupleAns[0] is None or tupleAns[1] is None:
                    # We have to reparse these results
                    print("Could not retrieve, set to reparse: " + parse_line)
                    with thread_lock:
                        with open(REPARSE_LIST_FILE, "a") as reparseFile:
                            reparseFile.write(parse_line + "\n")
                else:
                    # Output the resulting result and indicate that it was parsed
                    with thread_lock:
                        with open(PRICE_RESULTS_FILE, "a") as priceResFile:
                            print(parse_line)
                            print(tupleAns[0])
                            print(tupleAns[1])
                            print(str(tupleAns[2]) + "\n")
                            priceResFile.write(parse_line + "\n")
                            priceResFile.write(str(tupleAns[0]) + "\n")
                            priceResFile.write(str(tupleAns[1]) + "\n")
                            priceResFile.write(str(tupleAns[2]) + "\n\n")
                        with open(FINISHED_LIST_FILE, "a") as finishedFile:
                            finishedFile.write(parse_line + "\n")
            except Exception:
                print(traceback.format_exc())
                print("Could not retrieve, set to reparse: " + parse_line)
                with thread_lock:
                    with open(REPARSE_LIST_FILE, "a") as reparseFile:
                        reparseFile.write(parse_line + "\n")

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
        
        proxyList = ["socks5h://localhost:9050"]
        
        if q.qsize() > 0:
            threads = []
            for _ in range(THREADS):
                threads.append(threading.Thread(target=parse_product, daemon=True))
            for t in threads:
                t.start()
            products_batch_left = True
            # while products_batch_left:
            #     if keyboard.is_pressed('q'):
            #         print("Q Pressed - Quitting Program")
            #         sys.exit(1)
            # Wait for all threads to finish
            for t in threads:
                t.join()
        
        curParsedTotal += BATCH_SIZE
