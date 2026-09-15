# The Polite Scraper

A small, polite web scraper that collects book data from [Books to Scrape](https://books.toscrape.com/), a public sandbox site built specifically for scraping practice.

## Target Classification

- **Site:** https://books.toscrape.com/
- **Why this site is appropriate to scrape:** The site explicitly states "We love being scraped!" and displays a banner confirming it is a demo website built for web scraping practice. Prices and ratings are randomly assigned and have no real meaning.
- **Scope:** Only the first 3 catalogue pages (60 books total) are collected.
- **robots.txt result:** Requested `https://books.toscrape.com/robots.txt` — returned a 404, no robots file found. A missing file is not permission on its own; permission here comes from the site's own explicit invitation to scrape it.
- **Data collected:** Title, price, availability, star rating, and description for each book.

I will not reuse this code on another site without checking its rules and terms first.