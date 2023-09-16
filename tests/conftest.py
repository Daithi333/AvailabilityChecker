from unittest.mock import Mock

import pytest


@pytest.fixture(autouse=True)
def mock_request(monkeypatch):
    mock_response = Mock()
    mock_response.data.decode.return_value = '<p>html content</p>'

    mock_http_request = Mock(return_value=mock_response)

    monkeypatch.setattr("urllib3.PoolManager.request", mock_http_request)

    return mock_http_request, mock_response
