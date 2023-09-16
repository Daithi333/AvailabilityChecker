from unittest.mock import patch

from main import handler

event = {
    "key1": "value1",
    "key2": "value2",
}
context = "tests context"


@patch('main.Controller')
def test_handler_calls_controller_process(mock_controller):
    spy_controller = mock_controller.return_value
    handler(event, context)
    spy_controller.process.assert_called()
