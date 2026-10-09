import re
import hashlib
from datetime import datetime, timezone


def url_to_cache_filename(url: str) -> str:
    """Generates a safe, unique cache filename based on URL hash and path slug."""
    # Extract filename or path part for readability
    clean_url = url.split("?")[0].split("#")[0]
    parts = [p for p in clean_url.rstrip("/").split("/") if p]
    slug = parts[-1] if parts else "index"

    # Ensure safe filename
    slug = re.sub(r'[^\w\-_.]', '_', slug)
    if not slug.endswith(".html"):
        slug += ".html"

    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    return f"{url_hash}_{slug}"


def extract_price_gbp(price_text: str) -> float:
    """Converts price string like '£51.77' or 'Â£51.77' into a float 51.77."""
    if not price_text:
        raise ValueError("Empty price text")
    match = re.search(r"(\d+\.\d{2})", price_text)
    if match:
        return float(match.group(1))
    raise ValueError(f"Could not parse price float from '{price_text}'")


def get_utc_iso_timestamp() -> str:
    """Returns current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
