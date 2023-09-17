from unittest.mock import Mock, patch
import pytest

from alert import Alert


def test_alert_send_calls_sns_publish_with_message(mock_alert):
    mock_alert.sns.publish = Mock()
    mock_alert.send('arn:aws:sns:eu-west-1:1234567890:Test', 'Test message')
    mock_alert.sns.publish.assert_called_with(
        Message='Test message',
        TopicArn='arn:aws:sns:eu-west-1:1234567890:Test'
    )


def test_alert_send_returns_the_response_from_publish(mock_alert):
    mock_alert.sns.publish = Mock(return_value='SNS sent')
    result = mock_alert.send('arn:aws:sns:eu-west-1:1234567890:Test', 'Test message')
    assert result == 'SNS sent'


@pytest.fixture
def mock_alert():
    with patch('boto3.client'):
        alert = Alert()
        return alert
