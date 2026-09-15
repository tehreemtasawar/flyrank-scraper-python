import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

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

def extract_book_links(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for article in soup.find_all("article", class_="product_pod"):
        a_tag = article.find("h3").find("a")
        relative_url = a_tag["href"]
        absolute_url = urljoin(page_url, relative_url)
        links.append(absolute_url)

    next_link = soup.find("li", class_="next")
    next_url = None
    if next_link:
        next_url = urljoin(page_url, next_link.find("a")["href"])

    return links, next_url

if __name__ == "__main__":
    all_links = []
    url = "https://books.toscrape.com/catalogue/page-1.html"
    page_num = 1

    while url and page_num <= 3:
        cache_path = f"cache/catalogue-page-{page_num}.html"
        html = fetch_page(url, cache_path)
        links, next_url = extract_book_links(html, url)
        all_links.extend(links)
        url = next_url
        page_num += 1
        time.sleep(0.5)

    unique_links = list(set(all_links))
    print(f"catalogue_pages={page_num - 1}")
    print(f"discovered={len(all_links)}")
    print(f"unique_urls={len(unique_links)}")