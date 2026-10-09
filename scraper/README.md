# Polite Scraper — Books to Scrape Pipeline

A production-style, deterministic web scraping pipeline built in Python with Requests, BeautifulSoup4, and Pydantic. Implements target classification, local disk caching, polite request delays, schema validation, failure survival, and automated run reporting.

## Target Classification & Scope

- **Target Site**: [Books to Scrape](https://books.toscrape.com)
- **Target Purpose**: A public practice sandbox explicitly created for testing and practicing web scraping.
- **Crawl Scope**: First 3 catalogue pages (`index.html`, `page-2.html`, `page-3.html`), discovering 60 book detail pages.
- **Robots.txt Check**: Requested `https://books.toscrape.com/robots.txt` — returned HTTP `404 Not Found` ("no robots file found").
- **Classification Statement**: "I will not reuse this code on another site without checking its rules and terms first."

## Pipeline Architecture

```
[Target Catalogue Pages (1-3)] ──► Fetch & Discover ──► [60 Unique Book Detail URLs]
                                                               │
                                                       Fetch & Parse Detail
                                                               │
                                                  Normalize & Validate (Pydantic)
                                                               │
                                                   ┌───────────┴───────────┐
                                              Valid Records          Errors
                                                   │                       │
                                           output/books.json     output/errors.json
                                                   └───────────┬───────────┘
                                                       Run Summary
                                                           │
                                                  output/run-report.json
```

## Politeness & Reliability Rules

1. **User-Agent Identification**: Every request includes an identifying user agent string: `FlyRankInternshipA9/1.0 (+https://github.com/your-username/task-api)`.
2. **Local Caching**: Fetched HTML pages are cached locally under `scraper/cache/` to eliminate redundant network traffic during development and reruns.
3. **Request Delays**: Enforces a minimum 500 ms (0.5s) pause between live network calls. Cached calls bypass network delay.
4. **Timeouts & Retries**: Requests time out after 10 seconds. On timeouts or HTTP 5xx errors, the fetcher retries once. Non-recoverable errors (403, 404) are not retried.
5. **Idempotency**: Canonical product URLs serve as primary keys. Running the pipeline multiple times yields the exact same 60 records without duplication.
6. **Fault Isolation**: Single page failures or malformed HTML records are logged to `output/errors.json` without halting execution.

## Installation & Execution

### Setup
```bash
pip install -r requirements.txt
```

### Run Scraper Pipeline
```bash
python -m scraper.src.main
```

### Run with Failure Simulation (Stage 5 Checkpoint)
Injects one broken/404 book URL to verify pipeline fault tolerance:
```bash
python -m scraper.src.main --test-failure
```

### Run Unit Tests
```bash
python -m pytest scraper/tests/
```

## Record Schema

Each book in `output/books.json` conforms to the following Pydantic schema:

```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "price_gbp": 51.77,
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "description": "It's hard to imagine a world without A Light in the Attic...",
  "source_page": "https://books.toscrape.com/index.html",
  "fetched_at": "2026-10-09T13:40:21Z"
}
```

## Sample Run Report (`output/run-report.json`)

```json
{
  "start_time": "2026-10-09T13:40:21Z",
  "end_time": "2026-10-09T13:40:22Z",
  "duration_seconds": 0.42,
  "catalogue_pages_fetched": 3,
  "detail_pages_fetched": 60,
  "cache_hits": 63,
  "cache_misses": 0,
  "discovered_urls": 60,
  "unique_urls": 60,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
```

## Browser vs Plain HTTP Justification

This assignment required no headless browser (e.g. Playwright or Selenium) because the data is already present in the raw HTML response sent by the server. Using a full browser engine would add significant memory footprint, startup overhead, and CPU load without any benefit over standard HTTP requests and BeautifulSoup HTML parsing.

## Ethics Note

Web scraping should always be conducted responsibly and ethically. Always check for an official API before resorting to scraping. Respect site terms of service, robots.txt, and rate limits. Never attempt to bypass authentication gates, paywalls, or rate-limiting controls, and collect only data that is strictly necessary for your application.
