import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from scraper.src.fetcher import PoliteFetcher
from scraper.src.parser import parse_catalogue_page, parse_book_page
from scraper.src.models import RawBookRecord, BookRecord, RunReport
from scraper.src.utils import extract_price_gbp, get_utc_iso_timestamp


class ScraperPipeline:
    def __init__(
        self,
        start_url: str = "https://books.toscrape.com/index.html",
        max_catalogue_pages: int = 3,
        output_dir: str = "scraper/output",
        cache_dir: str = "scraper/cache",
        user_agent: Optional[str] = None,
    ):
        self.start_url = start_url
        self.max_catalogue_pages = max_catalogue_pages
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        fetcher_kwargs = {"cache_dir": cache_dir}
        if user_agent:
            fetcher_kwargs["user_agent"] = user_agent
        self.fetcher = PoliteFetcher(**fetcher_kwargs)

    def run(self, extra_urls: Optional[List[str]] = None) -> RunReport:
        start_time_iso = get_utc_iso_timestamp()
        start_ticks = time.time()

        print("=== Starting Polite Scraper Run ===")
        # Stage 2: Discover catalogue pages
        catalogue_url = self.start_url
        catalogue_count = 0
        discovered_urls: List[str] = []
        url_source_map: Dict[str, str] = {}  # book_url -> source_catalogue_url

        while catalogue_url and catalogue_count < self.max_catalogue_pages:
            try:
                html, _ = self.fetcher.fetch(catalogue_url)
                catalogue_count += 1
                book_urls, next_url = parse_catalogue_page(html, catalogue_url)

                for b_url in book_urls:
                    discovered_urls.append(b_url)
                    if b_url not in url_source_map:
                        url_source_map[b_url] = catalogue_url

                catalogue_url = next_url
            except Exception as e:
                print(f"[ERROR] Failed fetching catalogue page {catalogue_url}: {e}")
                break

        # Remove duplicate book URLs while preserving order
        unique_urls = list(dict.fromkeys(discovered_urls))
        print(f"[DISCOVERY SUMMARY] catalogue_pages={catalogue_count}, discovered={len(discovered_urls)}, unique_urls={len(unique_urls)}")

        # Include any extra URLs provided for testing failures (e.g., Stage 5 checkpoint)
        urls_to_process = list(unique_urls)
        if extra_urls:
            for extra in extra_urls:
                if extra not in urls_to_process:
                    urls_to_process.append(extra)
                    url_source_map[extra] = "http://test.invalid/source"

        # Stage 3 & 4: Extract, Normalize, Validate, Store
        valid_records: List[Dict[str, Any]] = []
        error_records: List[Dict[str, Any]] = []
        seen_canonical_urls = set()
        failed_pages = 0
        invalid_records_count = 0
        detail_pages_fetched = 0

        for book_url in urls_to_process:
            fetched_at = get_utc_iso_timestamp()
            source_page = url_source_map.get(book_url, self.start_url)

            try:
                html, _ = self.fetcher.fetch(book_url)
                detail_pages_fetched += 1

                # Parse raw record
                raw_record = parse_book_page(html, book_url, source_page, fetched_at)

                # Normalize price
                price_gbp = extract_price_gbp(raw_record.price_text)

                # Validate with Pydantic model
                validated_model = BookRecord(
                    title=raw_record.title,
                    product_url=raw_record.product_url,
                    price_text=raw_record.price_text,
                    price_gbp=price_gbp,
                    availability_text=raw_record.availability_text,
                    rating_text=raw_record.rating_text,
                    description=raw_record.description,
                    source_page=raw_record.source_page,
                    fetched_at=raw_record.fetched_at,
                )

                rec_dict = validated_model.model_dump()

                # Idempotency / deduplication check
                if validated_model.product_url not in seen_canonical_urls:
                    seen_canonical_urls.add(validated_model.product_url)
                    valid_records.append(rec_dict)

            except Exception as err:
                print(f"[PAGE FAILURE] Skipped failed page/record for {book_url}: {err}")
                failed_pages += 1
                error_records.append({
                    "product_url": book_url,
                    "error": str(err),
                    "failed_at": fetched_at
                })

        # Save to output files
        books_json_path = self.output_dir / "books.json"
        errors_json_path = self.output_dir / "errors.json"
        report_json_path = self.output_dir / "run-report.json"

        books_json_path.write_text(json.dumps(valid_records, indent=2), encoding="utf-8")
        errors_json_path.write_text(json.dumps(error_records, indent=2), encoding="utf-8")

        end_time_iso = get_utc_iso_timestamp()
        duration = round(time.time() - start_ticks, 2)

        report = RunReport(
            start_time=start_time_iso,
            end_time=end_time_iso,
            duration_seconds=duration,
            catalogue_pages_fetched=catalogue_count,
            detail_pages_fetched=detail_pages_fetched,
            cache_hits=self.fetcher.cache_hits,
            cache_misses=self.fetcher.cache_misses,
            discovered_urls=len(discovered_urls),
            unique_urls=len(unique_urls),
            valid_records=len(valid_records),
            invalid_records=invalid_records_count,
            failed_pages=failed_pages,
        )

        report_json_path.write_text(json.dumps(report.model_dump(), indent=2), encoding="utf-8")

        print("\n=== Scraper Run Completed ===")
        print(f"Valid records stored: {len(valid_records)} in {books_json_path}")
        print(f"Run report written to {report_json_path}")
        print(f"Failed pages: {failed_pages}")

        return report
