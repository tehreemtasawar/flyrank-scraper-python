import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
from pydantic import BaseModel, ValidationError

class BookRecord(BaseModel):
    title: str
    product_url: str
    price_gbp: float
    price_text: str
    availability_text: str
    rating_text: str | None
    description: str | None
    source_page: str
    fetched_at: str

def normalize_record(raw):
    price_clean = raw["price_text"].replace("£", "").replace("Â", "").strip()
    price_gbp = float(price_clean)
    return {
        "title": raw["title"],
        "product_url": raw["product_url"],
        "price_gbp": price_gbp,
        "price_text": raw["price_text"],
        "availability_text": raw["availability_text"],
        "rating_text": raw["rating_text"],
        "description": raw["description"],
        "source_page": raw["source_page"],
        "fetched_at": raw["fetched_at"]
    }

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/tehreemtasawar/flyrank-scraper-python)"
def fetch_page(url, cache_path):
    if os.path.exists(cache_path):
        print(f"CACHE HIT: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    print(f"FETCH: {url}")
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"

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

from datetime import datetime, timezone
import re

def extract_book_details(html, book_url, source_page):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1").get_text(strip=True)

    price_text = soup.find("p", class_="price_color").get_text(strip=True)

    availability_text = soup.find("p", class_="instock availability").get_text(strip=True)

    rating_tag = soup.find("p", class_=re.compile("star-rating"))
    rating_text = rating_tag["class"][1] if rating_tag else None

    description_tag = soup.find("div", id="product_description")
    if description_tag:
        description = description_tag.find_next_sibling("p").get_text(strip=True)
    else:
        description = None

    return {
        "title": title,
        "product_url": book_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

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

    records = []
    for i, book_url in enumerate(unique_links):
            valid_records = []
    invalid_records = []
    seen_urls = set()

    for raw in records:
        if raw["product_url"] in seen_urls:
            continue
        seen_urls.add(raw["product_url"])
        try:
            normalized = normalize_record(raw)
            validated = BookRecord(**normalized)
            valid_records.append(validated.model_dump())
        except (ValidationError, ValueError) as e:
            invalid_records.append({"record": raw, "reason": str(e)})

    with open("output/books.json", "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2, ensure_ascii=False)

    with open("output/errors.json", "w", encoding="utf-8") as f:
        json.dump(invalid_records, f, indent=2, ensure_ascii=False)

    print(f"valid_records={len(valid_records)}")
    print(f"invalid_records={len(invalid_records)}")