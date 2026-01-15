# This code tests HTTP proxies running on localhost ports 25000 to 25009.
import requests
import pathlib, os, sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from config import ( TEST_URL, TIMEOUT, PROXY_PROTOCOL, PROXY_HOST, PROXY_START_PORT, PROXY_COUNT ) 
import pathlib
    
for port in range(PROXY_START_PORT, PROXY_START_PORT + PROXY_COUNT):
    proxy = f"http://{PROXY_HOST}:{port}"
    try:
        r = requests.get(
            "http://httpbin.org/ip",
            proxies={"http": proxy, "https": proxy},
            timeout=TIMEOUT
        )
        print(f"[Ok] {proxy} → {r.text}")
    except:
        print(f"[Bad] {proxy}")