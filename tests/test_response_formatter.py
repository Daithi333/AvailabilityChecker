import pytest

from response_formatter import ResponseFormatter


def test_construct_html(response_formatter):
    products = [
        {'name': 'product1', 'price': '£0.01', 'url': 'product1@tests.com'},
        {'name': 'product2', 'price': '£0.02', 'url': 'product2@tests.com'}
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
        <td><a href="product1@tests.com">View</a></td>
        </tr>
        <tr>
        <td>product2</td>
        <td>£0.02</td>
        <td><a href="product2@tests.com">View</a></td>
        </tr>
        </table>
        </body>
        </html>
        """
    result = response_formatter.construct_html(products)
    assert result.rstrip() == html_response.rstrip()


def test_construct_string(response_formatter, products):
    result = response_formatter.construct_string(products)
    assert result == "The following products are available:\n\nproduct 1\n£0.01\nproduct1url.com\n\nproduct 2\n£0.02\nproduct2url.com\n\n"


@pytest.fixture
def response_formatter():
    return ResponseFormatter()


@pytest.fixture
def products():
    return [
        {'name': 'product 1', 'price': '£0.01', 'url': 'product1url.com'},
        {'name': 'product 2', 'price': '£0.02', 'url': 'product2url.com'}
    ]
