from unittest.mock import Mock, patch
import pytest

from app.alert import Alert


def test_alert_send_calls_sns_publish_with_message(alert):
    alert.sns.publish = Mock()
    alert.send('Test message')
    alert.sns.publish.assert_called_with(Message='Test message', TopicArn='arn:aws:sns:eu-west-1:757607970807:ProductAlert')


def test_alert_send_returns_the_response_from_publish(alert):
    alert.sns.publish = Mock(return_value='SNS sent')
    result = alert.send('Test message')
    assert result == 'SNS sent'


@pytest.fixture
def alert():
    with patch('boto3.client'):
        alert = Alert()
        return alert
