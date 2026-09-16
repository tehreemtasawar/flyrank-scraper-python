# The Polite Scraper

A small, polite web scraper that collects book data from [Books to Scrape](https://books.toscrape.com/), a public sandbox site built specifically for scraping practice.

## Target Classification

- **Site:** https://books.toscrape.com/
- **Why this site is appropriate to scrape:** The site explicitly states "We love being scraped!" and displays a banner confirming it is a demo website built for web scraping practice. Prices and ratings are randomly assigned and have no real meaning.
- **Scope:** Only the first 3 catalogue pages (60 books total) are collected.
- **robots.txt result:** Requested `https://books.toscrape.com/robots.txt`, returned a 404, no robots file found. A missing file is not permission on its own; permission here comes from the site's own explicit invitation to scrape it.
- **Data collected:** Title, price, availability, star rating, and description for each book.

I will not reuse this code on another site without checking its rules and terms first.

## How to Run

1. Install dependencies:

   pip install requests beautifulsoup4 pydantic

2. Run the scraper:

   python src/main.py

3. Output appears in `output/books.json`, `output/errors.json`, and `output/run-report.json`.

## Record Schema

Each validated record contains:

- `title` (string)
- `product_url` (string, canonical/absolute URL)
- `price_gbp` (number, cleaned from price_text)
- `price_text` (string, original raw text, e.g. "£31.12")
- `availability_text` (string)
- `rating_text` (string or null)
- `description` (string or null)
- `source_page` (string, which catalogue page this book was found on)
- `fetched_at` (string, ISO timestamp of when the page was fetched)

## Politeness Rules

- Every real request sends an honest User-Agent identifying this project.
- A 10-second timeout on every request, never waits forever.
- At least 0.5 seconds between real requests to the site.
- Only HTTP status 200 is treated as success; anything else is a failed fetch.
- All fetched pages are cached in `cache/`, so re-running during development never re-hits the live site unnecessarily.

## Surviving Failures

One deliberately broken URL (`fake-broken-book_9999`) is included in the run to prove the pipeline survives a bad page. The run finishes, the 60 good records are still saved, and the failure is recorded in the run report.

## Sample Run Report

    {
      "start_time": "2026-09-16T10:08:52.807466+00:00",
      "duration_seconds": 41.72,
      "pages_fetched": 61,
      "cache_hits": 60,
      "valid_records": 60,
      "invalid_records": 0,
      "failed_pages": 1
    }

## Why No Browser Was Needed

The book data (title, price, availability, description) is already present in the raw HTML the server sends, a plain HTTP request is enough to retrieve it. A full browser would only add cost (memory, startup time) without providing any extra data.

## Ethics Note

I used an official practice sandbox built for this exact purpose rather than a live production site. In general, I would prefer an official API when one exists, never bypass logins, paywalls, or explicit blocks, and only collect the data actually needed for the task.