import time
from pathlib import Path
from typing import Tuple, Optional
import requests

from scraper.src.utils import url_to_cache_filename

DEFAULT_USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/your-username/task-api)"
DEFAULT_TIMEOUT = 10.0
DEFAULT_DELAY = 0.5  # 500ms delay between network requests


class PoliteFetcher:
    def __init__(
        self,
        cache_dir: str = "scraper/cache",
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: float = DEFAULT_TIMEOUT,
        delay: float = DEFAULT_DELAY,
    ):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent
        self.timeout = timeout
        self.delay = delay
        self.last_request_time: float = 0.0
        self.cache_hits = 0
        self.cache_misses = 0

    def fetch(self, url: str, force_refresh: bool = False) -> Tuple[str, bool]:
        """
        Fetches page content from cache or network.
        Returns tuple of (html_content, is_cache_hit).
        """
        cache_filename = url_to_cache_filename(url)
        cache_filepath = self.cache_dir / cache_filename

        if not force_refresh and cache_filepath.exists():
            html = cache_filepath.read_text(encoding="utf-8")
            self.cache_hits += 1
            print(f"[CACHE HIT] {url} ({len(html)} bytes)")
            return html, True

        # Politeness delay before network request
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        headers = {"User-Agent": self.user_agent}
        self.cache_misses += 1

        # Attempt fetch with 1 retry on timeout or 5xx
        response = self._request_with_retry(url, headers)
        self.last_request_time = time.time()

        if response.status_code != 200:
            raise requests.HTTPError(
                f"Failed to fetch {url}: HTTP status code {response.status_code}",
                response=response,
            )

        html = response.text
        # Save to cache
        cache_filepath.write_text(html, encoding="utf-8")
        print(f"[FETCH] {url} ({len(html)} bytes)")
        return html, False

    def _request_with_retry(self, url: str, headers: dict) -> requests.Response:
        """Sends request with up to 1 retry on timeout or 5xx status codes."""
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                resp = requests.get(url, headers=headers, timeout=self.timeout)
                if resp.status_code >= 500 and attempt < max_attempts:
                    print(f"[RETRY] {url} returned HTTP {resp.status_code}, retrying attempt {attempt + 1}...")
                    time.sleep(1.0)
                    continue
                return resp
            except (requests.Timeout, requests.ConnectionError) as e:
                if attempt < max_attempts:
                    print(f"[RETRY] {url} encountered {type(e).__name__}, retrying attempt {attempt + 1}...")
                    time.sleep(1.0)
                    continue
                raise
