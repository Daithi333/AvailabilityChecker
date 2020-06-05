from io import StringIO
from unittest.mock import Mock, call
from urllib import request

import pytest

from bs4 import BeautifulSoup

from app.html_extractor import HtmlExtractor


def test_html_scraper_calls_request_urlopen_with_urls(html_extractor, soup_stub, request_urlopen):
    urls = ['url1.com', 'url2.com']
    html_extractor.scrape_html(urls)
    request.urlopen.assert_has_calls([call('url1.com'), call('url2.com')])


def test_html_scraper_returns_soup_list(html_extractor, soup_stub, request_urlopen):
    urls = ['url1.com', 'url2.com']
    result = html_extractor.scrape_html(urls)
    assert len(result) == 2
    assert str(result[0]) == '<p>html content</p>'


@pytest.fixture
def html_extractor():
    return HtmlExtractor()


@pytest.fixture
def soup_stub():
    return Mock(BeautifulSoup)


@pytest.fixture
def request_urlopen():
    request.urlopen = Mock(return_value=StringIO('<p>html content</p>'))
    return request.urlopen

