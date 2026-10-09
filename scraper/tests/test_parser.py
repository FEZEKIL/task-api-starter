import pytest
from scraper.src.utils import extract_price_gbp
from scraper.src.parser import parse_catalogue_page, parse_book_page
from scraper.src.models import BookRecord, RawBookRecord


def test_extract_price_gbp():
    assert extract_price_gbp("£51.77") == 51.77
    assert extract_price_gbp("Â£12.34") == 12.34
    assert extract_price_gbp("Price: £0.99") == 0.99
    with pytest.raises(ValueError):
        extract_price_gbp("No price here")


def test_parse_catalogue_page_urls():
    sample_html = """
    <html>
    <body>
        <article class="product_pod">
            <h3><a href="a-light-in-the-attic_1000/index.html">A Light in the Attic</a></h3>
        </article>
        <article class="product_pod">
            <h3><a href="tipping-the-velvet_999/index.html">Tipping the Velvet</a></h3>
        </article>
        <li class="next"><a href="page-2.html">next</a></li>
    </body>
    </html>
    """
    base_url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    product_urls, next_url = parse_catalogue_page(sample_html, base_url)

    assert len(product_urls) == 2
    assert product_urls[0] == "https://books.toscrape.com/catalogue/category/books_1/a-light-in-the-attic_1000/index.html"
    assert next_url == "https://books.toscrape.com/catalogue/category/books_1/page-2.html"


def test_parse_book_page_missing_description():
    sample_html = """
    <html>
    <body>
        <div class="product_main">
            <h1>Test Book Title</h1>
            <p class="price_color">£25.00</p>
            <p class="instock availability">In stock (5 available)</p>
            <p class="star-rating Four"></p>
        </div>
    </body>
    </html>
    """
    book_url = "https://books.toscrape.com/catalogue/test-book_1/index.html"
    raw_rec = parse_book_page(sample_html, book_url, source_page="https://books.toscrape.com/index.html", fetched_at="2026-08-06T10:00:00Z")

    assert raw_rec.title == "Test Book Title"
    assert raw_rec.price_text == "£25.00"
    assert raw_rec.description is None
    assert raw_rec.rating_text == "Four"


def test_book_record_schema_validation():
    valid = BookRecord(
        title="Valid Title",
        product_url="https://books.toscrape.com/catalogue/valid_1/index.html",
        price_text="£10.00",
        price_gbp=10.00,
        availability_text="In stock",
        rating_text="Five",
        description="A good book",
        source_page="https://books.toscrape.com/index.html",
        fetched_at="2026-08-06T10:00:00Z"
    )
    assert valid.price_gbp == 10.00

    with pytest.raises(ValueError):
        # Invalid relative URL
        BookRecord(
            title="Bad URL",
            product_url="invalid_url_without_http",
            price_text="£10.00",
            price_gbp=10.00,
            availability_text="In stock",
            rating_text="Five",
            source_page="https://books.toscrape.com/index.html",
            fetched_at="2026-08-06T10:00:00Z"
        )
