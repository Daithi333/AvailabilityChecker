from unittest.mock import Mock, patch
import pytest

from app.controller import Controller


def test_process_calls_read_lines(controller, read_lines):
    controller.process()
    read_lines.assert_called()


def test_process_calls_scrape_html_called_with_url_list(controller, read_lines, scrape_html):
    controller.process()
    controller.html_extractor.scrape_html.assert_called_with(['url1', 'url2'])


def test_process_calls_get_products_with_soup_list(controller, read_lines, scrape_html, get_products):
    controller.process()
    controller.html_extractor.get_products_tesco.assert_called_with(['<p>page 1</p>', '<p>page 2</p>'])


def test_process_calls_format_response_string_with_products_list(controller, read_lines, scrape_html, products, get_products, construct_string):
    controller.process()
    controller.response_formatter.construct_string.assert_called_with(products)


@pytest.mark.skip('html response no longer being sent')
def test_process_calls_alert_send_with_html_response(controller, read_lines, scrape_html, get_products, construct_html, alert_send):
    controller.process()
    controller.alert.send.assert_called_with("<p>Test html</p>")


def test_process_calls_alert_send_with_formatted_response(controller, read_lines, scrape_html, get_products, construct_string, alert_send):
    controller.process()
    controller.alert.send.assert_called_with("Products available:\n\nproduct1\n£0.01\nproduct1url.com\n\n")


def test_process_returns_response(controller, read_lines, scrape_html, get_products, alert_send):
    response = controller.process()
    assert response == 'SNS alert sent'


@pytest.mark.skip('code returns error instead of raising')
def test_process_read_lines_raises_io_error_when_file_not_found(controller):
    with pytest.raises(IOError):
        controller.process()


def test_process_read_lines_returns_error_when_file_not_found(controller, read_lines_exception):
    response = controller.process()
    assert response == ("[Errno 2] No such file or directory: 'test.txt'")


@pytest.fixture
def controller():
    with patch('boto3.client'):
        controller = Controller()
    return controller


@pytest.fixture
def read_lines(controller):
    controller.file_reader.read_lines = Mock(return_value=['url1', 'url2'])
    return controller.file_reader.read_lines


@pytest.fixture
def scrape_html(controller):
    soup_list = ['<p>page 1</p>', '<p>page 2</p>']
    controller.html_extractor.scrape_html = Mock(return_value=soup_list)
    return controller.html_extractor.scrape_html


@pytest.fixture
def products(controller):
    return [
        {'name': 'product 1', 'price': '£0.01', 'url': 'product1url.com'},
        {'name': 'product 2', 'price': '£0.02', 'url': 'product2url.com'}
    ]


@pytest.fixture
def get_products(controller, products):
    controller.html_extractor.get_products_tesco = Mock(return_value=products)
    return controller.html_extractor.get_products_tesco


@pytest.fixture
def construct_html(controller):
    html_response = "<p>Test html</p>"
    controller.response_formatter.construct_html = Mock(return_value=html_response)
    return controller.response_formatter.construct_html


@pytest.fixture
def construct_string(controller):
    string_response = "Products available:\n\nproduct1\n£0.01\nproduct1url.com\n\n"
    controller.response_formatter.construct_string = Mock(return_value=string_response)
    return controller.response_formatter.construct_string


@pytest.fixture
def alert_send(controller):
    controller.alert.send = Mock(return_value='SNS alert sent')
    return controller.alert.send


@pytest.fixture
def read_lines_exception(controller):
    exception = Exception("[Errno 2] No such file or directory: 'test.txt'")
    controller.file_reader.read_lines = Mock(side_effect=exception)
    return controller.file_reader.read_lines
