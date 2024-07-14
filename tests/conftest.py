import pytest
from pathlib import Path


@pytest.fixture
def pages_dir():
    return Path(__file__).parent / "pages"


@pytest.fixture
def results_html(pages_dir):
    results_html = pages_dir / "results.html"
    with open(results_html, "r", encoding="utf-8") as file:
        yield file.read()
