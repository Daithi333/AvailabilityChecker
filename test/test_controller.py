from unittest.mock import Mock

import pytest

from prod.controller import Controller


def test_process_call_to_filereader_returns_url_list():
    return Controller()
    controller.process()
    assert controller.urls[0] == "https://www.tesco.com/groceries/en-GB/search?query=Antibacterial%20wipes\n"
    assert controller.urls[1] == "https://www.tesco.com/groceries/en-GB/search?query=antibacterial%20handwash\n"


def test_process_calls_scrape_html_with_url_list(controller):
    controller.html_handler.scrape_html = Mock()
    controller.process()
    controller.html_handler.scrape_html.assert_called_with(controller.urls)

def test_process_calls_get_products_with_soup_list(controller):
    soup_list = ['page1', 'page2']
    controller.html_handler.scrape_html = Mock(return_value=soup_list)
    controller.process()
    controller.html_handler.get_products.assert_called_with(soup_list)


@pytest.fixture
def controller():
    return Controller()


@pytest.fixture
def file_handler(controller):
    return Mock(controller.file_reader)


@pytest.fixture
def html_handler(controller):
    return Mock(controller.html_handler)


@pytest.fixture
def alert(controller):
    return Mock(controller.alert)
