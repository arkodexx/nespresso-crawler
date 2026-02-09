# ☕⚡ Nespresso Product Crawler

A **fast, lightweight crawler for Nespresso.com** built with **pure Scrapy**, designed to extract structured product data at scale without browser automation.

Ideal for product analysis, pricing research, and catalog monitoring.

## 🔍 Highlights

- ⚡ **High-speed product crawling** with async concurrency
- 🧵 Efficient request scheduling optimized for catalog pages
- 🧱 **Fully populated product records** — no empty fields
- ♻️ **Duplicate-safe pipelines** for clean datasets
- 📦 Output formats: **CSV / JSON**

## 🧰 Tech Stack

- Python  
- Scrapy (no Selenium, no Playwright, minimal overhead)
- Scrapy-impersonate

## 📥 Installation & Usage

```bash
git clone https://github.com/arkodexx/nespresso-crawler.git
cd nespresso-crawler
pip install -r requirements.txt
scrapy crawl crawler -o data.json
or
scrapy crawl crawler -o data.csv
