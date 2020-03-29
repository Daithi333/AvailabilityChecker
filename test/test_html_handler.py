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

def test_format_results_returns_html_containing_product_info():
    products = [
        {'name': 'product1', 'price': '£0.01', 'url': 'product1@test.com'},
        {'name': 'product2', 'price': '£0.02', 'url': 'product2@test.com'}
    ]

    html_response = """\
        <html>
        <head>
        </head>
        <body>
        <h2>The following products are available:</h2>
        <table>
        <tr>
        <th>Product</th>
        <th>Price</th>
        <th>Link</th>
        </tr>
        <tr>
        <td>product1</td>
        <td>£0.01</td>
        <td><a href="product1@test.com">View</a></td>
        </tr>
        <tr>
        <td>product2</td>
        <td>£0.02</td>
        <td><a href="product2@test.com">View</a></td>
        </tr>
        </table>
        </body>
        </html>
        """

    html_handler = HtmlHandler()
    result = html_handler.format_results(products)
    assert result.rstrip() == html_response.rstrip()
