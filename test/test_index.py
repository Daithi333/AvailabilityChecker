from unittest.mock import patch

import index

event = {
    "key1": "value1",
    "key2": "value2",
}
context = "test context"


@patch('index.Controller')
def test_handler_calls_controller_process(fake_controller):
    spy_controller = fake_controller.return_value
    index.handler(event, context)
    spy_controller.process.assert_called()
