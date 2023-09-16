from unittest.mock import Mock, call, ANY
from urllib import request

import pytest
from urllib3 import Timeout

from bs4 import BeautifulSoup

from html_extractor import HtmlExtractor


def test_html_scraper_calls_request_urlopen_with_urls(html_extractor, soup_stub, mock_request):
    mock_http, mock_response = mock_request
    urls = ['url1.com', 'url2.com']
    expected_calls = [
        call(
            'GET',
            'url1.com',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            },
            timeout=ANY
        ),
        call(
            'GET',
            'url2.com',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'},
            timeout=ANY
        )
    ]
    html_extractor.scrape_html(urls)
    mock_http.assert_has_calls(expected_calls)

    mock_response.data.decode.assert_called_with('utf-8')


def test_html_scraper_returns_soup_list(html_extractor, soup_stub):
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
