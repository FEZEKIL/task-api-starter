from typing import Optional
from pydantic import BaseModel, Field, field_validator


class RawBookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str


class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: str
    fetched_at: str

    @field_validator("product_url", "source_page")
    def validate_urls(cls, v: str) -> str:
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(f"URL must start with http:// or https://, got: {v}")
        return v

    @field_validator("price_gbp")
    def validate_price(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"Price must be greater than zero, got: {v}")
        return v


class RunReport(BaseModel):
    start_time: str
    end_time: str
    duration_seconds: float
    catalogue_pages_fetched: int
    detail_pages_fetched: int
    cache_hits: int
    cache_misses: int
    discovered_urls: int
    unique_urls: int
    valid_records: int
    invalid_records: int
    failed_pages: int
