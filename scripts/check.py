# This code tests HTTP proxies running on localhost ports 25000 to 25009.
import requests

def check_proxies():
    proxy = "http://127.0.0.1:8080"

    for _ in range(5):
        r = requests.get(
            "http://httpbin.org/ip",
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        print(r.text)

if __name__ == "__main__":
    check_proxies()