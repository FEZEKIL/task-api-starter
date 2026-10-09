from urllib.parse import urljoin
from typing import List, Tuple, Optional
from bs4 import BeautifulSoup

from scraper.src.models import RawBookRecord


def parse_catalogue_page(html: str, page_url: str) -> Tuple[List[str], Optional[str]]:
    """
    Parses a catalogue page HTML.
    Returns:
      - list of absolute product URLs
      - absolute URL of next catalogue page (or None if no next page)
    """
    soup = BeautifulSoup(html, "html.parser")
    product_urls = []

    # Find all product links in article.product_pod
    for article in soup.select("article.product_pod"):
        a_tag = article.select_one("h3 a")
        if a_tag and a_tag.get("href"):
            raw_href = a_tag["href"]
            abs_url = urljoin(page_url, raw_href)
            product_urls.append(abs_url)

    # Find next catalogue page link
    next_tag = soup.select_one("li.next a")
    next_page_url = None
    if next_tag and next_tag.get("href"):
        next_page_url = urljoin(page_url, next_tag["href"])

    return product_urls, next_page_url


def parse_book_page(html: str, book_url: str, source_page: str, fetched_at: str) -> RawBookRecord:
    """
    Parses a book detail page HTML.
    Target selectors specifically at product area (.product_main, #product_description).
    Returns RawBookRecord.
    """
    soup = BeautifulSoup(html, "html.parser")
    product_main = soup.select_one(".product_main")

    if not product_main:
        raise ValueError(f"Could not find .product_main on page: {book_url}")

    # Title
    title_el = product_main.select_one("h1")
    title = title_el.get_text(strip=True) if title_el else ""

    # Price text
    price_el = product_main.select_one("p.price_color")
    price_text = price_el.get_text(strip=True) if price_el else ""

    # Availability text
    avail_el = product_main.select_one("p.instock.availability")
    availability_text = " ".join(avail_el.get_text().split()) if avail_el else ""

    # Rating text (e.g. "star-rating Three" -> "Three")
    rating_el = product_main.select_one("p.star-rating")
    rating_text = ""
    if rating_el:
        classes = rating_el.get("class", [])
        rating_classes = [c for c in classes if c != "star-rating"]
        if rating_classes:
            rating_text = rating_classes[0]

    # Description (from #product_description + p)
    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    return RawBookRecord(
        title=title,
        product_url=book_url,
        price_text=price_text,
        availability_text=availability_text,
        rating_text=rating_text,
        description=description,
        source_page=source_page,
        fetched_at=fetched_at,
    )
