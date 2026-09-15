import requests
import os

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/tehreemtasawar/flyrank-scraper-python)"
def fetch_page(url, cache_path):
    if os.path.exists(cache_path):
        print(f"CACHE HIT: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    print(f"FETCH: {url}")
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=10)

    print(f"Status: {response.status_code}, Size: {len(response.text)} bytes")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}: status {response.status_code}")

    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return response.text

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/page-1.html"
    cache_path = "cache/catalogue-page-1.html"
    html = fetch_page(url, cache_path)
    print(f"Fetched {len(html)} characters")