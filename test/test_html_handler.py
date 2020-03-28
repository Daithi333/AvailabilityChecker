from io import StringIO
from unittest.mock import Mock, call
from urllib import request
from bs4 import BeautifulSoup

from prod.htm_handler import HtmlHandler


def test_html_scraper_calls_request_urlopen_with_urls():
    urls = ['url1.com', 'url2.com']
    request.urlopen = Mock(return_value=StringIO('<p>html content</p>'))
    soup_stub = Mock(BeautifulSoup)
    html_handler = HtmlHandler()
    html_handler.scrape_html(urls)
    request.urlopen.assert_has_calls([call('url1.com'), call('url2.com')])


def test_html_scraper_returns_soup_list():
    urls = ['url1.com', 'url2.com']
    request.urlopen = Mock(return_value=StringIO('<p>html content</p>'))
    soup_stub = Mock(BeautifulSoup)
    html_handler = HtmlHandler()
    result = html_handler.scrape_html(urls)
    assert len(result) == 2
    assert str(result[0]) == '<p>html content</p>'
