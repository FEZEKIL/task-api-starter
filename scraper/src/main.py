import sys
import argparse
from scraper.src.scraper import ScraperPipeline


def main():
    parser = argparse.ArgumentParser(description="Polite Scraper for Books to Scrape (FlyRank Internship A9)")
    parser.add_argument("--test-failure", action="store_true", help="Inject one broken URL to verify Stage 5 failure survival")
    parser.add_argument("--max-pages", type=int, default=3, help="Number of catalogue pages to crawl (default: 3)")
    args = parser.parse_args()

    pipeline = ScraperPipeline(max_catalogue_pages=args.max_pages)
    extra_urls = ["https://books.toscrape.com/catalogue/non_existent_book_999999/index.html"] if args.test_failure else None

    report = pipeline.run(extra_urls=extra_urls)
    sys.exit(0 if report.valid_records > 0 else 1)


if __name__ == "__main__":
    main()
